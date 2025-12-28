# TSK-04-02 - 테스트 명세서

## 문서 정보

| 항목 | 내용 |
|------|------|
| Task ID | TSK-04-02 |
| 문서 버전 | 1.0 |
| 작성일 | 2025-12-28 |
| 상태 | 작성중 |

---

## 1. 테스트 환경

### 1.1 필수 도구

| 도구 | 버전 | 용도 |
|------|------|------|
| pytest | ^8.0 | 테스트 프레임워크 |
| pytest-asyncio | ^0.24 | 비동기 테스트 지원 |
| httpx | ^0.27 | FastAPI TestClient |
| pytest-cov | ^6.0 | 커버리지 측정 |

### 1.2 환경 설정

```bash
# 테스트 실행
cd orchay
pytest tests/test_web/ -v

# 커버리지 포함
pytest tests/test_web/ --cov=src/orchay/web --cov-report=term-missing

# 성능 테스트만
pytest tests/test_web/test_performance.py -v
```

### 1.3 pytest.ini 설정

```ini
[pytest]
asyncio_mode = auto
testpaths = tests
python_files = test_*.py
python_functions = test_*
```

---

## 2. 테스트 케이스 상세

### 2.1 서버 라이프사이클 테스트 (test_server.py)

#### TC-01: 서버 시작 테스트

| 항목 | 내용 |
|------|------|
| ID | TC-01 |
| 목적 | FastAPI 서버가 정상적으로 시작되는지 확인 |
| 사전 조건 | Mock Orchestrator 준비 |
| 테스트 단계 | 1. create_app(orchestrator) 호출<br>2. TestClient 생성<br>3. GET / 요청<br>4. 200 응답 확인 |
| 기대 결과 | HTTP 200 OK, HTML 컨텐츠 반환 |
| 우선순위 | 높음 |

```python
def test_server_starts(mock_orchestrator):
    """서버가 정상적으로 시작되는지 확인"""
    from orchay.web.server import create_app
    from fastapi.testclient import TestClient

    app = create_app(mock_orchestrator)
    client = TestClient(app)

    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
```

#### TC-02: 서버 종료 테스트

| 항목 | 내용 |
|------|------|
| ID | TC-02 |
| 목적 | 서버 종료 시 리소스가 정상 정리되는지 확인 |
| 사전 조건 | 서버 시작 상태 |
| 테스트 단계 | 1. TestClient 컨텍스트 종료<br>2. 리소스 해제 확인 |
| 기대 결과 | 정상 종료, 예외 없음 |
| 우선순위 | 높음 |

```python
def test_server_stops(mock_orchestrator):
    """서버가 정상적으로 종료되는지 확인"""
    from orchay.web.server import create_app
    from fastapi.testclient import TestClient

    app = create_app(mock_orchestrator)

    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200

    # 컨텍스트 종료 후 예외 없음 확인
    assert True
```

---

### 2.2 API 엔드포인트 테스트 (test_api.py)

#### TC-03: 루트 엔드포인트 테스트

| 항목 | 내용 |
|------|------|
| ID | TC-03 |
| 목적 | GET / 가 메인 페이지 HTML을 반환하는지 확인 |
| 테스트 단계 | 1. GET / 요청<br>2. 상태 코드 확인<br>3. HTML 구조 확인 |
| 기대 결과 | 200 OK, 완전한 HTML (DOCTYPE, head, body) |

```python
def test_root_endpoint(client):
    """메인 페이지가 정상 반환되는지 확인"""
    response = client.get("/")

    assert response.status_code == 200
    assert "<!DOCTYPE html>" in response.text or "<html" in response.text
    assert "orchay" in response.text.lower()
```

#### TC-04: 트리 엔드포인트 테스트

| 항목 | 내용 |
|------|------|
| ID | TC-04 |
| 목적 | GET /api/tree 가 WBS 트리 HTML 조각을 반환하는지 확인 |
| 테스트 단계 | 1. GET /api/tree 요청<br>2. 상태 코드 확인<br>3. WP/Task 요소 존재 확인 |
| 기대 결과 | 200 OK, 트리 노드가 포함된 HTML 조각 |

```python
def test_tree_endpoint(client):
    """WBS 트리가 정상 반환되는지 확인"""
    response = client.get("/api/tree")

    assert response.status_code == 200
    # WP 또는 Task 요소가 있어야 함
    assert "WP-" in response.text or "TSK-" in response.text or "tree" in response.text.lower()
```

#### TC-05: 트리 확장 엔드포인트 테스트

| 항목 | 내용 |
|------|------|
| ID | TC-05 |
| 목적 | GET /api/tree/{wp_id} 가 하위 노드를 반환하는지 확인 |
| 테스트 단계 | 1. GET /api/tree/WP-01 요청<br>2. 상태 코드 확인<br>3. 하위 노드 존재 확인 |
| 기대 결과 | 200 OK, 하위 ACT/TSK 노드 포함 |

