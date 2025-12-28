"""FastAPI 웹 서버 테스트.

TSK-01-01: FastAPI 앱 및 라우트 정의 테스트
TSK-02-01: 트리 데이터 API 테스트
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


# =============================================================================
# TSK-02-01: 트리 데이터 API 테스트
# =============================================================================


# TC-02-01: WP 하위 노드 API 정상 응답
@pytest.mark.asyncio
async def test_get_wp_children() -> None:
    """GET /api/tree/{wp_id} 요청 시 해당 WP의 하위 노드만 반환."""
    from httpx import ASGITransport, AsyncClient

    from orchay.web.server import create_app

    # WP-01과 WP-02에 각각 Task 생성
    mock_task1 = Mock()
    mock_task1.id = "TSK-01-01"
    mock_task1.title = "Task 1"
    mock_task1.status = Mock(value="[ ]")

    mock_task2 = Mock()
    mock_task2.id = "TSK-02-01"
    mock_task2.title = "트리 API"
    mock_task2.status = Mock(value="[bd]")

    mock_task3 = Mock()
    mock_task3.id = "TSK-02-02"
    mock_task3.title = "트리 템플릿"
    mock_task3.status = Mock(value="[ ]")

    mock_orchestrator = Mock()
    mock_orchestrator.project_name = "test_project"
    mock_orchestrator.mode = Mock(value="quick")
    mock_orchestrator.tasks = [mock_task1, mock_task2, mock_task3]
    mock_orchestrator.workers = []

    app = create_app(mock_orchestrator)
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/tree/WP-02")

    assert response.status_code == 200
    assert "TSK-02-01" in response.text
    assert "TSK-02-02" in response.text
    # WP-01 Task는 포함되지 않음
    assert "TSK-01-01" not in response.text


# TC-02-05: 존재하지 않는 WP 404 응답
@pytest.mark.asyncio
async def test_get_invalid_wp_returns_404() -> None:
    """존재하지 않는 WP 요청 시 404 반환."""
    from httpx import ASGITransport, AsyncClient

    from orchay.web.server import create_app

    mock_task = Mock()
    mock_task.id = "TSK-01-01"
    mock_task.title = "Task 1"
    mock_task.status = Mock(value="[ ]")

    mock_orchestrator = Mock()
    mock_orchestrator.project_name = "test_project"
    mock_orchestrator.mode = Mock(value="quick")
    mock_orchestrator.tasks = [mock_task]
    mock_orchestrator.workers = []

    app = create_app(mock_orchestrator)
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/tree/WP-99")

    assert response.status_code == 404
    assert "찾을 수 없습니다" in response.text


# TC-02-03: 트리 구조에 진행률 포함
@pytest.mark.asyncio
async def test_tree_includes_progress() -> None:
    """트리 API 응답에 진행률이 포함되는지 테스트."""
    from httpx import ASGITransport, AsyncClient

    from orchay.web.server import create_app

    # 2개 완료, 2개 미완료 = 50%
    mock_task1 = Mock()
    mock_task1.id = "TSK-01-01"
    mock_task1.title = "Task 1"
    mock_task1.status = Mock(value="[xx]")

    mock_task2 = Mock()
    mock_task2.id = "TSK-01-02"
    mock_task2.title = "Task 2"
    mock_task2.status = Mock(value="[xx]")

    mock_task3 = Mock()
    mock_task3.id = "TSK-01-03"
    mock_task3.title = "Task 3"
    mock_task3.status = Mock(value="[im]")

    mock_task4 = Mock()
    mock_task4.id = "TSK-01-04"
    mock_task4.title = "Task 4"
    mock_task4.status = Mock(value="[ ]")

    mock_orchestrator = Mock()
    mock_orchestrator.project_name = "test_project"
    mock_orchestrator.mode = Mock(value="quick")
    mock_orchestrator.tasks = [mock_task1, mock_task2, mock_task3, mock_task4]
    mock_orchestrator.workers = []

    app = create_app(mock_orchestrator)
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/tree")

    assert response.status_code == 200
    # 진행률 표시 확인 (50%)
    assert "50%" in response.text


# TC-02-04: 진행률 계산 함수 테스트
def test_calculate_progress() -> None:
    """calculate_progress 함수 테스트."""
    from orchay.web.tree import calculate_progress

    # 2/4 = 50%
    tasks_50 = [
        Mock(status=Mock(value="[xx]")),
        Mock(status=Mock(value="[xx]")),
        Mock(status=Mock(value="[im]")),
        Mock(status=Mock(value="[ ]")),
    ]
    assert calculate_progress(tasks_50) == 50.0


def test_calculate_progress_empty() -> None:
    """빈 목록의 진행률은 0."""
    from orchay.web.tree import calculate_progress

    assert calculate_progress([]) == 0.0


def test_calculate_progress_all_complete() -> None:
    """모두 완료 시 100%."""
    from orchay.web.tree import calculate_progress

    tasks = [
        Mock(status=Mock(value="[xx]")),
        Mock(status=Mock(value="[xx]")),
    ]
    assert calculate_progress(tasks) == 100.0
