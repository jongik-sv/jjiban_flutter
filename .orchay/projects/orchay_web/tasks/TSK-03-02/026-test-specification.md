# TSK-03-02 - 테스트 명세서

## 문서 정보

| 항목 | 내용 |
|------|------|
| Task ID | TSK-03-02 |
| 문서 버전 | 1.0 |
| 작성일 | 2025-12-28 |
| 설계 문서 | `010-design.md` |
| 추적 매트릭스 | `025-traceability-matrix.md` |

---

## 1. 테스트 범위

### 1.1 테스트 대상

| 대상 | 설명 | 테스트 유형 |
|------|------|------------|
| `/api/workers` API | Worker 상태 반환 엔드포인트 | 단위 테스트 |
| workers.html 템플릿 | Worker 상태 바 렌더링 | 렌더링 테스트 |
| HTMX 자동 갱신 | 5초 polling 동작 | E2E 테스트 |
| Jinja2 필터 | status_icon, status_bg | 단위 테스트 |

### 1.2 테스트 제외 대상

| 제외 대상 | 이유 |
|----------|------|
| Orchestrator 내부 로직 | 별도 Task (기존 테스트 존재) |
| Worker 상태 변경 로직 | 별도 모듈 테스트 |

---

## 2. 테스트 케이스

### 2.1 API 테스트

#### TC-01-01: GET /api/workers 기본 응답

| 항목 | 내용 |
|------|------|
| 테스트 ID | TC-01-01 |
| 테스트 명 | Worker 상태 API 기본 응답 테스트 |
| 관련 유즈케이스 | UC-01 |
| 사전 조건 | 웹서버 실행, Orchestrator 초기화 |

**테스트 단계:**
1. GET /api/workers 요청 전송
2. HTTP 200 응답 확인
3. Content-Type: text/html 확인
4. HTML 내 Worker 정보 포함 확인

**예상 결과:**
- 상태 코드: 200
- 응답 본문: Worker 상태 HTML 파셜

**테스트 코드 (pytest):**
```python
@pytest.mark.asyncio
async def test_get_workers_success(client: AsyncClient):
    response = await client.get("/api/workers")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "W1" in response.text or "No workers" in response.text
```

---

#### TC-01-02: Worker 없음 처리

| 항목 | 내용 |
|------|------|
| 테스트 ID | TC-01-02 |
| 테스트 명 | Worker 없을 때 빈 상태 표시 |
| 관련 유즈케이스 | UC-01 대안 흐름 |
| 사전 조건 | Orchestrator.workers = [] |

**테스트 단계:**
1. 빈 Worker 목록으로 서버 시작
2. GET /api/workers 요청
3. "No workers available" 메시지 확인

**예상 결과:**
- 응답에 "No workers" 또는 빈 상태 메시지 포함

**테스트 코드:**
```python
@pytest.mark.asyncio
async def test_get_workers_empty(client_empty: AsyncClient):
    response = await client_empty.get("/api/workers")
    assert response.status_code == 200
    assert "No workers" in response.text
```

---

### 2.2 렌더링 테스트

#### TC-02-01: Worker 상태별 아이콘 렌더링

| 항목 | 내용 |
|------|------|
| 테스트 ID | TC-02-01 |
| 테스트 명 | 상태별 올바른 아이콘 표시 |
| 관련 비즈니스 규칙 | - |
| 사전 조건 | 다양한 상태의 Worker 존재 |

**테스트 데이터:**

| Worker ID | State | 예상 아이콘 |
|-----------|-------|-----------|
| 1 | IDLE | 🟢 |
| 2 | BUSY | 🟡 |
| 3 | ERROR | 🔴 |

**테스트 단계:**
1. 각 상태의 Worker 생성
2. GET /api/workers 요청
3. 응답에서 각 상태별 아이콘 확인

**예상 결과:**
- IDLE: 🟢 포함
- BUSY: 🟡 포함
- ERROR: 🔴 포함

**테스트 코드:**
```python
@pytest.mark.asyncio
async def test_worker_status_icons(client_with_workers: AsyncClient):
    response = await client_with_workers.get("/api/workers")
    assert "🟢" in response.text  # IDLE
    assert "🟡" in response.text  # BUSY
    assert "🔴" in response.text  # ERROR
```

---

