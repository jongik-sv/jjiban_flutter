# TSK-01-01 테스트 명세서

## 문서 정보

| 항목 | 내용 |
|------|------|
| Task ID | TSK-01-01 |
| 문서 버전 | 1.0 |
| 작성일 | 2025-12-28 |
| 연관 설계서 | `010-design.md` |
| 추적 매트릭스 | `025-traceability-matrix.md` |

---

## 1. 단위 테스트

### TC-01: create_app 함수 테스트

| 항목 | 내용 |
|------|------|
| 테스트 ID | TC-01 |
| 테스트 대상 | `create_app` 함수 |
| 사전 조건 | Mock Orchestrator 준비 |
| 테스트 단계 | 1. Mock Orchestrator 생성<br/>2. create_app(orchestrator) 호출<br/>3. 반환값 검증 |
| 예상 결과 | FastAPI 앱 인스턴스 반환 |
| 우선순위 | 높음 |

```python
# 테스트 코드 예시
def test_create_app():
    """create_app이 FastAPI 앱을 정상적으로 생성하는지 테스트"""
    from orchay.web.server import create_app
    from unittest.mock import Mock

    mock_orchestrator = Mock()
    mock_orchestrator.project = "test_project"
    mock_orchestrator.mode = Mock(value="quick")
    mock_orchestrator.tasks = []
    mock_orchestrator.workers = []

    app = create_app(mock_orchestrator)

    assert app is not None
    assert isinstance(app, FastAPI)
    assert app.state.orchestrator == mock_orchestrator
```

### TC-07: Orchestrator 접근 테스트

| 항목 | 내용 |
|------|------|
| 테스트 ID | TC-07 |
| 테스트 대상 | `app.state.orchestrator` |
| 사전 조건 | create_app으로 앱 생성 완료 |
| 테스트 단계 | 1. create_app 호출<br/>2. app.state.orchestrator 접근<br/>3. 원본 Orchestrator와 동일한지 검증 |
| 예상 결과 | 주입된 Orchestrator와 동일 |
| 우선순위 | 높음 |

```python
def test_orchestrator_reference():
    """Orchestrator 참조가 올바르게 저장되는지 테스트"""
    from orchay.web.server import create_app
    from unittest.mock import Mock

    mock_orchestrator = Mock()
    app = create_app(mock_orchestrator)

    assert app.state.orchestrator is mock_orchestrator
```

---

## 2. 통합 테스트

### TC-02: 메인 페이지 응답 테스트

| 항목 | 내용 |
|------|------|
| 테스트 ID | TC-02 |
| 테스트 대상 | `GET /` 엔드포인트 |
| 사전 조건 | 테스트 클라이언트 준비, 템플릿 파일 존재 |
| 테스트 단계 | 1. GET / 요청<br/>2. 응답 상태 코드 확인<br/>3. Content-Type 확인<br/>4. 필수 요소 포함 확인 |
| 예상 결과 | 200 OK, text/html, 프로젝트명 포함 |
| 우선순위 | 높음 |

```python
import pytest
from httpx import AsyncClient
from orchay.web.server import create_app

@pytest.mark.asyncio
async def test_index_page():
    """메인 페이지가 정상적으로 렌더링되는지 테스트"""
    from unittest.mock import Mock

    mock_orchestrator = Mock()
    mock_orchestrator.project = "test_project"
    mock_orchestrator.mode = Mock(value="quick")
    mock_orchestrator.tasks = []
    mock_orchestrator.workers = []

    app = create_app(mock_orchestrator)

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "test_project" in response.text
```

### TC-03: 트리 API 응답 테스트

| 항목 | 내용 |
|------|------|
| 테스트 ID | TC-03 |
| 테스트 대상 | `GET /api/tree` 엔드포인트 |
| 사전 조건 | Mock Task 목록 준비 |
| 테스트 단계 | 1. GET /api/tree 요청<br/>2. 응답 상태 코드 확인<br/>3. HTML 조각 반환 확인 |
| 예상 결과 | 200 OK, HTML 조각 반환 |
| 우선순위 | 높음 |

```python
@pytest.mark.asyncio
async def test_tree_api():
    """트리 API가 HTML 조각을 반환하는지 테스트"""
    from unittest.mock import Mock

    mock_task = Mock()
    mock_task.id = "TSK-01-01"
    mock_task.title = "Test Task"

    mock_orchestrator = Mock()
    mock_orchestrator.tasks = [mock_task]

    app = create_app(mock_orchestrator)

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/tree")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
```

### TC-04: Task 상세 API 응답 테스트

| 항목 | 내용 |
|------|------|
| 테스트 ID | TC-04 |
| 테스트 대상 | `GET /api/detail/{task_id}` 엔드포인트 |
| 사전 조건 | 존재하는 Task ID |
| 테스트 단계 | 1. GET /api/detail/TSK-01-01 요청<br/>2. 응답 상태 코드 확인<br/>3. Task 정보 포함 확인 |
| 예상 결과 | 200 OK, Task 정보 포함 |
| 우선순위 | 높음 |

