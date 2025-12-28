"""FastAPI 웹 서버 모듈.

TSK-01-01: FastAPI 앱 및 라우트 정의
TSK-02-01: 트리 데이터 API
TSK-03-01: Task 상세 API 및 템플릿
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from orchay.web.filters import status_bg, status_icon
from orchay.web.tree import build_tree, build_wp_children

if TYPE_CHECKING:
    from orchay.main import Orchestrator
    from orchay.models import Task


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
    """Task 관련 문서 목록 조회.

    Args:
        task_id: Task ID (예: TSK-01-01)
        base_path: Task 문서 기본 경로 (기본: .jjiban/projects/{project}/tasks)
        project_name: 프로젝트 이름

    Returns:
        존재하는 문서 파일명 목록 (정렬됨)
    """
    if base_path is None:
        # 기본 경로: .jjiban/projects/{project}/tasks/{task_id}/
        base_path = Path(".jjiban/projects") / project_name / "tasks"

    task_dir = base_path / task_id

    if not task_dir.exists() or not task_dir.is_dir():
        return []

    # .md 파일만 반환, 정렬
    docs = [f.name for f in task_dir.iterdir() if f.is_file() and f.suffix == ".md"]
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
        """WBS 트리 HTML 조각."""
        tasks = orchestrator.tasks
        tree = build_tree(tasks)
        return templates.TemplateResponse(
            request,
            "partials/tree.html",
            {"tree": tree},
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

    return app


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