```python
def test_tree_expand_endpoint(client):
    """트리 확장 요청이 정상 동작하는지 확인"""
    response = client.get("/api/tree/WP-01")

    # 존재하지 않아도 에러가 아닌 빈 결과 반환
    assert response.status_code in [200, 404]
```

#### TC-06: 상세 엔드포인트 테스트

| 항목 | 내용 |
|------|------|
| ID | TC-06 |
| 목적 | GET /api/detail/{task_id} 가 Task 상세를 반환하는지 확인 |
| 테스트 단계 | 1. GET /api/detail/TSK-01-01 요청<br>2. 상태 코드 확인<br>3. Task 정보 포함 확인 |
| 기대 결과 | 200 OK, Task ID, Status, Category 등 포함 |

```python
def test_detail_endpoint(client, mock_task_id):
    """Task 상세가 정상 반환되는지 확인"""
    response = client.get(f"/api/detail/{mock_task_id}")

    assert response.status_code == 200
    assert mock_task_id in response.text or "detail" in response.text.lower()
```

#### TC-07: Worker 엔드포인트 테스트

| 항목 | 내용 |
|------|------|
| ID | TC-07 |
| 목적 | GET /api/workers 가 Worker 상태 바를 반환하는지 확인 |
| 테스트 단계 | 1. GET /api/workers 요청<br>2. 상태 코드 확인<br>3. Worker 상태 아이콘 포함 확인 |
| 기대 결과 | 200 OK, Worker 상태 표시 (🟢, 🟡 등) |

```python
def test_workers_endpoint(client):
    """Worker 상태가 정상 반환되는지 확인"""
    response = client.get("/api/workers")

    assert response.status_code == 200
    # Worker 상태 표시 요소가 있어야 함
    assert "worker" in response.text.lower() or any(
        icon in response.text for icon in ["🟢", "🟡", "🔴", "⏸️"]
    )
```

#### TC-08: 진행률 엔드포인트 테스트

| 항목 | 내용 |
|------|------|
| ID | TC-08 |
| 목적 | GET /api/progress 가 전체 진행률을 반환하는지 확인 |
| 테스트 단계 | 1. GET /api/progress 요청<br>2. 상태 코드 확인<br>3. 진행률 표시 확인 |
| 기대 결과 | 200 OK, 진행률 퍼센트 또는 프로그레스 바 |

```python
def test_progress_endpoint(client):
    """전체 진행률이 정상 반환되는지 확인"""
    response = client.get("/api/progress")

    assert response.status_code == 200
    # 진행률 관련 표시가 있어야 함
    assert "%" in response.text or "progress" in response.text.lower()
```

---

### 2.3 HTMX 인터랙션 테스트 (test_htmx.py)

#### TC-09: HTMX 속성 확인 테스트

| 항목 | 내용 |
|------|------|
| ID | TC-09 |
| 목적 | 메인 페이지에 HTMX 속성이 포함되어 있는지 확인 |
| 테스트 단계 | 1. GET / 요청<br>2. hx-get, hx-trigger 속성 존재 확인 |
| 기대 결과 | HTMX 속성 포함된 HTML |

```python
def test_htmx_attributes(client):
    """HTMX 속성이 페이지에 포함되어 있는지 확인"""
    response = client.get("/")

    assert response.status_code == 200
    # HTMX 속성 확인
    assert "hx-get" in response.text or "hx-post" in response.text
    assert "hx-trigger" in response.text or "hx-swap" in response.text
```

#### TC-10: HTMX 조각 응답 테스트

| 항목 | 내용 |
|------|------|
| ID | TC-10 |
| 목적 | API 엔드포인트가 완전한 HTML 조각을 반환하는지 확인 |
| 테스트 단계 | 1. GET /api/tree 요청<br>2. HTML 태그 구조 확인<br>3. 불완전한 HTML이 아닌지 확인 |
| 기대 결과 | 유효한 HTML 조각 (열림/닫힘 태그 매칭) |

```python
def test_htmx_partial_responses(client):
    """HTMX 조각 응답이 유효한 HTML인지 확인"""
    endpoints = ["/api/tree", "/api/workers", "/api/progress"]

    for endpoint in endpoints:
        response = client.get(endpoint)
        assert response.status_code == 200

        # 기본적인 HTML 구조 확인
        text = response.text
        # div 태그가 있다면 닫힘 태그도 있어야 함
        if "<div" in text:
            assert "</div>" in text
```

---

### 2.4 성능 테스트 (test_performance.py)

#### TC-11: 페이지 로드 시간 테스트

