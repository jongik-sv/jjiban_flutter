"""FastAPI 웹 서버 모듈.

TSK-01-01: FastAPI 앱 및 라우트 정의
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

if TYPE_CHECKING:
    from orchay.main import Orchestrator
    from orchay.models import Task


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
                "project": orchestrator.project_name,
                "mode": orchestrator.mode.value,
            },
        )

    @app.get("/api/tree", response_class=HTMLResponse)
    async def _get_tree(request: Request) -> HTMLResponse:
        """WBS 트리 HTML 조각."""
        tasks = orchestrator.tasks
        tree = _build_tree(tasks)
        return templates.TemplateResponse(
            request,
            "partials/tree.html",
            {"tree": tree},
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
        return templates.TemplateResponse(
            request,
            "partials/detail.html",
            {"task": task},
        )

    @app.get("/api/workers", response_class=HTMLResponse)
    async def _get_workers(request: Request) -> HTMLResponse:
        """Worker 상태 HTML 조각."""
        workers = orchestrator.workers
        return templates.TemplateResponse(
            request,
            "partials/workers.html",
            {"workers": workers},
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
