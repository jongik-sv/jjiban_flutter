"""트리 API, 트리 구조 변환 및 트리 템플릿 테스트.

TSK-02-01: 트리 데이터 API 테스트
TSK-02-02: 트리 템플릿 구현 테스트
"""

from unittest.mock import Mock

import pytest
from httpx import ASGITransport, AsyncClient

from orchay.models import Task, TaskCategory, TaskPriority, TaskStatus


# ============================================================================
# TC-01: 전체 트리 API 정상 응답
# ============================================================================
@pytest.mark.asyncio
async def test_get_tree_returns_html() -> None:
    """GET /api/tree 요청 시 HTML 트리 반환."""
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
    # 트리 노드 구조가 포함되어야 함
    assert "tree-node" in response.text or "WP-01" in response.text


@pytest.mark.asyncio
async def test_get_tree_with_multiple_tasks() -> None:
    """여러 Task가 있을 때 WP별로 그룹화되어 반환."""
    from orchay.web.server import create_app

    mock_tasks = []
    for i, (task_id, status_code) in enumerate(
        [
            ("TSK-01-01", "[ ]"),
            ("TSK-01-02", "[bd]"),
            ("TSK-02-01", "[dd]"),
            ("TSK-02-02", "[xx]"),
        ]
    ):
        task = Mock()
        task.id = task_id
        task.title = f"Test Task {i}"
        task.status = Mock(value=status_code)
        mock_tasks.append(task)

    mock_orchestrator = Mock()
    mock_orchestrator.project_name = "test_project"
    mock_orchestrator.mode = Mock(value="quick")
    mock_orchestrator.tasks = mock_tasks
    mock_orchestrator.workers = []

    app = create_app(mock_orchestrator)
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/tree")

    assert response.status_code == 200
    # WP-01, WP-02 모두 포함
    assert "WP-01" in response.text
    assert "WP-02" in response.text


# ============================================================================
# TC-02: WP 하위 노드 API 정상 응답
# ============================================================================
@pytest.mark.asyncio
async def test_get_wp_children() -> None:
    """GET /api/tree/{wp_id} 요청 시 하위 노드 반환."""
    from orchay.web.server import create_app

    mock_tasks = []
    for task_id, status_code in [
        ("TSK-01-01", "[ ]"),
        ("TSK-02-01", "[bd]"),
        ("TSK-02-02", "[dd]"),
    ]:
        task = Mock()
        task.id = task_id
        task.title = f"Task {task_id}"
        task.status = Mock(value=status_code)
        mock_tasks.append(task)

    mock_orchestrator = Mock()
    mock_orchestrator.project_name = "test_project"
    mock_orchestrator.mode = Mock(value="quick")
    mock_orchestrator.tasks = mock_tasks
    mock_orchestrator.workers = []

    app = create_app(mock_orchestrator)
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/tree/WP-02")

    assert response.status_code == 200
    # WP-02의 하위 Task만 포함
    assert "TSK-02-01" in response.text
    assert "TSK-02-02" in response.text
    # WP-01의 Task는 포함되지 않아야 함
    assert "TSK-01-01" not in response.text


# ============================================================================
# TC-03: 트리 구조 변환 정확성
# ============================================================================
def test_build_tree_structure() -> None:
    """Task 목록이 WP/ACT/TSK 계층으로 변환됨."""
    from orchay.web.tree import build_tree

    tasks = [
        Task(
            id="TSK-01-01",
            title="Task 1",
            category=TaskCategory.DEVELOPMENT,
            status=TaskStatus.TODO,
            priority=TaskPriority.MEDIUM,
        ),
        Task(
            id="TSK-01-02",
            title="Task 2",
            category=TaskCategory.DEVELOPMENT,
            status=TaskStatus.BASIC_DESIGN,
            priority=TaskPriority.HIGH,
        ),
        Task(
            id="TSK-02-01",
            title="Task 3",
            category=TaskCategory.DEVELOPMENT,
            status=TaskStatus.DETAIL_DESIGN,
            priority=TaskPriority.MEDIUM,
        ),
    ]
    tree = build_tree(tasks)

    # WP-01, WP-02 두 개의 WP 노드
    assert len(tree) == 2
    assert tree[0].id == "WP-01"
    assert tree[1].id == "WP-02"

    # WP-01 하위에 2개 Task
    assert len(tree[0].children) == 2
    # WP-02 하위에 1개 Task
    assert len(tree[1].children) == 1


def test_build_tree_empty() -> None:
    """빈 Task 목록은 빈 트리 반환."""
    from orchay.web.tree import build_tree

    tree = build_tree([])
    assert len(tree) == 0


