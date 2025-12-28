"""Jinja2 템플릿 테스트.

TSK-01-02: Jinja2 템플릿 기본 구조 테스트
테스트 명세: 026-test-specification.md
"""

from unittest.mock import Mock

import pytest


# 공통 fixture
@pytest.fixture
def mock_orchestrator() -> Mock:
    """Mock Orchestrator fixture."""
    mock = Mock()
    mock.project_name = "test_project"
    mock.mode = Mock(value="quick")
    mock.tasks = []
    mock.workers = []
    return mock


@pytest.fixture
def client(mock_orchestrator: Mock):
    """테스트 클라이언트 fixture."""
    from httpx import ASGITransport, AsyncClient

    from orchay.web.server import create_app

    app = create_app(mock_orchestrator)
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


# TC-01: 다크테마 적용 확인
@pytest.mark.asyncio
async def test_dark_theme_applied(mock_orchestrator: Mock) -> None:
    """다크테마 클래스가 적용되었는지 확인."""
    from httpx import ASGITransport, AsyncClient

    from orchay.web.server import create_app

    app = create_app(mock_orchestrator)
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/")

    assert response.status_code == 200
    assert "bg-gray-900" in response.text
    assert "text-gray-100" in response.text


# TC-02: 2열 레이아웃 구조 확인
@pytest.mark.asyncio
async def test_two_column_layout(mock_orchestrator: Mock) -> None:
    """2열 레이아웃 구조가 존재하는지 확인."""
    from httpx import ASGITransport, AsyncClient

    from orchay.web.server import create_app

    app = create_app(mock_orchestrator)
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/")

    assert response.status_code == 200
    assert 'id="tree-panel"' in response.text
    assert 'id="detail-panel"' in response.text
    assert "w-1/2" in response.text


# TC-03: HTMX CDN 로드
@pytest.mark.asyncio
async def test_htmx_cdn_loaded(mock_orchestrator: Mock) -> None:
    """HTMX CDN 스크립트가 포함되어 있는지 확인."""
    from httpx import ASGITransport, AsyncClient

    from orchay.web.server import create_app

    app = create_app(mock_orchestrator)
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/")

    assert response.status_code == 200
    assert "unpkg.com/htmx.org" in response.text


# TC-04: Tailwind CSS CDN 로드
@pytest.mark.asyncio
async def test_tailwind_cdn_loaded(mock_orchestrator: Mock) -> None:
    """Tailwind CSS CDN 스크립트가 포함되어 있는지 확인."""
    from httpx import ASGITransport, AsyncClient

    from orchay.web.server import create_app

    app = create_app(mock_orchestrator)
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/")

    assert response.status_code == 200
    assert "cdn.tailwindcss.com" in response.text


# TC-05: 헤더 프로젝트명 표시
@pytest.mark.asyncio
async def test_header_project_name(mock_orchestrator: Mock) -> None:
    """헤더에 프로젝트명이 표시되는지 확인."""
    from httpx import ASGITransport, AsyncClient

    from orchay.web.server import create_app

    app = create_app(mock_orchestrator)
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/")

    assert response.status_code == 200
    assert "orchay - " in response.text
    assert "test_project" in response.text


# TC-06: 헤더 모드 표시
@pytest.mark.asyncio
async def test_header_mode_badge(mock_orchestrator: Mock) -> None:
    """헤더에 실행 모드가 표시되는지 확인."""
    from httpx import ASGITransport, AsyncClient

    from orchay.web.server import create_app

    app = create_app(mock_orchestrator)
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/")

    assert response.status_code == 200
    assert "MODE:" in response.text


# TC-07: Worker 바 영역 존재
@pytest.mark.asyncio
async def test_workers_bar_exists(mock_orchestrator: Mock) -> None:
    """Worker 상태 바 영역이 존재하는지 확인."""
    from httpx import ASGITransport, AsyncClient

    from orchay.web.server import create_app

    app = create_app(mock_orchestrator)
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/")

    assert response.status_code == 200
    assert 'id="workers-bar"' in response.text


# TC-08: 트리 패널 HTMX 속성
@pytest.mark.asyncio
async def test_tree_panel_htmx_attributes(mock_orchestrator: Mock) -> None:
    """트리 패널에 HTMX 속성이 있는지 확인."""
    from httpx import ASGITransport, AsyncClient

    from orchay.web.server import create_app

    app = create_app(mock_orchestrator)
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/")

    assert response.status_code == 200
    assert 'hx-get="/api/tree"' in response.text
    assert 'hx-trigger="load, every 5s"' in response.text


# TC-09: 상세 패널 기본 상태
@pytest.mark.asyncio
async def test_detail_panel_default_message(mock_orchestrator: Mock) -> None:
    """상세 패널 기본 메시지가 표시되는지 확인."""
    from httpx import ASGITransport, AsyncClient

    from orchay.web.server import create_app

    app = create_app(mock_orchestrator)
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/")

    assert response.status_code == 200
    assert "Task를 선택하세요" in response.text


# TC-10: base.html extends 구조 확인 (템플릿 소스 검증)
def test_base_html_exists() -> None:
    """base.html 템플릿 파일이 존재하는지 확인."""
    from pathlib import Path

    base_path = Path(__file__).parent.parent / "src" / "orchay" / "web" / "templates" / "base.html"
    assert base_path.exists(), "base.html 파일이 존재해야 합니다"


def test_index_extends_base() -> None:
    """index.html이 base.html을 상속하는지 확인."""
    from pathlib import Path

    index_path = (
        Path(__file__).parent.parent / "src" / "orchay" / "web" / "templates" / "index.html"
    )
    content = index_path.read_text(encoding="utf-8")
    assert '{% extends "base.html" %}' in content, "index.html은 base.html을 상속해야 합니다"


def test_index_uses_content_block() -> None:
    """index.html이 content 블록을 사용하는지 확인."""
    from pathlib import Path

    index_path = (
        Path(__file__).parent.parent / "src" / "orchay" / "web" / "templates" / "index.html"
    )
    content = index_path.read_text(encoding="utf-8")
    assert "{% block content %}" in content, "index.html은 content 블록을 사용해야 합니다"
    assert "{% endblock %}" in content, "index.html은 endblock으로 닫아야 합니다"