```python
@pytest.mark.asyncio
async def test_detail_api():
    """Task 상세 API가 올바른 정보를 반환하는지 테스트"""
    from unittest.mock import Mock

    mock_task = Mock()
    mock_task.id = "TSK-01-01"
    mock_task.title = "Test Task"
    mock_task.status = Mock(value="[ ]")
    mock_task.category = Mock(value="development")

    mock_orchestrator = Mock()
    mock_orchestrator.tasks = [mock_task]

    app = create_app(mock_orchestrator)

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/detail/TSK-01-01")

    assert response.status_code == 200
    assert "TSK-01-01" in response.text
```

### TC-05: Worker API 응답 테스트

| 항목 | 내용 |
|------|------|
| 테스트 ID | TC-05 |
| 테스트 대상 | `GET /api/workers` 엔드포인트 |
| 사전 조건 | Mock Worker 목록 준비 |
| 테스트 단계 | 1. GET /api/workers 요청<br/>2. 응답 상태 코드 확인<br/>3. Worker 상태 포함 확인 |
| 예상 결과 | 200 OK, Worker 상태 포함 |
| 우선순위 | 높음 |

```python
@pytest.mark.asyncio
async def test_workers_api():
    """Worker API가 상태 정보를 반환하는지 테스트"""
    from unittest.mock import Mock

    mock_worker = Mock()
    mock_worker.id = 1
    mock_worker.state = Mock(value="idle")

    mock_orchestrator = Mock()
    mock_orchestrator.workers = [mock_worker]

    app = create_app(mock_orchestrator)

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/workers")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
```

### TC-06: 존재하지 않는 Task 테스트

| 항목 | 내용 |
|------|------|
| 테스트 ID | TC-06 |
| 테스트 대상 | `GET /api/detail/{task_id}` 404 처리 |
| 사전 조건 | 존재하지 않는 Task ID |
| 테스트 단계 | 1. GET /api/detail/INVALID-ID 요청<br/>2. 응답 상태 코드 확인<br/>3. 에러 메시지 확인 |
| 예상 결과 | 404 Not Found, 에러 메시지 포함 |
| 우선순위 | 중간 |

```python
@pytest.mark.asyncio
async def test_detail_api_not_found():
    """존재하지 않는 Task 요청 시 404를 반환하는지 테스트"""
    from unittest.mock import Mock

    mock_orchestrator = Mock()
    mock_orchestrator.tasks = []

    app = create_app(mock_orchestrator)

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/detail/INVALID-ID")

    assert response.status_code == 404
    assert "찾을 수 없습니다" in response.text
```

---

## 3. 수동 테스트

### MT-01: 서버 실행 테스트

| 항목 | 내용 |
|------|------|
| 테스트 ID | MT-01 |
| 테스트 대상 | uvicorn 서버 실행 |
| 사전 조건 | 의존성 설치 완료 |
| 테스트 단계 | 1. `orchay --web` 실행<br/>2. 콘솔에서 서버 시작 메시지 확인<br/>3. 브라우저에서 localhost:8080 접속<br/>4. 페이지 로드 확인 |
| 예상 결과 | 서버 정상 시작, 페이지 표시 |
| 우선순위 | 높음 |

### MT-02: 페이지 로드 시간 테스트

| 항목 | 내용 |
|------|------|
| 테스트 ID | MT-02 |
| 테스트 대상 | 페이지 로드 성능 |
| 사전 조건 | 서버 실행 중 |
| 테스트 단계 | 1. 브라우저 개발자 도구 열기<br/>2. 네트워크 탭 선택<br/>3. 페이지 새로고침<br/>4. 로드 시간 확인 |
| 예상 결과 | 1초 이내 로드 완료 |
| 우선순위 | 중간 |

---

## 4. 테스트 요약

| 테스트 유형 | 테스트 케이스 수 | 우선순위 높음 | 우선순위 중간 |
|------------|----------------|--------------|--------------|
| 단위 테스트 | 2 | 2 | 0 |
| 통합 테스트 | 5 | 4 | 1 |
| 수동 테스트 | 2 | 1 | 1 |
| **합계** | **9** | **7** | **2** |

---

## 5. 테스트 환경

| 항목 | 요구사항 |
|------|----------|
| Python | >= 3.10 |
| pytest | >= 7.0 |
| pytest-asyncio | >= 0.21 |
| httpx | >= 0.24 |
| FastAPI | >= 0.115 |

---

## 변경 이력

| 버전 | 일자 | 작성자 | 변경 내용 |
|------|------|--------|----------|
| 1.0 | 2025-12-28 | Claude | 최초 작성 |