def test_build_tree_with_4level_task() -> None:
    """4레벨 Task ID (TSK-XX-XX-XX)도 올바르게 처리."""
    from orchay.web.tree import build_tree

    tasks = [
        Task(
            id="TSK-01-01-01",
            title="4Level Task",
            category=TaskCategory.DEVELOPMENT,
            status=TaskStatus.TODO,
            priority=TaskPriority.MEDIUM,
        ),
        Task(
            id="TSK-01-01-02",
            title="4Level Task 2",
            category=TaskCategory.DEVELOPMENT,
            status=TaskStatus.TODO,
            priority=TaskPriority.MEDIUM,
        ),
    ]
    tree = build_tree(tasks)

    assert len(tree) == 1
    assert tree[0].id == "WP-01"
    # ACT-01-01 하위에 2개 Task
    assert len(tree[0].children) == 1  # ACT-01-01
    assert tree[0].children[0].id == "ACT-01-01"
    assert len(tree[0].children[0].children) == 2


# ============================================================================
# TC-04: 진행률 계산 정확성
# ============================================================================
def test_calculate_progress() -> None:
    """WP 진행률이 하위 Task 완료 비율로 계산됨."""
    from orchay.web.tree import calculate_progress

    tasks = [
        Task(
            id="TSK-01-01",
            title="T1",
            category=TaskCategory.DEVELOPMENT,
            status=TaskStatus.DONE,
            priority=TaskPriority.MEDIUM,
        ),  # 완료
        Task(
            id="TSK-01-02",
            title="T2",
            category=TaskCategory.DEVELOPMENT,
            status=TaskStatus.DONE,
            priority=TaskPriority.MEDIUM,
        ),  # 완료
        Task(
            id="TSK-01-03",
            title="T3",
            category=TaskCategory.DEVELOPMENT,
            status=TaskStatus.IMPLEMENT,
            priority=TaskPriority.MEDIUM,
        ),  # 미완료
        Task(
            id="TSK-01-04",
            title="T4",
            category=TaskCategory.DEVELOPMENT,
            status=TaskStatus.TODO,
            priority=TaskPriority.MEDIUM,
        ),  # 미완료
    ]
    progress = calculate_progress(tasks)
    assert progress == 50.0  # 2/4 = 50%


def test_calculate_progress_empty() -> None:
    """빈 목록은 0% 반환."""
    from orchay.web.tree import calculate_progress

    progress = calculate_progress([])
    assert progress == 0.0


def test_calculate_progress_all_complete() -> None:
    """모든 Task 완료 시 100% 반환."""
    from orchay.web.tree import calculate_progress

    tasks = [
        Task(
            id="TSK-01-01",
            title="T1",
            category=TaskCategory.DEVELOPMENT,
            status=TaskStatus.DONE,
            priority=TaskPriority.MEDIUM,
        ),
        Task(
            id="TSK-01-02",
            title="T2",
            category=TaskCategory.DEVELOPMENT,
            status=TaskStatus.DONE,
            priority=TaskPriority.MEDIUM,
        ),
    ]
    progress = calculate_progress(tasks)
    assert progress == 100.0


# ============================================================================
# TC-05: 존재하지 않는 WP 404 응답
# ============================================================================
@pytest.mark.asyncio
async def test_get_invalid_wp_returns_404() -> None:
    """존재하지 않는 WP 요청 시 404 반환."""
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
        response = await client.get("/api/tree/WP-99")

    assert response.status_code == 404
    assert "찾을 수 없습니다" in response.text


# ============================================================================
# TSK-02-02: 트리 템플릿 테스트
# ============================================================================


# UT-001: 노드 타입별 렌더링
@pytest.mark.asyncio
async def test_tree_template_renders_wp_node() -> None:
    """WP 노드가 올바른 구조로 렌더링됨 (UT-001)."""
    from orchay.web.server import create_app

    mock_task = Mock()
    mock_task.id = "TSK-01-01"
    mock_task.title = "Test Task"
    mock_task.status = Mock(value="[ ]")

    mock_orchestrator = Mock()
    mock_orchestrator.project_name = "test"
    mock_orchestrator.mode = Mock(value="quick")
    mock_orchestrator.tasks = [mock_task]
    mock_orchestrator.workers = []

    app = create_app(mock_orchestrator)
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/tree")

    assert response.status_code == 200
    # WP 노드 구조 확인
    assert 'data-type="wp"' in response.text
    assert 'data-testid="tree-node-wp"' in response.text
    assert "text-blue-400" in response.text  # WP 아이콘 색상


# UT-002: 상태 색상 매핑
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "status_code,expected_color",
    [
        ("[ ]", "bg-gray-500"),
        ("[bd]", "bg-blue-500"),
        ("[dd]", "bg-purple-500"),
        ("[an]", "bg-indigo-500"),
        ("[ds]", "bg-cyan-500"),
        ("[ap]", "bg-green-500"),
        ("[im]", "bg-yellow-500"),
        ("[fx]", "bg-orange-500"),
        ("[vf]", "bg-teal-500"),
        ("[xx]", "bg-emerald-500"),
    ],
)
async def test_status_color_mapping(status_code: str, expected_color: str) -> None:
    """상태 코드별 올바른 색상 클래스 반환 (UT-002)."""
    from orchay.web.server import create_app

    mock_task = Mock()
    mock_task.id = "TSK-01-01"
    mock_task.title = "Test Task"
    mock_task.status = Mock(value=status_code)

    mock_orchestrator = Mock()
    mock_orchestrator.project_name = "test"
    mock_orchestrator.mode = Mock(value="quick")
    mock_orchestrator.tasks = [mock_task]
    mock_orchestrator.workers = []

    app = create_app(mock_orchestrator)
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # WP를 확장하여 Task 노드 로드
        response = await client.get("/api/tree/WP-01")

    assert response.status_code == 200
    assert expected_color in response.text


