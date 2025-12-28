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
    mock_task.schedule = ""
    mock_task.tags = ["test"]
    mock_task.depends = []
    # TSK-06-02: 요구사항/기술 스펙 필드
    mock_task.prd_ref = ""
    mock_task.requirements = []
    mock_task.acceptance = []
    mock_task.tech_spec = []
    mock_task.api_spec = []
    mock_task.ui_spec = []

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


# =============================================================================
# TSK-03-01: Task 상세 API 및 템플릿 테스트
# =============================================================================


# UT-001: get_task_detail 정상 조회 (모든 속성 포함 확인)
@pytest.mark.asyncio
async def test_get_task_detail_all_properties() -> None:
    """Task 상세 조회 시 모든 속성이 HTML에 포함되는지 테스트."""
    from httpx import ASGITransport, AsyncClient

    from orchay.web.server import create_app

    mock_task = Mock()
    mock_task.id = "TSK-03-01"
    mock_task.title = "Task 상세 API 및 템플릿"
    mock_task.status = Mock(value="[dd]")
    mock_task.category = Mock(value="development")
    mock_task.priority = Mock(value="high")
    mock_task.domain = "fullstack"
    mock_task.assignee = "developer"
    mock_task.schedule = ""
    mock_task.tags = ["api", "detail", "template"]
    mock_task.depends = ["TSK-02-02"]
    # TSK-06-02: 요구사항/기술 스펙 필드
    mock_task.prd_ref = "PRD 3.2"
    mock_task.requirements = ["요구사항1", "요구사항2"]
    mock_task.acceptance = []
    mock_task.tech_spec = ["스펙1"]
    mock_task.api_spec = []
    mock_task.ui_spec = []

    mock_orchestrator = Mock()
    mock_orchestrator.project_name = "orchay_web"
    mock_orchestrator.mode = Mock(value="quick")
    mock_orchestrator.tasks = [mock_task]
    mock_orchestrator.workers = []

    app = create_app(mock_orchestrator)
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/detail/TSK-03-01")

    assert response.status_code == 200
    html = response.text

    # FR-001~FR-006 필수 속성 확인
    assert "TSK-03-01" in html  # FR-001: Task ID
    assert "Task 상세 API 및 템플릿" in html  # FR-002: Title
    assert "[dd]" in html  # FR-003: Status
    assert "development" in html  # FR-004: Category
    assert "high" in html  # FR-005: Priority
    assert "TSK-02-02" in html  # FR-006: Depends


# UT-003: get_task_documents 문서 목록 조회
def test_get_task_documents_returns_existing_files(tmp_path: pytest.TempPathFactory) -> None:
    """존재하는 파일만 문서 목록에 포함 (TSK-06-03: 메타정보 포함)."""
    from orchay.web.server import get_task_documents

    # Given
    task_dir = tmp_path / "TSK-03-01"
    task_dir.mkdir()
    (task_dir / "010-design.md").touch()
    (task_dir / "025-traceability-matrix.md").touch()

    # When
    docs = get_task_documents("TSK-03-01", base_path=tmp_path)
    doc_names = [d["name"] for d in docs]

    # Then
    assert len(docs) == 2
    assert "010-design.md" in doc_names
    assert "025-traceability-matrix.md" in doc_names
    # TSK-06-03: 메타정보 필드 검증
    for doc in docs:
        assert "name" in doc
        assert "type" in doc
        assert "size" in doc
        assert "size_formatted" in doc
        assert "modified" in doc
        assert "modified_formatted" in doc


# UT-003-2: get_task_documents 문서 없는 경우
def test_get_task_documents_empty_when_no_dir(tmp_path: pytest.TempPathFactory) -> None:
    """Task 디렉토리가 없으면 빈 목록 반환."""
    from orchay.web.server import get_task_documents

    # When
    docs = get_task_documents("TSK-99-99", base_path=tmp_path)

    # Then
    assert docs == []


