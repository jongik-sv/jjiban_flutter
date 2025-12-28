# TSK-02-01 테스트 명세서

## 문서 정보

| 항목 | 내용 |
|------|------|
| Task ID | TSK-02-01 |
| 문서 버전 | 1.0 |
| 작성일 | 2025-12-28 |

---

## 1. 테스트 범위

### 1.1 테스트 대상

| 대상 | 파일 | 테스트 유형 |
|------|------|------------|
| 트리 API 라우트 | server.py | 단위/통합 |
| 트리 구조 변환 | tree.py | 단위 |
| 진행률 계산 | tree.py | 단위 |
| HTMX 인터랙션 | tree.html | E2E |

### 1.2 테스트 제외

| 항목 | 사유 |
|------|------|
| tree.html 스타일링 | UI 스타일은 시각 검증 |
| Orchestrator 모킹 | 별도 fixture 제공 |

---

## 2. 단위 테스트

### TC-01: 전체 트리 API 정상 응답

| 항목 | 내용 |
|------|------|
| 테스트 ID | TC-01 |
| 설명 | GET /api/tree 요청 시 HTML 트리 반환 |
| 사전 조건 | Orchestrator에 tasks 로드됨 |
| 테스트 단계 | 1. GET /api/tree 요청<br>2. 응답 확인 |
| 예상 결과 | 200 OK, Content-Type: text/html |
| 검증 항목 | - 응답 본문에 tree-node 클래스 포함<br>- WP 노드 포함 |

```python
async def test_get_tree_returns_html(client):
    response = await client.get("/api/tree")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "tree-node" in response.text
```

### TC-02: WP 하위 노드 API 정상 응답

| 항목 | 내용 |
|------|------|
| 테스트 ID | TC-02 |
| 설명 | GET /api/tree/{wp_id} 요청 시 하위 노드 반환 |
| 사전 조건 | WP-02가 존재 |
| 테스트 단계 | 1. GET /api/tree/WP-02 요청<br>2. 응답 확인 |
| 예상 결과 | 200 OK, 하위 Task 노드 포함 |
| 검증 항목 | - TSK-02-01 포함<br>- WP 노드 미포함 |

```python
async def test_get_wp_children(client):
    response = await client.get("/api/tree/WP-02")
    assert response.status_code == 200
    assert "TSK-02-01" in response.text
    assert 'data-id="WP-02"' not in response.text
```

### TC-03: 트리 구조 변환 정확성

| 항목 | 내용 |
|------|------|
| 테스트 ID | TC-03 |
| 설명 | Task 목록이 WP/ACT/TSK 계층으로 변환됨 |
| 사전 조건 | Task 목록 제공 |
| 테스트 단계 | 1. build_tree 함수 호출<br>2. 결과 구조 확인 |
| 예상 결과 | TreeNode 리스트, 계층 구조 정확 |

```python
def test_build_tree_structure():
    tasks = [
        Task(id="TSK-01-01", title="Task 1", status="[ ]"),
        Task(id="TSK-01-02", title="Task 2", status="[bd]"),
        Task(id="TSK-02-01", title="Task 3", status="[dd]"),
    ]
    tree = build_tree(tasks)

    assert len(tree) == 2  # WP-01, WP-02
    assert tree[0].id == "WP-01"
    assert len(tree[0].children) == 2  # TSK-01-01, TSK-01-02
    assert tree[1].id == "WP-02"
    assert len(tree[1].children) == 1  # TSK-02-01
```

### TC-04: 진행률 계산 정확성

| 항목 | 내용 |
|------|------|
| 테스트 ID | TC-04 |
| 설명 | WP 진행률이 하위 Task 완료 비율로 계산됨 |
| 사전 조건 | Task 목록 제공 |
| 테스트 단계 | 1. calculate_progress 함수 호출<br>2. 결과 확인 |
| 예상 결과 | 정확한 퍼센트 값 |

```python
def test_calculate_progress():
    tasks = [
        Task(status="[xx]"),  # 완료
        Task(status="[xx]"),  # 완료
        Task(status="[im]"),  # 미완료
        Task(status="[ ]"),   # 미완료
    ]
    progress = calculate_progress(tasks)
    assert progress == 50.0  # 2/4 = 50%

def test_calculate_progress_empty():
    progress = calculate_progress([])
    assert progress == 0.0

def test_calculate_progress_all_complete():
    tasks = [Task(status="[xx]"), Task(status="[xx]")]
    progress = calculate_progress(tasks)
    assert progress == 100.0
```