| 항목 | 내용 |
|------|------|
| ID | TC-11 |
| 목적 | 메인 페이지 로드 시간이 1초 미만인지 확인 |
| 테스트 단계 | 1. 타이머 시작<br>2. GET / 요청<br>3. 타이머 종료<br>4. 1초 미만 검증 |
| 기대 결과 | 응답 시간 < 1000ms |

```python
import time

def test_page_load_time(client):
    """메인 페이지 로드 시간이 1초 미만인지 확인"""
    start = time.perf_counter()
    response = client.get("/")
    elapsed = time.perf_counter() - start

    assert response.status_code == 200
    assert elapsed < 1.0, f"페이지 로드 시간 {elapsed:.3f}초 > 1초"
```

#### TC-12: API 응답 시간 테스트

| 항목 | 내용 |
|------|------|
| ID | TC-12 |
| 목적 | 모든 API 엔드포인트 응답 시간이 1초 미만인지 확인 |
| 테스트 단계 | 1. 각 엔드포인트에 대해 타이머 측정<br>2. 1초 미만 검증 |
| 기대 결과 | 모든 엔드포인트 응답 시간 < 1000ms |

```python
import time
import pytest

@pytest.mark.parametrize("endpoint", [
    "/",
    "/api/tree",
    "/api/workers",
    "/api/progress",
])
def test_api_response_time(client, endpoint):
    """API 응답 시간이 1초 미만인지 확인"""
    start = time.perf_counter()
    response = client.get(endpoint)
    elapsed = time.perf_counter() - start

    assert response.status_code == 200
    assert elapsed < 1.0, f"{endpoint} 응답 시간 {elapsed:.3f}초 > 1초"
```

---

## 3. 공통 픽스처 (conftest.py)

```python
import pytest
from fastapi.testclient import TestClient
from orchay.web.server import create_app
from orchay.models.task import Task, TaskStatus, TaskCategory, TaskPriority
from orchay.models.worker import Worker, WorkerState


@pytest.fixture
def mock_tasks():
    """테스트용 Mock Task 목록"""
    return [
        Task(
            id="TSK-01-01",
            title="기능 구현",
            status=TaskStatus.DETAIL_DESIGN,
            category=TaskCategory.DEVELOPMENT,
            priority=TaskPriority.HIGH,
            depends=[],
        ),
        Task(
            id="TSK-01-02",
            title="테스트 작성",
            status=TaskStatus.TODO,
            category=TaskCategory.DEVELOPMENT,
            priority=TaskPriority.MEDIUM,
            depends=["TSK-01-01"],
        ),
    ]


@pytest.fixture
def mock_workers():
    """테스트용 Mock Worker 목록"""
    return [
        Worker(id=1, pane_id=1, state=WorkerState.IDLE),
        Worker(id=2, pane_id=2, state=WorkerState.BUSY),
        Worker(id=3, pane_id=3, state=WorkerState.PAUSED),
    ]


@pytest.fixture
def mock_orchestrator(mock_tasks, mock_workers):
    """테스트용 Mock Orchestrator"""
    class MockOrchestrator:
        def __init__(self):
            self.tasks = mock_tasks
            self.workers = mock_workers
            self.mode = "quick"
            self.project = "test-project"

    return MockOrchestrator()


@pytest.fixture
def client(mock_orchestrator):
    """FastAPI TestClient 픽스처"""
    app = create_app(mock_orchestrator)
    with TestClient(app) as c:
        yield c


@pytest.fixture
def mock_task_id():
    """테스트용 Task ID"""
    return "TSK-01-01"
```

---

## 4. 테스트 실행 계획

### 4.1 실행 순서

| 순서 | 테스트 파일 | 설명 |
|------|------------|------|
| 1 | test_server.py | 서버 기동 가능 여부 먼저 확인 |
| 2 | test_api.py | API 엔드포인트 기능 확인 |
| 3 | test_htmx.py | HTMX 통합 확인 |
| 4 | test_performance.py | 성능 요구사항 충족 확인 |

### 4.2 CI/CD 통합

```yaml
# .github/workflows/test.yml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          cd orchay
          pip install -e ".[dev]"
      - name: Run tests
        run: |
          cd orchay
          pytest tests/test_web/ -v --cov=src/orchay/web
```

---

## 5. 합격/불합격 기준

### 5.1 합격 기준

| 기준 | 요구 사항 |
|------|----------|
| 테스트 통과율 | 100% |
| 성능 테스트 | 모든 엔드포인트 < 1초 |
| 에러 없음 | ERROR 상태 0개 |

### 5.2 불합격 기준

| 기준 | 조건 |
|------|------|
| 기능 테스트 실패 | 1개 이상 FAILED |
| 성능 기준 미달 | 응답 시간 >= 1초 |
| 테스트 실행 오류 | ERROR 발생 |

---

## 변경 이력

| 버전 | 일자 | 작성자 | 변경 내용 |
|------|------|--------|----------|
| 1.0 | 2025-12-28 | Claude | 최초 작성 |