#### TC-02-02: Worker 상태별 배경색 클래스

| 항목 | 내용 |
|------|------|
| 테스트 ID | TC-02-02 |
| 테스트 명 | 상태별 올바른 Tailwind 배경색 클래스 |
| 관련 비즈니스 규칙 | BR-02 |
| 사전 조건 | 다양한 상태의 Worker 존재 |

**테스트 단계:**
1. 각 상태의 Worker 생성
2. GET /api/workers 요청
3. 응답 HTML에서 Tailwind 클래스 확인

**예상 결과:**
- IDLE: `bg-green-500/20` 클래스 포함
- BUSY: `bg-yellow-500/20` 클래스 포함
- ERROR: `bg-red-500/20` 클래스 포함

**테스트 코드:**
```python
@pytest.mark.asyncio
async def test_worker_status_bg_classes(client_with_workers: AsyncClient):
    response = await client_with_workers.get("/api/workers")
    assert "bg-green-500/20" in response.text  # IDLE
    assert "bg-yellow-500/20" in response.text  # BUSY
    assert "bg-red-500/20" in response.text  # ERROR
```

---

### 2.3 비즈니스 규칙 테스트

#### TC-03-01: busy Worker의 current_task 표시

| 항목 | 내용 |
|------|------|
| 테스트 ID | TC-03-01 |
| 테스트 명 | busy 상태 Worker에 Task ID 표시 |
| 관련 비즈니스 규칙 | BR-01 |
| 사전 조건 | busy 상태 + current_task 설정 |

**테스트 데이터:**
- Worker(id=1, state=BUSY, current_task="TSK-01-01")

**테스트 단계:**
1. busy 상태 Worker 생성 (current_task 포함)
2. GET /api/workers 요청
3. 응답에서 Task ID 표시 확인

**예상 결과:**
- 응답에 "TSK-01-01" 문자열 포함

**테스트 코드:**
```python
@pytest.mark.asyncio
async def test_busy_worker_shows_task(client_busy_worker: AsyncClient):
    response = await client_busy_worker.get("/api/workers")
    assert "TSK-01-01" in response.text
```

---

#### TC-03-02: idle Worker는 Task ID 미표시

| 항목 | 내용 |
|------|------|
| 테스트 ID | TC-03-02 |
| 테스트 명 | idle 상태 Worker에 Task ID 미표시 |
| 관련 비즈니스 규칙 | BR-01 역조건 |
| 사전 조건 | idle 상태 Worker (current_task=None) |

**테스트 데이터:**
- Worker(id=1, state=IDLE, current_task=None)

**테스트 단계:**
1. idle 상태 Worker 생성
2. GET /api/workers 요청
3. 응답에서 Task ID 영역 비어있음 확인

**예상 결과:**
- idle Worker 영역에 Task ID 미표시

---

### 2.4 Jinja2 필터 단위 테스트

#### TC-04-01: status_icon 필터 테스트

| 항목 | 내용 |
|------|------|
| 테스트 ID | TC-04-01 |
| 테스트 명 | status_icon 필터 모든 상태 변환 |
| 관련 컴포넌트 | Jinja2 필터 |

**테스트 데이터:**

| 입력 (WorkerState) | 예상 출력 |
|-------------------|----------|
| IDLE | "🟢" |
| BUSY | "🟡" |
| PAUSED | "⏸️" |
| ERROR | "🔴" |
| BLOCKED | "⊘" |
| DEAD | "💀" |
| DONE | "✅" |

**테스트 코드:**
```python
def test_status_icon_filter():
    from orchay.web.filters import status_icon
    from orchay.models.worker import WorkerState

    assert status_icon(WorkerState.IDLE) == "🟢"
    assert status_icon(WorkerState.BUSY) == "🟡"
    assert status_icon(WorkerState.PAUSED) == "⏸️"
    assert status_icon(WorkerState.ERROR) == "🔴"
    assert status_icon(WorkerState.BLOCKED) == "⊘"
    assert status_icon(WorkerState.DEAD) == "💀"
    assert status_icon(WorkerState.DONE) == "✅"
```

---

#### TC-04-02: status_bg 필터 테스트

| 항목 | 내용 |
|------|------|
| 테스트 ID | TC-04-02 |
| 테스트 명 | status_bg 필터 모든 상태 변환 |
| 관련 컴포넌트 | Jinja2 필터 |

