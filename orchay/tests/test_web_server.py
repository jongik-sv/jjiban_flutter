"""FastAPI 웹 서버 테스트.

TSK-01-01: FastAPI 앱 및 라우트 정의 테스트
"""

from unittest.mock import Mock

import pytest
from fastapi import FastAPI


# TC-01: create_app 함수 테스트
def test_create_app() -> None:
    """create_app이 FastAPI 앱을 정상적으로 생성하는지 테스트."""
    from orchay.web.server import create_app

    mock_orchestrator = Mock()
    mock_orchestrator.project_name = "test_project"
    mock_orchestrator.mode = Mock(value="quick")
    mock_orchestrator.tasks = []
    mock_orchestrator.workers = []

    app = create_app(mock_orchestrator)

    assert app is not None
    assert isinstance(app, FastAPI)
    assert app.state.orchestrator == mock_orchestrator


# TC-07: Orchestrator 접근 테스트
def test_orchestrator_reference() -> None:
    """Orchestrator 참조가 올바르게 저장되는지 테스트."""
    from orchay.web.server import create_app

    mock_orchestrator = Mock()
    mock_orchestrator.project_name = "test_project"
    mock_orchestrator.mode = Mock(value="quick")
    mock_orchestrator.tasks = []
    mock_orchestrator.workers = []

    app = create_app(mock_orchestrator)

    assert app.state.orchestrator is mock_orchestrator


# TC-02: 메인 페이지 응답 테스트
@pytest.mark.asyncio
async def test_index_page() -> None:
    """메인 페이지가 정상적으로 렌더링되는지 테스트."""
    from httpx import ASGITransport, AsyncClient

    from orchay.web.server import create_app

    mock_orchestrator = Mock()
    mock_orchestrator.project_name = "test_project"
    mock_orchestrator.mode = Mock(value="quick")
    mock_orchestrator.tasks = []
    mock_orchestrator.workers = []

    app = create_app(mock_orchestrator)
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "test_project" in response.text


# TC-03: 트리 API 응답 테스트
@pytest.mark.asyncio
async def test_tree_api() -> None:
    """트리 API가 HTML 조각을 반환하는지 테스트."""
    from httpx import ASGITransport, AsyncClient

    from orchay.web.server import create_app

    mock_task = Mock()
    mock_task.id = "TSK-01-01"
    mock_task.title = "Test Task"
    mock_task.status = Mock(value="[ ]")

    mock_orchestrator = Mock()
    mock_orchestrator.project_name = "test_project"
    mock_orchestrator.mode = Mock(value="quick")
    mock_orchestrator.tasks = [mock_task]
    mock_orchestrator.workers = []

    app = create_app(mock_orchestrator)
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/tree")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


# TC-04: Task 상세 API 응답 테스트
@pytest.mark.asyncio
async def test_detail_api() -> None:
    """Task 상세 API가 올바른 정보를 반환하는지 테스트."""
    from httpx import ASGITransport, AsyncClient

    from orchay.web.server import create_app

    mock_task = Mock()
    mock_task.id = "TSK-01-01"
    mock_task.title = "Test Task"
    mock_task.status = Mock(value="[ ]")
    mock_task.category = Mock(value="development")
    mock_task.priority = Mock(value="high")
    mock_task.domain = "backend"
    mock_task.assignee = "developer"
    mock_task.tags = ["test"]
    mock_task.depends = []

    mock_orchestrator = Mock()
    mock_orchestrator.project_name = "test_project"
    mock_orchestrator.mode = Mock(value="quick")
    mock_orchestrator.tasks = [mock_task]
    mock_orchestrator.workers = []

    app = create_app(mock_orchestrator)
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/detail/TSK-01-01")

    assert response.status_code == 200
    assert "TSK-01-01" in response.text


# TC-05: Worker API 응답 테스트
@pytest.mark.asyncio
async def test_workers_api() -> None:
    """Worker API가 상태 정보를 반환하는지 테스트."""
    from httpx import ASGITransport, AsyncClient

    from orchay.web.server import create_app

    mock_worker = Mock()
    mock_worker.id = 1
    mock_worker.pane_id = 1
    mock_worker.state = Mock(value="idle")
    mock_worker.current_task = None

    mock_orchestrator = Mock()
    mock_orchestrator.project_name = "test_project"
    mock_orchestrator.mode = Mock(value="quick")
    mock_orchestrator.tasks = []
    mock_orchestrator.workers = [mock_worker]

    app = create_app(mock_orchestrator)
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/workers")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


# TC-06: 존재하지 않는 Task 테스트
@pytest.mark.asyncio
async def test_detail_api_not_found() -> None:
    """존재하지 않는 Task 요청 시 404를 반환하는지 테스트."""
    from httpx import ASGITransport, AsyncClient

    from orchay.web.server import create_app

    mock_orchestrator = Mock()
    mock_orchestrator.project_name = "test_project"
    mock_orchestrator.mode = Mock(value="quick")
    mock_orchestrator.tasks = []
    mock_orchestrator.workers = []

    app = create_app(mock_orchestrator)
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/detail/INVALID-ID")

    assert response.status_code == 404
    assert "찾을 수 없습니다" in response.text