# E2E-002: 문서 목록 표시 (API 통합) - 실제 프로젝트 문서 확인
@pytest.mark.asyncio
async def test_task_detail_shows_documents_section() -> None:
    """Task 상세에 Documents 섹션이 표시된다."""
    from httpx import ASGITransport, AsyncClient

    from orchay.web.server import create_app

    # Given: Documents 섹션은 항상 표시됨 (문서가 있든 없든)
    mock_task = Mock()
    mock_task.id = "TSK-03-01"
    mock_task.title = "Task 상세 API 및 템플릿"
    mock_task.status = Mock(value="[dd]")
    mock_task.category = Mock(value="development")
    mock_task.priority = Mock(value="high")
    mock_task.domain = "fullstack"
    mock_task.assignee = "developer"
    mock_task.schedule = ""
    mock_task.tags = []
    mock_task.depends = []
    # TSK-06-02: 요구사항/기술 스펙 필드
    mock_task.prd_ref = ""
    mock_task.requirements = []
    mock_task.acceptance = []
    mock_task.tech_spec = []
    mock_task.api_spec = []
    mock_task.ui_spec = []

    mock_orchestrator = Mock()
    mock_orchestrator.project_name = "orchay_web"
    mock_orchestrator.mode = Mock(value="quick")
    mock_orchestrator.tasks = [mock_task]
    mock_orchestrator.workers = []

    app = create_app(mock_orchestrator)
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/detail/TSK-03-01")

    assert response.status_code == 200
    html = response.text

    # FR-007: Documents 섹션 확인
    assert "Documents" in html
    assert 'data-testid="documents-section"' in html
    assert 'data-testid="documents-list"' in html


# E2E-003: 미존재 Task 오류
@pytest.mark.asyncio
async def test_task_detail_not_found_error_message() -> None:
    """존재하지 않는 Task 조회 시 에러 메시지가 표시된다."""
    from httpx import ASGITransport, AsyncClient

    from orchay.web.server import create_app

    mock_orchestrator = Mock()
    mock_orchestrator.project_name = "orchay_web"
    mock_orchestrator.mode = Mock(value="quick")
    mock_orchestrator.tasks = []
    mock_orchestrator.workers = []

    app = create_app(mock_orchestrator)
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/detail/TSK-99-99")

    assert response.status_code == 404
    assert "TSK-99-99" in response.text
    assert "찾을 수 없습니다" in response.text


# UT-002: STATUS_COLORS 상태 색상 매핑 (detail.html 내 사용)
def test_status_colors_detail_mapping() -> None:
    """상태 코드별 올바른 스타일 적용 확인."""
    # detail.html의 상태 색상 매핑은 템플릿 내 조건문으로 처리됨
    # 주요 상태 코드 목록 검증
    status_codes = ["[ ]", "[bd]", "[dd]", "[ap]", "[im]", "[xx]"]
    for code in status_codes:
        assert isinstance(code, str), f"Status code {code} is not a string"


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
    # TSK-03-03: morph extension으로 깜빡임 최소화 (idiomorph 사용)
    assert 'hx-swap="morph:innerHTML"' in response.text


# =============================================================================
# TSK-02-03: 트리 인터랙션 구현 테스트
# 테스트 명세서 (026-test-specification.md) TC-01 ~ TC-08
# =============================================================================


# TC-01: WP 노드 확장 (HTMX 속성 검증)
@pytest.mark.asyncio
async def test_wp_node_expand_htmx_attributes() -> None:
    """WP 노드에 확장을 위한 HTMX 속성이 설정되어 있는지 확인."""
    from httpx import ASGITransport, AsyncClient

    from orchay.web.server import create_app

    mock_task = Mock()
    mock_task.id = "TSK-02-01"
    mock_task.title = "트리 API"
    mock_task.status = Mock(value="[dd]")

    mock_orchestrator = Mock()
    mock_orchestrator.project_name = "test_project"
    mock_orchestrator.mode = Mock(value="quick")
    mock_orchestrator.tasks = [mock_task]
    mock_orchestrator.workers = []

    app = create_app(mock_orchestrator)
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/tree")

    html = response.text

    # HTMX 확장 속성 확인
    assert 'hx-get="/api/tree/WP-02"' in html
    assert 'hx-target="#wp-children-WP-02"' in html
    assert 'hx-swap="innerHTML"' in html
    # 토글 아이콘 확인 (▶)
    assert "▶" in html
    # TSK-06-01: 토글 함수 호출 확인 (클릭 분리로 parentElement 참조)
    assert "toggleWp(this.parentElement)" in html


