"""FastAPI 웹 서버 모듈.

TSK-01-01: FastAPI 앱 및 라우트 정의
TSK-02-01: 트리 데이터 API
TSK-03-01: Task 상세 API 및 템플릿
TSK-05-01: Document Viewer API
TSK-06-01: 트리 패널 개선 (통계 배지, 검색, WP/ACT Detail)
TSK-06-02: Task Detail 패널 개선 (워크플로우 스테퍼, 진행률)
TSK-06-03: 문서 테이블 (메타정보 포함)
"""

from __future__ import annotations

import asyncio
import hashlib
import os
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, PlainTextResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import StreamingResponse

from orchay.web.filters import status_bg, status_icon
from orchay.web.markdown_renderer import get_pygments_css, render_markdown
from orchay.web.tree import build_tree, build_wp_children

if TYPE_CHECKING:
    from orchay.main import Orchestrator
    from orchay.models import Task

# TSK-05-01: Document Viewer 허용 확장자
ALLOWED_EXTENSIONS = {".md", ".png", ".jpg", ".jpeg", ".gif", ".webp"}

# TSK-06-02: 워크플로우 단계 정의
WORKFLOW_STEPS = ["시작 전", "설계", "승인", "구현", "검증", "완료"]

# TSK-06-02: 상태별 워크플로우 단계 인덱스 매핑
STATUS_TO_STEP: dict[str, int] = {
    "[ ]": 0,  # 시작 전
    "[bd]": 1,  # 설계
    "[dd]": 1,  # 설계
    "[an]": 1,  # 설계
    "[ds]": 1,  # 설계
    "[ap]": 2,  # 승인
    "[im]": 3,  # 구현
    "[fx]": 3,  # 구현
    "[vf]": 4,  # 검증
    "[xx]": 5,  # 완료
}

# TSK-06-02: 상태별 진행률 (BR-002)
STATUS_TO_PROGRESS: dict[str, int] = {
    "[ ]": 0,
    "[bd]": 15,
    "[dd]": 25,
    "[an]": 25,
    "[ds]": 25,
    "[ap]": 40,
    "[im]": 60,
    "[fx]": 60,
    "[vf]": 80,
    "[xx]": 100,
}


def get_workflow_step(status: str) -> int:
    """상태 코드에서 워크플로우 단계 인덱스 반환 (TSK-06-02).

    Args:
        status: 상태 코드 (예: '[dd]')

    Returns:
        워크플로우 단계 인덱스 (0-5)
    """
    return STATUS_TO_STEP.get(status, 0)


def get_task_progress(status: str) -> int:
    """상태 코드에서 진행률 반환 (TSK-06-02).

    Args:
        status: 상태 코드 (예: '[dd]')

    Returns:
        진행률 (0-100)
    """
    return STATUS_TO_PROGRESS.get(status, 0)


def format_file_size(size_bytes: int) -> str:
    """파일 크기를 사람이 읽기 쉬운 형태로 변환 (TSK-06-03 BR-02).

    Args:
        size_bytes: 파일 크기 (바이트)

    Returns:
        포맷된 크기 문자열 (예: "8.3 KB")
    """
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f} MB"


def format_date(timestamp: float) -> str:
    """Unix timestamp를 YYYY-MM-DD 형식으로 변환 (TSK-06-03 BR-03).

    Args:
        timestamp: Unix timestamp

    Returns:
        포맷된 날짜 문자열 (예: "2025-12-28")
    """
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")


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


def calculate_tree_version(tasks: list[Task]) -> str:
    """Task 상태 기반 버전 해시 생성 (조건부 폴링용).

    변경 없으면 304 Not Modified를 반환하여 DOM을 건드리지 않도록 함.

    Args:
        tasks: Task 목록

    Returns:
        8자리 MD5 해시 문자열
    """
    status_str = "|".join(
        f"{t.id}:{t.status.value}" for t in sorted(tasks, key=lambda t: t.id)
    )
    return hashlib.md5(status_str.encode()).hexdigest()[:8]