**테스트 데이터:**

| 입력 (WorkerState) | 예상 출력 |
|-------------------|----------|
| IDLE | "bg-green-500/20" |
| BUSY | "bg-yellow-500/20" |
| ERROR | "bg-red-500/20" |

**테스트 코드:**
```python
def test_status_bg_filter():
    from orchay.web.filters import status_bg
    from orchay.models.worker import WorkerState

    assert status_bg(WorkerState.IDLE) == "bg-green-500/20"
    assert status_bg(WorkerState.BUSY) == "bg-yellow-500/20"
    assert status_bg(WorkerState.ERROR) == "bg-red-500/20"
```

---

### 2.5 E2E 테스트

#### TC-05-01: HTMX 자동 갱신 확인

| 항목 | 내용 |
|------|------|
| 테스트 ID | TC-05-01 |
| 테스트 명 | HTMX 5초 자동 갱신 동작 |
| 관련 비즈니스 규칙 | BR-03 |
| 사전 조건 | 브라우저 환경 (Playwright) |

**테스트 단계:**
1. 메인 페이지 로드
2. Worker 상태 바 영역 확인
3. hx-trigger="every 5s" 속성 확인
4. 5초 대기 후 갱신 요청 확인

**예상 결과:**
- 상태 바 영역에 hx-trigger="every 5s" 속성 존재
- 5초 후 /api/workers 요청 발생

**테스트 코드 (Playwright):**
```python
async def test_htmx_auto_refresh(page: Page):
    await page.goto("http://localhost:8080")

    # HTMX 속성 확인
    workers_bar = page.locator("#workers-bar")
    await expect(workers_bar).to_have_attribute("hx-trigger", "every 5s")
    await expect(workers_bar).to_have_attribute("hx-get", "/api/workers")
```

---

## 3. 테스트 환경

### 3.1 테스트 도구

| 도구 | 버전 | 용도 |
|------|------|------|
| pytest | >= 7.0 | 테스트 프레임워크 |
| pytest-asyncio | >= 0.21 | 비동기 테스트 |
| httpx | >= 0.24 | FastAPI 테스트 클라이언트 |
| playwright | >= 1.40 | E2E 브라우저 테스트 |

### 3.2 테스트 Fixture

```python
@pytest.fixture
async def client() -> AsyncIterator[AsyncClient]:
    """기본 테스트 클라이언트."""
    from orchay.web.server import create_app
    app = create_app(mock_orchestrator)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture
def mock_orchestrator():
    """테스트용 Orchestrator 모의 객체."""
    orch = Mock()
    orch.workers = [
        Worker(id=1, pane_id=1, state=WorkerState.IDLE),
        Worker(id=2, pane_id=2, state=WorkerState.BUSY, current_task="TSK-01-01"),
        Worker(id=3, pane_id=3, state=WorkerState.ERROR),
    ]
    return orch
```

---

## 4. 테스트 실행

### 4.1 단위 테스트 실행

```bash
cd orchay
pytest tests/test_web_workers.py -v
```

### 4.2 E2E 테스트 실행

```bash
cd orchay
pytest tests/e2e/test_workers_bar.py -v --browser chromium
```

### 4.3 전체 테스트 실행

```bash
cd orchay
pytest tests/ -v --cov=orchay.web
```

---

## 5. 테스트 완료 기준

### 5.1 통과 기준

| 기준 | 조건 |
|------|------|
| 단위 테스트 | 100% 통과 |
| 렌더링 테스트 | 100% 통과 |
| E2E 테스트 | 100% 통과 |
| 코드 커버리지 | >= 80% |

### 5.2 테스트 케이스 요약

| 카테고리 | 테스트 수 | 우선순위 |
|----------|----------|----------|
| API 테스트 | 2 | 높음 |
| 렌더링 테스트 | 2 | 높음 |
| 비즈니스 규칙 | 2 | 중간 |
| Jinja2 필터 | 2 | 중간 |
| E2E 테스트 | 1 | 낮음 |
| **총합** | **9** | - |

---

## 변경 이력

| 버전 | 일자 | 작성자 | 변경 내용 |
|------|------|--------|----------|
| 1.0 | 2025-12-28 | Claude | 최초 작성 |