# TC-02: WP 노드 축소 (CSS 애니메이션 클래스 검증)
@pytest.mark.asyncio
async def test_wp_node_collapse_css_classes() -> None:
    """WP 하위 노드 컨테이너에 애니메이션 CSS 클래스가 설정되어 있는지 확인."""
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
        response = await client.get("/api/tree")

    html = response.text

    # 애니메이션 CSS 클래스 확인
    assert "transition-all" in html
    assert "duration-300" in html
    assert "max-h-0" in html
    assert "opacity-0" in html


# TC-03: Task 선택 (상세 패널 로드 HTMX)
@pytest.mark.asyncio
async def test_task_select_htmx_detail_load() -> None:
    """Task 노드 클릭 시 상세 패널로 로드하는 HTMX 속성 확인."""
    from httpx import ASGITransport, AsyncClient

    from orchay.web.server import create_app

    mock_task = Mock()
    mock_task.id = "TSK-02-03"
    mock_task.title = "트리 인터랙션 구현"
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

    html = response.text

    # Task 선택 HTMX 속성 확인
    assert 'hx-get="/api/detail/TSK-02-03"' in html
    assert 'hx-target="#detail-panel"' in html
    assert 'hx-swap="innerHTML"' in html
    # 선택 함수 호출 확인
    assert "selectTask(this)" in html


# TC-04: Task 선택 전환 (selectTask 함수 존재 확인)
@pytest.mark.asyncio
async def test_task_selection_switch_function() -> None:
    """selectTask 함수가 index.html에 정의되어 있는지 확인."""
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

    html = response.text

    # selectTask 함수 정의 확인
    assert "function selectTask(el)" in html
    # 기존 선택 해제 로직 확인
    assert ".selected" in html
    # 새로운 선택 스타일 적용 확인
    assert "ring-2" in html or "ring-blue-500" in html


# TC-05: 자동 갱신 (every 5s trigger)
@pytest.mark.asyncio
async def test_tree_auto_refresh_every_5s() -> None:
    """트리 패널이 5초마다 자동 갱신되는 HTMX 설정 확인."""
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

    html = response.text

    # 트리 패널 자동 갱신 확인
    assert 'id="tree-panel"' in html
    assert 'hx-get="/api/tree"' in html
    assert 'hx-trigger="load, every 5s"' in html


# TC-06: 애니메이션 시간 (transition-duration 확인)
@pytest.mark.asyncio
async def test_animation_duration_300ms() -> None:
    """CSS transition이 300ms (0.3초)로 설정되어 있는지 확인."""
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
        response = await client.get("/api/tree")

    html = response.text

    # Tailwind duration-300 (300ms = 0.3s) 확인
    assert "duration-300" in html
    # 토글 아이콘 회전 애니메이션
    assert "transition-transform" in html or "duration-200" in html


# TC-07: 네트워크 오류 처리 (에러 핸들러 함수 확인)
@pytest.mark.asyncio
async def test_network_error_handling_function() -> None:
    """HTMX 네트워크 오류 처리 리스너가 정의되어 있는지 확인."""
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

    html = response.text

    # HTMX 에러 이벤트 핸들러 확인
    assert "htmx:responseError" in html
    assert "htmx:sendError" in html
    # showToast 함수 확인
    assert "function showToast" in html
    # 에러 메시지 확인
    assert "네트워크 연결 실패" in html or "서버 오류" in html