def get_task_documents(
    task_id: str,
    base_path: Path | None = None,
    project_name: str = "",
) -> list[dict[str, str | int]]:
    """Task 관련 문서 목록 조회 (TSK-06-03: 메타정보 포함).

    Args:
        task_id: Task ID (예: TSK-01-01)
        base_path: Task 문서 기본 경로 (기본: .orchay/projects/{project}/tasks)
        project_name: 프로젝트 이름

    Returns:
        문서 메타정보 딕셔너리 목록 (정렬됨)
        각 항목: {name, type, size, size_formatted, modified, modified_formatted}
    """
    if base_path is None:
        # 기본 경로: .orchay/projects/{project}/tasks/{task_id}/
        base_path = Path(".orchay/projects") / project_name / "tasks"

    task_dir = base_path / task_id

    if not task_dir.exists() or not task_dir.is_dir():
        return []

    docs: list[dict[str, str | int]] = []

    for f in task_dir.iterdir():
        if not f.is_file():
            continue
        suffix = f.suffix.lower()
        if suffix not in ALLOWED_EXTENSIONS:
            continue

        # 파일 메타정보 조회 (TSK-06-03)
        try:
            stat = os.stat(f)
            size = stat.st_size
            modified = stat.st_mtime
        except OSError:
            size = 0
            modified = 0.0

        docs.append(
            {
                "name": f.name,
                "type": suffix[1:].upper(),  # ".md" -> "MD"
                "size": size,
                "size_formatted": format_file_size(size),
                "modified": modified,
                "modified_formatted": format_date(modified) if modified > 0 else "-",
            }
        )

    # 파일명 기준 정렬
    return sorted(docs, key=lambda d: str(d["name"]))


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

    @app.get("/api/tree", response_class=HTMLResponse, response_model=None)
    async def _get_tree(request: Request) -> HTMLResponse | Response:
        """WBS 트리 HTML 조각 (TSK-06-01: 통계 포함, 조건부 폴링).

        ETag 기반 조건부 응답으로 변경이 없으면 304 반환.
        이를 통해 클라이언트 DOM을 건드리지 않아 Tree 펼침/선택 상태 유지.
        """
        tasks = orchestrator.tasks
        version = calculate_tree_version(tasks)

        # ETag 조건 체크: 변경 없으면 304 반환 (DOM 건드리지 않음)
        if request.headers.get("If-None-Match") == version:
            return Response(status_code=304)

        tree = build_tree(tasks)
        stats = calculate_stats(tasks)
        response = templates.TemplateResponse(
            request,
            "partials/tree.html",
            {"tree": tree, "stats": stats},
        )
        response.headers["ETag"] = version
        return response

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
        """Task 상세 HTML 조각 (TSK-06-02: 워크플로우 스테퍼, 요구사항 추가)."""
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

        # TSK-06-02: 워크플로우 스테퍼 및 진행률 데이터
        current_step = get_workflow_step(task.status.value)
        task_progress = get_task_progress(task.status.value)

        return templates.TemplateResponse(
            request,
            "partials/detail.html",
            {
                "task": task,
                "documents": documents,
                "project_name": orchestrator.project_name,
                "workflow_steps": WORKFLOW_STEPS,
                "current_step": current_step,
                "task_progress": task_progress,
            },
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
    ) -> HTMLResponse | FileResponse:
        """문서/이미지 파일 조회 (TSK-05-01: Document Viewer API).

        Args:
            task_id: Task ID (예: TSK-05-01)
            doc_name: 파일명 (예: 010-design.md)

        Returns:
            - .md 파일: HTMLResponse (렌더링된 HTML)
            - 이미지 파일: FileResponse

        Raises:
            HTTPException 400: 허용되지 않는 확장자
            HTTPException 403: Path traversal 시도
            HTTPException 404: 파일 없음
        """
        # 기본 경로 설정
        base_path = (Path(".orchay/projects") / orchestrator.project_name / "tasks").resolve()
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
            # 서버 사이드 Markdown 렌더링 (markdown-it-py + Pygments)
            raw_content = file_path.read_text(encoding="utf-8")
            html_content = render_markdown(raw_content)
            return HTMLResponse(html_content, media_type="text/html; charset=utf-8")
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

    @app.get("/api/pygments.css", response_class=PlainTextResponse)
    async def _get_pygments_css() -> PlainTextResponse:
        """Pygments 코드 하이라이팅 CSS 반환 (monokai 테마)."""
        css = get_pygments_css("monokai")
        return PlainTextResponse(css, media_type="text/css")

    @app.get("/api/events")
    async def _sse_events(request: Request) -> StreamingResponse:
        """SSE 엔드포인트 - Task/Worker 상태 변경 시에만 이벤트 발송.

        깜빡임 없는 실시간 업데이트를 위해 폴링 대신 SSE 사용.
        변경이 있을 때만 OOB HTML을 전송하여 해당 요소만 교체.
        """

        async def event_generator():
            last_tree_version = ""
            last_worker_states = ""

            while True:
                # 연결 끊김 확인
                if await request.is_disconnected():
                    break

                tasks = orchestrator.tasks
                workers = orchestrator.workers

                # Tree 버전 계산
                current_tree_version = calculate_tree_version(tasks)

                # Worker 상태 문자열
                current_worker_states = "|".join(
                    f"{w.id}:{w.state.value}" for w in workers
                )

                events_to_send = []

                # Tree 상태 변경 감지
                if current_tree_version != last_tree_version:
                    last_tree_version = current_tree_version

                    # 상태 배지 OOB HTML 생성
                    oob_badges = _generate_status_badges_oob(tasks)
                    if oob_badges:
                        events_to_send.append(("tree-update", oob_badges))

                    # 진행률 OOB HTML 생성
                    stats = calculate_stats(tasks)
                    progress_oob = _generate_progress_oob(stats)
                    events_to_send.append(("progress-update", progress_oob))

                # Worker 상태 변경 감지
                if current_worker_states != last_worker_states:
                    last_worker_states = current_worker_states

                    # Worker 바 HTML 생성 (OOB로 감싸기)
                    progress = calculate_progress(tasks)
                    workers_inner = templates.get_template("partials/workers.html").render(
                        workers=workers, progress=progress
                    )
                    # workers-bar의 내용만 OOB로 교체
                    oob_workers = (
                        f'<div id="workers-bar" hx-swap-oob="innerHTML" '
                        f'class="bg-gray-800 border-b border-gray-700 px-4 py-2">'
                        f'{workers_inner}</div>'
                    )
                    events_to_send.append(("workers-update", oob_workers))

                # 이벤트 전송
                for event_name, data in events_to_send:
                    # SSE 형식: 줄바꿈을 공백으로 치환 (SSE 프로토콜)
                    escaped_data = data.replace("\n", " ")
                    yield f"event: {event_name}\ndata: {escaped_data}\n\n"

                await asyncio.sleep(2)  # 2초마다 체크

        return StreamingResponse(
            event_generator(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",  # nginx 버퍼링 비활성화
            },
        )

    return app


