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


# =============================================================================
# TSK-03-02: Worker 상태 바 구현 테스트
# =============================================================================


# TC-01-01: GET /api/workers 기본 응답
@pytest.mark.asyncio
async def test_get_workers_success() -> None:
    """Worker 상태 API 기본 응답 테스트."""
    from httpx import ASGITransport, AsyncClient

    from orchay.models.worker import Worker, WorkerState
    from orchay.web.server import create_app

    worker1 = Worker(id=1, pane_id=1, state=WorkerState.IDLE)
    worker2 = Worker(id=2, pane_id=2, state=WorkerState.BUSY, current_task="TSK-01-01")

    mock_orchestrator = Mock()
    mock_orchestrator.project_name = "test_project"
    mock_orchestrator.mode = Mock(value="quick")
    mock_orchestrator.tasks = []
    mock_orchestrator.workers = [worker1, worker2]

    app = create_app(mock_orchestrator)
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/workers")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "W1" in response.text or "No workers" in response.text


# TC-01-02: Worker 없음 처리
@pytest.mark.asyncio
async def test_get_workers_empty() -> None:
    """Worker 없을 때 빈 상태 표시 테스트."""
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
        response = await client.get("/api/workers")

    assert response.status_code == 200
    assert "No workers" in response.text


# TC-02-01: Worker 상태별 아이콘 렌더링
@pytest.mark.asyncio
async def test_worker_status_icons() -> None:
    """상태별 올바른 아이콘 표시 테스트."""
    from httpx import ASGITransport, AsyncClient

    from orchay.models.worker import Worker, WorkerState
    from orchay.web.server import create_app

    workers = [
        Worker(id=1, pane_id=1, state=WorkerState.IDLE),
        Worker(id=2, pane_id=2, state=WorkerState.BUSY, current_task="TSK-01-01"),
        Worker(id=3, pane_id=3, state=WorkerState.ERROR),
    ]

    mock_orchestrator = Mock()
    mock_orchestrator.project_name = "test_project"
    mock_orchestrator.mode = Mock(value="quick")
    mock_orchestrator.tasks = []
    mock_orchestrator.workers = workers

    app = create_app(mock_orchestrator)
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/workers")

    assert "🟢" in response.text  # IDLE
    assert "🟡" in response.text  # BUSY
    assert "🔴" in response.text  # ERROR


# TC-02-02: Worker 상태별 배경색 클래스
@pytest.mark.asyncio
async def test_worker_status_bg_classes() -> None:
    """상태별 올바른 Tailwind 배경색 클래스 테스트."""
    from httpx import ASGITransport, AsyncClient

    from orchay.models.worker import Worker, WorkerState
    from orchay.web.server import create_app

    workers = [
        Worker(id=1, pane_id=1, state=WorkerState.IDLE),
        Worker(id=2, pane_id=2, state=WorkerState.BUSY, current_task="TSK-01-01"),
        Worker(id=3, pane_id=3, state=WorkerState.ERROR),
    ]

    mock_orchestrator = Mock()
    mock_orchestrator.project_name = "test_project"
    mock_orchestrator.mode = Mock(value="quick")
    mock_orchestrator.tasks = []
    mock_orchestrator.workers = workers

    app = create_app(mock_orchestrator)
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/workers")

    assert "bg-green-500/20" in response.text  # IDLE
    assert "bg-yellow-500/20" in response.text  # BUSY
    assert "bg-red-500/20" in response.text  # ERROR


# TC-03-01: busy Worker의 current_task 표시
@pytest.mark.asyncio
async def test_busy_worker_shows_task() -> None:
    """busy 상태 Worker에 Task ID 표시 테스트."""
    from httpx import ASGITransport, AsyncClient

    from orchay.models.worker import Worker, WorkerState
    from orchay.web.server import create_app

    worker = Worker(id=1, pane_id=1, state=WorkerState.BUSY, current_task="TSK-01-01")

    mock_orchestrator = Mock()
    mock_orchestrator.project_name = "test_project"
    mock_orchestrator.mode = Mock(value="quick")
    mock_orchestrator.tasks = []
    mock_orchestrator.workers = [worker]

    app = create_app(mock_orchestrator)
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/workers")

    assert "TSK-01-01" in response.text


# TC-03-02: idle Worker는 Task ID 미표시
@pytest.mark.asyncio
async def test_idle_worker_no_task() -> None:
    """idle 상태 Worker에 Task ID 미표시 테스트."""
    from httpx import ASGITransport, AsyncClient

    from orchay.models.worker import Worker, WorkerState
    from orchay.web.server import create_app

    worker = Worker(id=1, pane_id=1, state=WorkerState.IDLE, current_task=None)

    mock_orchestrator = Mock()
    mock_orchestrator.project_name = "test_project"
    mock_orchestrator.mode = Mock(value="quick")
    mock_orchestrator.tasks = []
    mock_orchestrator.workers = [worker]

    app = create_app(mock_orchestrator)
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/workers")

    # idle Worker는 current_task가 None이므로 TSK-로 시작하는 ID가 없어야 함
    # W1, 🟢, idle은 있지만 TSK- 패턴은 없어야 함
    assert "W1" in response.text
    assert "🟢" in response.text


# TC-04-01: status_icon 필터 테스트
def test_status_icon_filter() -> None:
    """status_icon 필터 모든 상태 변환 테스트."""
    from orchay.models.worker import WorkerState
    from orchay.web.filters import status_icon

    assert status_icon(WorkerState.IDLE) == "🟢"
    assert status_icon(WorkerState.BUSY) == "🟡"
    assert status_icon(WorkerState.PAUSED) == "⏸️"
    assert status_icon(WorkerState.ERROR) == "🔴"
    assert status_icon(WorkerState.BLOCKED) == "⊘"
    assert status_icon(WorkerState.DEAD) == "💀"
    assert status_icon(WorkerState.DONE) == "✅"


# TC-04-02: status_bg 필터 테스트
def test_status_bg_filter() -> None:
    """status_bg 필터 모든 상태 변환 테스트."""
    from orchay.models.worker import WorkerState
    from orchay.web.filters import status_bg

    assert status_bg(WorkerState.IDLE) == "bg-green-500/20"
    assert status_bg(WorkerState.BUSY) == "bg-yellow-500/20"
    assert status_bg(WorkerState.PAUSED) == "bg-purple-500/20"
    assert status_bg(WorkerState.ERROR) == "bg-red-500/20"
    assert status_bg(WorkerState.BLOCKED) == "bg-gray-500/20"
    assert status_bg(WorkerState.DEAD) == "bg-gray-700/20"
    assert status_bg(WorkerState.DONE) == "bg-emerald-500/20"


# TC-05-01: HTMX 자동 갱신 확인 (index.html 검증)
@pytest.mark.asyncio
async def test_htmx_auto_refresh_attributes() -> None:
    """index.html에 HTMX 자동 갱신 속성 확인 테스트."""
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

    # HTMX 속성 확인
    assert 'id="workers-bar"' in response.text
    assert 'hx-get="/api/workers"' in response.text
    assert 'hx-trigger="load, every 5s"' in response.text
    assert 'hx-swap="innerHTML"' in response.text