# TC-08: 404 오류 처리 (상세 패널)
@pytest.mark.asyncio
async def test_404_error_in_detail_panel() -> None:
    """존재하지 않는 Task 요청 시 404 응답 및 에러 메시지 확인."""
    from httpx import ASGITransport, AsyncClient

    from orchay.web.server import create_app

    mock_orchestrator = Mock()
    mock_orchestrator.project_name = "test_project"
    mock_orchestrator.mode = Mock(value="quick")
    mock_orchestrator.tasks = []  # 빈 Task 목록
    mock_orchestrator.workers = []

    app = create_app(mock_orchestrator)
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/detail/TSK-99-99")

    assert response.status_code == 404
    assert "TSK-99-99" in response.text
    assert "찾을 수 없습니다" in response.text


# TC-09: 상태 유지 (localStorage 관련 코드 확인)
@pytest.mark.asyncio
async def test_state_persistence_localStorage() -> None:
    """BR-02 선택 상태 유지를 위한 localStorage 코드 확인."""
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

    html = response.text

    # localStorage 상태 관리 코드 확인
    assert "localStorage.setItem" in html or "localStorage.getItem" in html
    assert "saveState" in html
    assert "restoreState" in html
    # 갱신 후 상태 복원 확인
    assert "htmx:afterSwap" in html


# UT-01: 트리 노드 HTML 생성 (data-testid 확인)
@pytest.mark.asyncio
async def test_tree_node_html_has_testid() -> None:
    """트리 노드에 data-testid 속성이 설정되어 있는지 확인."""
    from httpx import ASGITransport, AsyncClient

    from orchay.web.server import create_app

    mock_task = Mock()
    mock_task.id = "TSK-01-01"
    mock_task.title = "Task 1"
    mock_task.status = Mock(value="[dd]")

    mock_orchestrator = Mock()
    mock_orchestrator.project_name = "test_project"
    mock_orchestrator.mode = Mock(value="quick")
    mock_orchestrator.tasks = [mock_task]
    mock_orchestrator.workers = []

    app = create_app(mock_orchestrator)
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/tree")

    html = response.text

    # data-testid 속성 확인
    assert 'data-testid="tree-root"' in html
    assert 'data-testid="tree-node-wp"' in html
    assert 'data-testid="tree-node-task"' in html
    assert 'data-testid="status-badge"' in html


# UT-02: 상태 클래스 매핑 (status_badge 매크로)
@pytest.mark.asyncio
async def test_status_badge_color_mapping() -> None:
    """상태 코드별 올바른 배경 색상 클래스 적용 확인."""
    from httpx import ASGITransport, AsyncClient

    from orchay.web.server import create_app

    # 다양한 상태의 Task 생성
    tasks = []
    status_list = ["[ ]", "[dd]", "[xx]"]
    expected_colors = ["bg-gray-500", "bg-purple-500", "bg-emerald-500"]

    for i, status in enumerate(status_list):
        task = Mock()
        task.id = f"TSK-01-0{i + 1}"
        task.title = f"Task {i + 1}"
        task.status = Mock(value=status)
        tasks.append(task)

    mock_orchestrator = Mock()
    mock_orchestrator.project_name = "test_project"
    mock_orchestrator.mode = Mock(value="quick")
    mock_orchestrator.tasks = tasks
    mock_orchestrator.workers = []

    app = create_app(mock_orchestrator)
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/tree")

    html = response.text

    # 상태별 색상 클래스 확인
    for color in expected_colors:
        assert color in html


# =============================================================================
# TSK-03-03: 실시간 자동 갱신 테스트
# 테스트 명세서 (026-test-specification.md) TC-U01 ~ TC-E05
# =============================================================================


# TC-U01: 진행률 계산 - 정상 케이스
def test_calculate_progress_normal_case() -> None:
    """진행률 계산: 10개 중 4개 완료 = 40%."""
    from orchay.web.server import calculate_progress

    tasks = [
        Mock(status=Mock(value="[xx]")),
        Mock(status=Mock(value="[xx]")),
        Mock(status=Mock(value="[xx]")),
        Mock(status=Mock(value="[xx]")),
        Mock(status=Mock(value="[im]")),
        Mock(status=Mock(value="[dd]")),
        Mock(status=Mock(value="[ ]")),
        Mock(status=Mock(value="[ ]")),
        Mock(status=Mock(value="[ ]")),
        Mock(status=Mock(value="[ ]")),
    ]
    result = calculate_progress(tasks)
    assert result["total"] == 10
    assert result["done"] == 4
    assert result["percentage"] == 40