def _generate_status_badges_oob(tasks: list[Task]) -> str:
    """상태 배지 OOB HTML 생성 (SSE용).

    각 Task의 상태 배지를 hx-swap-oob="true"로 감싸서
    해당 ID의 요소만 교체되도록 함.

    Args:
        tasks: Task 목록

    Returns:
        OOB HTML 문자열
    """
    # 상태별 배경색 매핑
    color_map = {
        "[ ]": "bg-gray-500",
        "[bd]": "bg-blue-500",
        "[dd]": "bg-purple-500",
        "[an]": "bg-indigo-500",
        "[ds]": "bg-cyan-500",
        "[ap]": "bg-green-500",
        "[im]": "bg-yellow-500",
        "[fx]": "bg-orange-500",
        "[vf]": "bg-teal-500",
        "[xx]": "bg-emerald-500",
    }

    oob_parts = []
    for task in tasks:
        status = task.status.value
        color = color_map.get(status, "bg-gray-500")
        badge_html = (
            f'<span id="status-{task.id}" hx-swap-oob="true" '
            f'class="status-badge px-1.5 py-0.5 text-xs rounded {color} '
            f'text-white min-w-[32px] text-center">{status}</span>'
        )
        oob_parts.append(badge_html)

    return "".join(oob_parts)


def _generate_progress_oob(stats: dict[str, int]) -> str:
    """진행률 바 OOB HTML 생성 (SSE용).

    Args:
        stats: 통계 정보

    Returns:
        OOB HTML 문자열
    """
    percentage = stats.get("percentage", 0)
    return (
        f'<div id="stats-progress-bar" hx-swap-oob="true" '
        f'class="h-full bg-emerald-500 transition-all duration-300" '
        f'style="width: {percentage}%"></div>'
        f'<span id="stats-progress-text" hx-swap-oob="true" '
        f'class="text-sm text-gray-400 min-w-[40px]">{percentage}%</span>'
    )


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