### TC-05: 존재하지 않는 WP 404 응답

| 항목 | 내용 |
|------|------|
| 테스트 ID | TC-05 |
| 설명 | 존재하지 않는 WP 요청 시 404 반환 |
| 사전 조건 | WP-99 미존재 |
| 테스트 단계 | 1. GET /api/tree/WP-99 요청<br>2. 응답 확인 |
| 예상 결과 | 404 Not Found |

```python
async def test_get_invalid_wp_returns_404(client):
    response = await client.get("/api/tree/WP-99")
    assert response.status_code == 404
    assert "찾을 수 없습니다" in response.text
```

---

## 3. E2E 테스트

### TC-06: HTMX 자동 갱신

| 항목 | 내용 |
|------|------|
| 테스트 ID | TC-06 |
| 설명 | 트리가 5초마다 자동으로 갱신됨 |
| 사전 조건 | 웹서버 실행, 브라우저 열림 |
| 테스트 단계 | 1. 페이지 로드<br>2. 6초 대기<br>3. 네트워크 요청 확인 |
| 예상 결과 | /api/tree 요청 2회 이상 |
| 검증 항목 | - hx-trigger="every 5s" 동작<br>- 깜빡임 없이 업데이트 |

```python
async def test_htmx_auto_refresh(page):
    await page.goto("http://localhost:8080")

    # 초기 로드 확인
    await page.wait_for_selector(".tree-root")

    # 6초 대기 (5초 갱신 주기)
    await asyncio.sleep(6)

    # 네트워크 요청 확인
    requests = page.request_log
    tree_requests = [r for r in requests if "/api/tree" in r.url]
    assert len(tree_requests) >= 2
```

### TC-07: WP 확장/축소 인터랙션

| 항목 | 내용 |
|------|------|
| 테스트 ID | TC-07 |
| 설명 | WP 클릭 시 하위 노드 표시/숨김 |
| 사전 조건 | 트리 로드됨 |
| 테스트 단계 | 1. WP-02 클릭<br>2. 하위 노드 확인<br>3. WP-02 다시 클릭<br>4. 하위 노드 숨김 확인 |
| 예상 결과 | 토글 동작 정상 |

```python
async def test_wp_expand_collapse(page):
    await page.goto("http://localhost:8080")

    # WP-02 확장
    wp02 = page.locator('[data-id="WP-02"]')
    await wp02.click()

    # 하위 노드 표시 확인
    await page.wait_for_selector('[data-id="TSK-02-01"]')
    assert await page.is_visible('[data-id="TSK-02-01"]')

    # WP-02 축소
    await wp02.click()
    await asyncio.sleep(0.5)

    # 하위 노드 숨김 확인
    assert not await page.is_visible('[data-id="TSK-02-01"]')
```

---

## 4. 테스트 데이터

### 4.1 Mock Orchestrator

```python
@pytest.fixture
def mock_orchestrator():
    orch = Mock(spec=Orchestrator)
    orch.tasks = [
        Task(id="TSK-01-01", title="FastAPI 앱", status="[ ]", category="development"),
        Task(id="TSK-01-02", title="템플릿 구조", status="[ ]", category="development"),
        Task(id="TSK-02-01", title="트리 API", status="[bd]", category="development"),
        Task(id="TSK-02-02", title="트리 템플릿", status="[ ]", category="development"),
    ]
    return orch
```

### 4.2 FastAPI Test Client

```python
@pytest.fixture
async def client(mock_orchestrator):
    app = create_app(mock_orchestrator)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
```

---

## 5. 테스트 실행

### 5.1 명령어

```bash
# 단위 테스트
pytest tests/web/test_tree.py -v

# E2E 테스트 (Playwright)
pytest tests/web/test_tree_e2e.py -v

# 커버리지
pytest tests/web/ --cov=orchay.web --cov-report=term-missing
```

### 5.2 통과 기준

| 항목 | 기준 |
|------|------|
| 단위 테스트 | 100% 통과 |
| E2E 테스트 | 100% 통과 |
| 커버리지 | 80% 이상 |

---

## 변경 이력

| 버전 | 일자 | 변경 내용 |
|------|------|----------|
| 1.0 | 2025-12-28 | 최초 작성 |