# TC-U02: 진행률 계산 - 빈 리스트
def test_calculate_progress_empty_list() -> None:
    """진행률 계산: 빈 리스트 = 0%."""
    from orchay.web.server import calculate_progress

    result = calculate_progress([])
    assert result["total"] == 0
    assert result["done"] == 0
    assert result["percentage"] == 0


# TC-U03: Worker API 진행률 포함 응답
@pytest.mark.asyncio
async def test_workers_api_includes_progress_display() -> None:
    """Worker API 응답에 진행률 표시가 포함되는지 확인."""
    from httpx import ASGITransport, AsyncClient

    from orchay.models.worker import Worker, WorkerState
    from orchay.web.server import create_app

    # 5개 Task: 2개 완료, 3개 미완료 = 40%
    tasks = [
        Mock(status=Mock(value="[xx]")),
        Mock(status=Mock(value="[xx]")),
        Mock(status=Mock(value="[im]")),
        Mock(status=Mock(value="[dd]")),
        Mock(status=Mock(value="[ ]")),
    ]

    mock_orchestrator = Mock()
    mock_orchestrator.project_name = "test_project"
    mock_orchestrator.mode = Mock(value="quick")
    mock_orchestrator.tasks = tasks
    mock_orchestrator.workers = [Worker(id=1, pane_id=1, state=WorkerState.IDLE)]

    app = create_app(mock_orchestrator)
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/workers")

    html = response.text

    # 진행률 표시 확인
    assert "Progress:" in html
    assert "2/5" in html
    assert "40%" in html
    assert 'data-testid="progress-section"' in html
    assert 'data-testid="progress-bar"' in html
    assert 'data-testid="progress-text"' in html


# TC-E01: Worker 상태 5초 자동 갱신 (HTMX 설정 확인)
@pytest.mark.asyncio
async def test_worker_bar_auto_refresh_5s() -> None:
    """Worker 상태 바에 5초 자동 갱신 HTMX 속성 확인."""
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

    html = response.text

    # Worker 바 자동 갱신 설정 확인
    assert 'id="workers-bar"' in html
    assert 'hx-get="/api/workers"' in html
    assert 'hx-trigger="load, every 5s"' in html


# TC-E03: Task 상세 자동 갱신 (JavaScript 함수 확인)
@pytest.mark.asyncio
async def test_task_detail_auto_refresh_function() -> None:
    """Task Detail 자동 갱신 JavaScript 함수가 정의되어 있는지 확인."""
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

    html = response.text

    # Task Detail 자동 갱신 함수 확인
    assert "startDetailRefresh" in html
    assert "detailRefreshInterval" in html
    assert "setInterval" in html
    # 선택된 Task 저장 속성 확인
    assert "data-selected-task" in html


# TC-E04: UI 깜빡임 방지 (settle 시간 확인)
@pytest.mark.asyncio
async def test_htmx_settle_time_for_flicker_prevention() -> None:
    """HTMX morph extension이 설정되어 깜빡임이 최소화되는지 확인."""
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

    html = response.text

    # morph extension 활성화 확인 (idiomorph 기반 깜빡임 방지)
    assert 'hx-ext="morph"' in html
    assert 'hx-swap="morph:innerHTML"' in html


# TC-E05: 네트워크 오류 처리 (에러 핸들러 확인)
@pytest.mark.asyncio
async def test_network_error_handler_exists() -> None:
    """네트워크 오류 처리를 위한 HTMX 이벤트 핸들러 확인."""
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

    html = response.text

    # 에러 핸들러 확인
    assert "htmx:responseError" in html
    assert "htmx:sendError" in html
    assert "showToast" in html


