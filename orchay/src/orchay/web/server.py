"""FastAPI 웹 서버 모듈.

TSK-01-01: FastAPI 앱 및 라우트 정의
TSK-02-01: 트리 데이터 API
TSK-03-01: Task 상세 API 및 템플릿
TSK-05-01: Document Viewer API
TSK-06-01: 트리 패널 개선 (통계 배지, 검색, WP/ACT Detail)
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from orchay.web.filters import status_bg, status_icon
from orchay.web.tree import build_tree, build_wp_children

if TYPE_CHECKING:
    from orchay.main import Orchestrator
    from orchay.models import Task

# TSK-05-01: Document Viewer 허용 확장자
ALLOWED_EXTENSIONS = {".md", ".png", ".jpg", ".jpeg", ".gif", ".webp"}


def calculate_stats(tasks: list[Task]) -> dict[str, int]:
    """통계 정보 계산 (TSK-06-01).

    Args:
        tasks: Task 목록

    Returns:
        통계 정보 {"wp_count", "act_count", "tsk_count", "done_count", "percentage"}
    """
    wp_ids: set[str] = set()
    act_ids: set[str] = set()

    for task in tasks:
        parts = task.id.split("-")
        if len(parts) >= 2:
            wp_ids.add(f"WP-{parts[1]}")
        if len(parts) >= 3:
            act_ids.add(f"ACT-{parts[1]}-{parts[2]}")

    total = len(tasks)
    done = sum(1 for t in tasks if t.status.value == "[xx]")

    return {
        "wp_count": len(wp_ids),
        "act_count": len(act_ids) if act_ids else 0,
        "tsk_count": total,
        "done_count": done,
        "percentage": int((done / total) * 100) if total > 0 else 0,
    }


def calculate_progress(tasks: list[Task]) -> dict[str, int]:
    """전체 진행률 계산.

    Args:
        tasks: Task 목록

    Returns:
        진행률 정보 {"total": int, "done": int, "percentage": int}
    """
    total = len(tasks)
    if total == 0:
        return {"total": 0, "done": 0, "percentage": 0}

    done = sum(1 for t in tasks if t.status.value == "[xx]")
    percentage = int((done / total) * 100)
    return {"total": total, "done": done, "percentage": percentage}


def get_task_documents(
    task_id: str,
    base_path: Path | None = None,
    project_name: str = "",
) -> list[str]:
    """Task 관련 문서 목록 조회 (TSK-05-01: 이미지 지원 추가).

    Args:
        task_id: Task ID (예: TSK-01-01)
        base_path: Task 문서 기본 경로 (기본: .jjiban/projects/{project}/tasks)
        project_name: 프로젝트 이름

    Returns:
        존재하는 문서/이미지 파일명 목록 (정렬됨)
    """
    if base_path is None:
        # 기본 경로: .jjiban/projects/{project}/tasks/{task_id}/
        base_path = Path(".jjiban/projects") / project_name / "tasks"

    task_dir = base_path / task_id

    if not task_dir.exists() or not task_dir.is_dir():
        return []

    # 허용된 확장자 파일만 반환, 정렬
    docs = [
        f.name
        for f in task_dir.iterdir()
        if f.is_file() and f.suffix.lower() in ALLOWED_EXTENSIONS
    ]
    return sorted(docs)


def create_app(orchestrator: Orchestrator) -> FastAPI:
    """FastAPI 앱 생성 및 Orchestrator 참조 주입.

    Args:
        orchestrator: Task 오케스트레이터 인스턴스

    Returns:
        설정된 FastAPI 앱 인스턴스
    """
    app = FastAPI(title="orchay Web Monitor")

    # 경로 설정
    base_dir = Path(__file__).parent
    templates = Jinja2Templates(directory=base_dir / "templates")

    # Jinja2 필터 등록
    templates.env.filters["status_icon"] = status_icon
    templates.env.filters["status_bg"] = status_bg

    # 정적 파일 마운트
    static_dir = base_dir / "static"
    if static_dir.exists():
        app.mount("/static", StaticFiles(directory=static_dir), name="static")

    # Orchestrator 참조 저장
    app.state.orchestrator = orchestrator

    @app.get("/", response_class=HTMLResponse)
    async def _index(request: Request) -> HTMLResponse:
        """메인 페이지."""
        return templates.TemplateResponse(
            request,
            "index.html",
            {
                "project_name": orchestrator.project_name,
                "mode": orchestrator.mode.value,
            },
        )

    @app.get("/api/tree", response_class=HTMLResponse)
    async def _get_tree(request: Request) -> HTMLResponse:
        """WBS 트리 HTML 조각 (TSK-06-01: 통계 포함)."""
        tasks = orchestrator.tasks
        tree = build_tree(tasks)
        stats = calculate_stats(tasks)
        return templates.TemplateResponse(
            request,
            "partials/tree.html",
            {"tree": tree, "stats": stats},
        )

    @app.get("/api/tree/{wp_id}", response_class=HTMLResponse)
    async def _get_wp_children(request: Request, wp_id: str) -> HTMLResponse:
        """WP 하위 노드 HTML 조각."""
        tasks = orchestrator.tasks
        try:
            children = build_wp_children(tasks, wp_id)
        except ValueError:
            return templates.TemplateResponse(
                request,
                "partials/error.html",
                {"message": f"WP '{wp_id}'를 찾을 수 없습니다"},
                status_code=404,
            )

        return templates.TemplateResponse(
            request,
            "partials/wp_children.html",
            {"wp_id": wp_id, "children": children},
        )

    @app.get("/api/detail/{task_id}", response_class=HTMLResponse)
    async def _get_detail(request: Request, task_id: str) -> HTMLResponse:
        """Task 상세 HTML 조각."""
        task = _find_task(orchestrator.tasks, task_id)
        if not task:
            return templates.TemplateResponse(
                request,
                "partials/error.html",
                {"message": f"Task '{task_id}'를 찾을 수 없습니다"},
                status_code=404,
            )

        # FR-007: 관련 문서 목록 조회
        documents = get_task_documents(
            task_id=task_id,
            project_name=orchestrator.project_name,
        )

        return templates.TemplateResponse(
            request,
            "partials/detail.html",
            {"task": task, "documents": documents},
        )

    @app.get("/api/workers", response_class=HTMLResponse)
    async def _get_workers(request: Request) -> HTMLResponse:
        """Worker 상태 HTML 조각 (진행률 포함)."""
        workers = orchestrator.workers
        progress = calculate_progress(orchestrator.tasks)
        return templates.TemplateResponse(
            request,
            "partials/workers.html",
            {"workers": workers, "progress": progress},
        )

    @app.get("/api/wp-detail/{wp_id}", response_class=HTMLResponse)
    async def _get_wp_detail(request: Request, wp_id: str) -> HTMLResponse:
        """WP 상세 정보 HTML 조각 (TSK-06-01)."""
        tasks = orchestrator.tasks
        wp_info = _get_wp_info(tasks, wp_id)
        if not wp_info:
            return templates.TemplateResponse(
                request,
                "partials/error.html",
                {"message": f"WP '{wp_id}'를 찾을 수 없습니다"},
                status_code=404,
            )
        return templates.TemplateResponse(
            request,
            "partials/wp_detail.html",
            {"wp": wp_info},
        )

    @app.get("/api/document/{task_id}/{doc_name:path}", response_model=None)
    async def _get_document(
        task_id: str,
        doc_name: str,
    ) -> PlainTextResponse:
        """문서/이미지 파일 조회 (TSK-05-01: Document Viewer API).

        Args:
            task_id: Task ID (예: TSK-05-01)
            doc_name: 파일명 (예: 010-design.md)

        Returns:
            - .md 파일: PlainTextResponse (마크다운 텍스트)
            - 이미지 파일: FileResponse

        Raises:
            HTTPException 400: 허용되지 않는 확장자
            HTTPException 403: Path traversal 시도
            HTTPException 404: 파일 없음
        """
        # 기본 경로 설정
        base_path = (
            Path(".jjiban/projects") / orchestrator.project_name / "tasks"
        ).resolve()
        file_path = (base_path / task_id / doc_name).resolve()

        # Path traversal 검증 (BR-02)
        if not file_path.is_relative_to(base_path):
            raise HTTPException(status_code=403, detail="Access denied")

        # 확장자 검증 (BR-01)
        suffix = file_path.suffix.lower()
        if suffix not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {suffix}",
            )

        # 파일 존재 확인
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="Document not found")

        # 응답 타입 결정 (BR-03, BR-04)
        if suffix == ".md":
            content = file_path.read_text(encoding="utf-8")
            return PlainTextResponse(content, media_type="text/plain; charset=utf-8")
        else:
            # 이미지 MIME 타입 매핑
            mime_types = {
                ".png": "image/png",
                ".jpg": "image/jpeg",
                ".jpeg": "image/jpeg",
                ".gif": "image/gif",
                ".webp": "image/webp",
            }
            return FileResponse(file_path, media_type=mime_types.get(suffix, "image/png"))

    return app


def _get_wp_info(tasks: list[Task], wp_id: str) -> dict | None:
    """WP 정보 추출 (TSK-06-01).

    Args:
        tasks: Task 목록
        wp_id: WP ID (예: WP-01)

    Returns:
        WP 정보 딕셔너리 또는 None
    """
    # WP ID에서 번호 추출
    wp_num = wp_id.replace("WP-", "")
    wp_tasks = [t for t in tasks if t.id.split("-")[1] == wp_num]

    if not wp_tasks:
        return None

    done_count = sum(1 for t in wp_tasks if t.status.value == "[xx]")
    total_count = len(wp_tasks)
    progress = int((done_count / total_count) * 100) if total_count > 0 else 0

    return {
        "id": wp_id,
        "title": f"Work Package {wp_num}",
        "child_count": total_count,
        "done_count": done_count,
        "progress": progress,
        "tasks": wp_tasks,
    }


def _build_tree(tasks: list[Task]) -> dict[str, dict[str, list[Task]]]:
    """Task 목록을 WP/ACT 계층 구조로 변환.

    Args:
        tasks: Task 목록

    Returns:
        WP -> ACT -> Task 계층 구조
    """
    tree: dict[str, dict[str, list[Task]]] = {}

    for task in tasks:
        # Task ID 파싱: TSK-XX-YY 형식
        parts = task.id.split("-")
        if len(parts) >= 3:
            wp_id = f"WP-{parts[1]}"
            act_id = f"ACT-{parts[1]}-{parts[2]}"
        else:
            wp_id = "WP-00"
            act_id = "ACT-00-00"

        if wp_id not in tree:
            tree[wp_id] = {}
        if act_id not in tree[wp_id]:
            tree[wp_id][act_id] = []

        tree[wp_id][act_id].append(task)

    return tree


def _find_task(tasks: list[Task], task_id: str) -> Task | None:
    """Task ID로 Task 검색.

    Args:
        tasks: Task 목록
        task_id: 검색할 Task ID

    Returns:
        찾은 Task 또는 None
    """
    for task in tasks:
        if task.id == task_id:
            return task
    return None