# UT-003: 진행률 표시
@pytest.mark.asyncio
async def test_wp_progress_displayed() -> None:
    """WP 노드에 진행률이 표시됨 (UT-003)."""
    from orchay.web.server import create_app

    # 2개 완료, 2개 미완료 = 50%
    mock_tasks = []
    for task_id, status in [
        ("TSK-01-01", "[xx]"),
        ("TSK-01-02", "[xx]"),
        ("TSK-01-03", "[im]"),
        ("TSK-01-04", "[ ]"),
    ]:
        task = Mock()
        task.id = task_id
        task.title = f"Task {task_id}"
        task.status = Mock(value=status)
        mock_tasks.append(task)

    mock_orchestrator = Mock()
    mock_orchestrator.project_name = "test"
    mock_orchestrator.mode = Mock(value="quick")
    mock_orchestrator.tasks = mock_tasks
    mock_orchestrator.workers = []

    app = create_app(mock_orchestrator)
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/tree")

    assert response.status_code == 200
    assert "(50%)" in response.text
    assert 'data-testid="wp-progress"' in response.text


# UT-004: 확장/축소 토글 아이콘
@pytest.mark.asyncio
async def test_toggle_icon_present() -> None:
    """WP 노드에 확장/축소 토글 아이콘이 있음 (UT-004)."""
    from orchay.web.server import create_app

    mock_task = Mock()
    mock_task.id = "TSK-01-01"
    mock_task.title = "Test Task"
    mock_task.status = Mock(value="[ ]")

    mock_orchestrator = Mock()
    mock_orchestrator.project_name = "test"
    mock_orchestrator.mode = Mock(value="quick")
    mock_orchestrator.tasks = [mock_task]
    mock_orchestrator.workers = []

    app = create_app(mock_orchestrator)
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/tree")

    assert response.status_code == 200
    assert "toggle-icon" in response.text
    assert 'data-expanded="false"' in response.text
    assert "▶" in response.text


# UT-005: Task 클릭 HTMX 속성
@pytest.mark.asyncio
async def test_task_has_htmx_detail_link() -> None:
    """Task 노드가 HTMX 상세 링크를 포함함 (UT-005)."""
    from orchay.web.server import create_app

    mock_task = Mock()
    mock_task.id = "TSK-01-01"
    mock_task.title = "Test Task"
    mock_task.status = Mock(value="[ ]")

    mock_orchestrator = Mock()
    mock_orchestrator.project_name = "test"
    mock_orchestrator.mode = Mock(value="quick")
    mock_orchestrator.tasks = [mock_task]
    mock_orchestrator.workers = []

    app = create_app(mock_orchestrator)
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/tree/WP-01")

    assert response.status_code == 200
    assert 'hx-get="/api/detail/TSK-01-01"' in response.text
    assert 'hx-target="#detail-panel"' in response.text


# UT-006: data-testid 속성 확인
@pytest.mark.asyncio
async def test_tree_has_testids() -> None:
    """트리 요소에 data-testid 속성이 있음 (E2E 테스트용)."""
    from orchay.web.server import create_app

    mock_task = Mock()
    mock_task.id = "TSK-01-01"
    mock_task.title = "Test Task"
    mock_task.status = Mock(value="[ ]")

    mock_orchestrator = Mock()
    mock_orchestrator.project_name = "test"
    mock_orchestrator.mode = Mock(value="quick")
    mock_orchestrator.tasks = [mock_task]
    mock_orchestrator.workers = []

    app = create_app(mock_orchestrator)
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/tree")

    assert response.status_code == 200
    assert 'data-testid="tree-root"' in response.text
    assert 'data-testid="tree-node-wp"' in response.text
    assert 'data-testid="toggle-icon"' in response.text


# 빈 트리 테스트
@pytest.mark.asyncio
async def test_empty_tree_message() -> None:
    """Task가 없을 때 빈 상태 메시지 표시."""
    from orchay.web.server import create_app

    mock_orchestrator = Mock()
    mock_orchestrator.project_name = "test"
    mock_orchestrator.mode = Mock(value="quick")
    mock_orchestrator.tasks = []
    mock_orchestrator.workers = []

    app = create_app(mock_orchestrator)
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/tree")

    assert response.status_code == 200
    assert 'data-testid="empty-tree"' in response.text
    assert "등록된 Task가 없습니다" in response.text