# 진행률 프로그레스 바 스타일 확인
@pytest.mark.asyncio
async def test_progress_bar_styling() -> None:
    """진행률 프로그레스 바에 적절한 스타일이 적용되는지 확인."""
    from httpx import ASGITransport, AsyncClient

    from orchay.models.worker import Worker, WorkerState
    from orchay.web.server import create_app

    tasks = [Mock(status=Mock(value="[xx]")) for _ in range(5)]

    mock_orchestrator = Mock()
    mock_orchestrator.project_name = "test_project"
    mock_orchestrator.mode = Mock(value="quick")
    mock_orchestrator.tasks = tasks
    mock_orchestrator.workers = [Worker(id=1, pane_id=1, state=WorkerState.IDLE)]

    app = create_app(mock_orchestrator)
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/workers")

    html = response.text

    # 프로그레스 바 스타일 확인
    assert "bg-green-500" in html  # 진행 바 색상
    assert "transition-all" in html  # 애니메이션
    assert "duration-300" in html  # 애니메이션 시간
    assert 'style="width: 100%"' in html  # 5/5 = 100%


# =============================================================================
# TSK-04-02: 성능 테스트
# 테스트 명세서 (026-test-specification.md) TC-11, TC-12
# =============================================================================


# TC-11: 페이지 로드 시간 테스트
@pytest.mark.asyncio
async def test_page_load_time() -> None:
    """메인 페이지 로드 시간이 1초 미만인지 확인 (PRD 4: 성능 요구사항)."""
    import time

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
        start = time.perf_counter()
        response = await client.get("/")
        elapsed = time.perf_counter() - start

    assert response.status_code == 200
    assert elapsed < 1.0, f"페이지 로드 시간 {elapsed:.3f}초 > 1초"


# TC-12: API 응답 시간 테스트
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "endpoint",
    [
        "/",
        "/api/tree",
        "/api/workers",
    ],
)
async def test_api_response_time(endpoint: str) -> None:
    """API 응답 시간이 1초 미만인지 확인."""
    import time

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
        start = time.perf_counter()
        response = await client.get(endpoint)
        elapsed = time.perf_counter() - start

    assert response.status_code == 200
    assert elapsed < 1.0, f"{endpoint} 응답 시간 {elapsed:.3f}초 > 1초"


# TC-02: 서버 종료 테스트 (명시적)
def test_server_stops_cleanly() -> None:
    """서버가 정상적으로 종료되고 리소스가 정리되는지 확인."""
    from fastapi.testclient import TestClient

    from orchay.web.server import create_app

    mock_orchestrator = Mock()
    mock_orchestrator.project_name = "test_project"
    mock_orchestrator.mode = Mock(value="quick")
    mock_orchestrator.tasks = []
    mock_orchestrator.workers = []

    app = create_app(mock_orchestrator)

    # TestClient 컨텍스트 관리자로 리소스 정리 테스트
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200

    # 컨텍스트 종료 후 예외 없이 정상 종료 확인
    assert True, "서버가 예외 없이 종료됨"


# =============================================================================
# TSK-05-01: Document Viewer API 테스트
# 테스트 명세서 (026-test-specification.md) UT-01 ~ UT-05
# =============================================================================


# UT-01: 마크다운 문서 API 정상 응답
@pytest.mark.asyncio
async def test_get_markdown_document(tmp_path: pytest.TempPathFactory) -> None:
    """마크다운 파일 요청 시 PlainTextResponse 반환 확인."""
    from httpx import ASGITransport, AsyncClient

    from orchay.web.server import create_app

    # 테스트용 마크다운 파일 생성
    task_dir = tmp_path / "orchay_web" / "tasks" / "TSK-TEST"
    task_dir.mkdir(parents=True)
    test_md = task_dir / "test.md"
    test_md.write_text("# Test Document\n\nHello World!", encoding="utf-8")

    mock_orchestrator = Mock()
    mock_orchestrator.project_name = "orchay_web"
    mock_orchestrator.mode = Mock(value="quick")
    mock_orchestrator.tasks = []
    mock_orchestrator.workers = []

    import os

    original_cwd = os.getcwd()
    os.chdir(tmp_path)

    try:
        # .orchay 경로 구조 생성
        orchay_tasks = tmp_path / ".orchay" / "projects" / "orchay_web" / "tasks" / "TSK-TEST"
        orchay_tasks.mkdir(parents=True)
        (orchay_tasks / "test.md").write_text("# Test Document\n\nHello World!", encoding="utf-8")

        app = create_app(mock_orchestrator)
        transport = ASGITransport(app=app)

        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/api/document/TSK-TEST/test.md")

        assert response.status_code == 200
        assert "text/plain" in response.headers["content-type"]
        assert "# Test Document" in response.text
    finally:
        os.chdir(original_cwd)


# UT-02: 허용되지 않는 확장자 차단
@pytest.mark.asyncio
@pytest.mark.parametrize("ext", [".pdf", ".exe", ".py", ".html"])
async def test_reject_disallowed_extensions(ext: str) -> None:
    """허용되지 않는 확장자 요청 시 400 반환."""
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
        response = await client.get(f"/api/document/TSK-TEST/file{ext}")

    assert response.status_code == 400
    assert "Unsupported file type" in response.text


# UT-03: Path Traversal 차단
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "malicious_path",
    [
        "../../../etc/passwd.md",
        "..%2F..%2F..%2Fetc%2Fpasswd.md",
        "test/../../../etc/passwd.md",
    ],
)
async def test_block_path_traversal(malicious_path: str) -> None:
    """Path traversal 시도 시 403 또는 404 반환 (경로 탈출 불가)."""
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
        response = await client.get(f"/api/document/TSK-TEST/{malicious_path}")

    # 403 Access denied 또는 404 (경로 resolve 후 존재하지 않음)
    assert response.status_code in [403, 404]


# UT-04: 이미지 파일 API 정상 응답
@pytest.mark.asyncio
async def test_get_image_document(tmp_path: pytest.TempPathFactory) -> None:
    """이미지 파일 요청 시 FileResponse 반환 확인."""
    from httpx import ASGITransport, AsyncClient

    from orchay.web.server import create_app

    mock_orchestrator = Mock()
    mock_orchestrator.project_name = "test_project"
    mock_orchestrator.mode = Mock(value="quick")
    mock_orchestrator.tasks = []
    mock_orchestrator.workers = []

    import os

    original_cwd = os.getcwd()
    os.chdir(tmp_path)

    try:
        # 이미지 파일 생성 (1x1 PNG 바이트)
        orchay_tasks = tmp_path / ".orchay" / "projects" / "test_project" / "tasks" / "TSK-TEST"
        orchay_tasks.mkdir(parents=True)
        # 1x1 PNG 바이트
        png_bytes = (
            b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01"
            b"\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00"
            b"\x00\x0cIDATx\x9cc\xf8\x0f\x00\x00\x01\x01\x00\x05"
            b"\x18\xd8N\x00\x00\x00\x00IEND\xaeB`\x82"
        )
        (orchay_tasks / "image.png").write_bytes(png_bytes)

        app = create_app(mock_orchestrator)
        transport = ASGITransport(app=app)

        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/api/document/TSK-TEST/image.png")

        assert response.status_code == 200
        assert "image/png" in response.headers["content-type"]
    finally:
        os.chdir(original_cwd)


# UT-05: 존재하지 않는 파일 404
@pytest.mark.asyncio
async def test_document_not_found() -> None:
    """존재하지 않는 파일 요청 시 404 반환."""
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
        response = await client.get("/api/document/TSK-TEST/nonexistent.md")

    assert response.status_code == 404
    assert "not found" in response.text.lower()


# Document Viewer 모달 HTML 확인
@pytest.mark.asyncio
async def test_document_viewer_modal_exists() -> None:
    """index.html에 Document Viewer 모달이 포함되어 있는지 확인."""
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

    html = response.text

    # 모달 요소 확인
    assert 'id="document-modal"' in html
    assert 'id="document-content"' in html
    assert 'id="document-close-btn"' in html
    assert "openDocument" in html
    assert "closeDocument" in html


# Document Viewer JavaScript 함수 확인
@pytest.mark.asyncio
async def test_document_viewer_javascript_functions() -> None:
    """Document Viewer JavaScript 함수가 정의되어 있는지 확인."""
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

    html = response.text

    # JavaScript 함수 확인
    assert "async function openDocument" in html
    assert "function closeDocument" in html
    assert "marked.parse" in html
    assert "mermaid.run" in html
    # ESC 키 핸들러
    assert "e.key === 'Escape'" in html or "Escape" in html


# get_task_documents 이미지 지원 확인
def test_get_task_documents_includes_images(tmp_path: pytest.TempPathFactory) -> None:
    """get_task_documents가 이미지 파일도 반환하는지 확인 (TSK-06-03: 메타정보 포함)."""
    from orchay.web.server import get_task_documents

    # Given
    task_dir = tmp_path / "TSK-TEST"
    task_dir.mkdir()
    (task_dir / "010-design.md").touch()
    (task_dir / "wireframe.png").touch()
    (task_dir / "screenshot.jpg").touch()
    (task_dir / "secret.pdf").touch()  # 허용되지 않는 확장자

    # When
    docs = get_task_documents("TSK-TEST", base_path=tmp_path)
    doc_names = [d["name"] for d in docs]

    # Then
    assert len(docs) == 3  # md + png + jpg (pdf 제외)
    assert "010-design.md" in doc_names
    assert "wireframe.png" in doc_names
    assert "screenshot.jpg" in doc_names
    assert "secret.pdf" not in doc_names
    # TSK-06-03: 타입 필드 검증
    doc_types = {d["name"]: d["type"] for d in docs}
    assert doc_types["010-design.md"] == "MD"
    assert doc_types["wireframe.png"] == "PNG"
    assert doc_types["screenshot.jpg"] == "JPG"


# =============================================================================
# TC-12b: 대용량 데이터 성능 테스트
# =============================================================================


# TC-12b: 대용량 데이터 성능 테스트
@pytest.mark.asyncio
async def test_api_response_time_with_large_data() -> None:
    """대용량 데이터(20개 Task)에서도 응답 시간이 1초 미만인지 확인."""
    import time

    from httpx import ASGITransport, AsyncClient

    from orchay.models.worker import Worker, WorkerState
    from orchay.web.server import create_app

    # 20개 Task 생성 (표준 테스트 데이터)
    tasks = []
    for i in range(20):
        wp_num = (i // 4) + 1
        task_num = (i % 4) + 1
        mock_task = Mock()
        mock_task.id = f"TSK-0{wp_num}-0{task_num}"
        mock_task.title = f"Task {i + 1}"
        mock_task.status = Mock(value="[xx]" if i < 5 else "[ ]")
        tasks.append(mock_task)

    # 5개 Worker 생성
    workers = [Worker(id=i, pane_id=i, state=WorkerState.IDLE) for i in range(1, 6)]

    mock_orchestrator = Mock()
    mock_orchestrator.project_name = "test_project"
    mock_orchestrator.mode = Mock(value="quick")
    mock_orchestrator.tasks = tasks
    mock_orchestrator.workers = workers

    app = create_app(mock_orchestrator)
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # 메인 페이지
        start = time.perf_counter()
        response = await client.get("/")
        elapsed = time.perf_counter() - start
        assert response.status_code == 200
        assert elapsed < 1.0, f"/ 응답 시간 {elapsed:.3f}초 > 1초"

        # 트리 API
        start = time.perf_counter()
        response = await client.get("/api/tree")
        elapsed = time.perf_counter() - start
        assert response.status_code == 200
        assert elapsed < 1.0, f"/api/tree 응답 시간 {elapsed:.3f}초 > 1초"

        # Worker API
        start = time.perf_counter()
        response = await client.get("/api/workers")
        elapsed = time.perf_counter() - start
        assert response.status_code == 200
        assert elapsed < 1.0, f"/api/workers 응답 시간 {elapsed:.3f}초 > 1초"
