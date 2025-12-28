# TSK-03-03 - 테스트 명세서

## 문서 정보

| 항목 | 내용 |
|------|------|
| Task ID | TSK-03-03 |
| 문서 버전 | 1.0 |
| 작성일 | 2025-12-28 |

---

## 1. 테스트 범위

### 1.1 테스트 대상

| 대상 | 유형 | 설명 |
|------|------|------|
| `/api/workers` | 단위 테스트 | 진행률 포함 응답 |
| `_calculate_progress` | 단위 테스트 | 진행률 계산 로직 |
| 자동 갱신 | E2E 테스트 | HTMX 5초 폴링 |
| 에러 처리 | E2E 테스트 | 네트워크 오류 대응 |

### 1.2 테스트 제외

| 제외 대상 | 이유 |
|----------|------|
| WBS 트리 갱신 | TSK-02-03에서 이미 구현/테스트 |
| Task 상세 API | TSK-03-01에서 이미 테스트 |

---

## 2. 단위 테스트

### TC-U01: 진행률 계산 - 정상 케이스

**테스트 대상:** `_calculate_progress(tasks)`

| 입력 | 기대 결과 |
|------|----------|
| 10개 Task, 4개 [xx] | `{"total": 10, "done": 4, "percentage": 40}` |
| 5개 Task, 0개 [xx] | `{"total": 5, "done": 0, "percentage": 0}` |
| 3개 Task, 3개 [xx] | `{"total": 3, "done": 3, "percentage": 100}` |

**테스트 코드:**
```python
def test_calculate_progress_normal():
    tasks = [
        Task(id="TSK-01-01", status=TaskStatus.DONE),
        Task(id="TSK-01-02", status=TaskStatus.DONE),
        Task(id="TSK-01-03", status=TaskStatus.IN_PROGRESS),
    ]
    result = _calculate_progress(tasks)
    assert result["total"] == 3
    assert result["done"] == 2
    assert result["percentage"] == 66  # int(2/3*100)
```

### TC-U02: 진행률 계산 - 빈 리스트

**테스트 대상:** `_calculate_progress([])`

| 입력 | 기대 결과 |
|------|----------|
| 빈 리스트 | `{"total": 0, "done": 0, "percentage": 0}` |

**테스트 코드:**
```python
def test_calculate_progress_empty():
    result = _calculate_progress([])
    assert result["total"] == 0
    assert result["done"] == 0
    assert result["percentage"] == 0
```

### TC-U03: Worker API 진행률 포함 응답

**테스트 대상:** `GET /api/workers`

**검증 항목:**
- 응답 HTML에 진행률 표시 포함
- `Progress:` 텍스트 존재
- 백분율 표시 정확

**테스트 코드:**
```python
@pytest.mark.asyncio
async def test_workers_api_includes_progress():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/workers")
    assert response.status_code == 200
    assert "Progress:" in response.text
    assert "%" in response.text
```

---

## 3. E2E 테스트

### TC-E01: Worker 상태 5초 자동 갱신

**전제 조건:**
- 웹 서버 실행 중
- 브라우저 접속

**테스트 절차:**
1. 페이지 접속
2. Worker 상태 확인
3. 6초 대기
4. Worker 상태 변경 확인

**기대 결과:**
- 5초 후 Worker 상태 영역 갱신
- HTMX 요청 발생 확인

**검증 방법:**
```python
# Playwright 사용
async def test_worker_auto_refresh(page):
    await page.goto("http://localhost:8080")
    initial_html = await page.inner_html("#workers-bar")
    await page.wait_for_timeout(6000)  # 6초 대기
    # HTMX 요청 발생 확인 (네트워크 모니터링)
```

### TC-E02: 진행률 표시 정확성

**전제 조건:**
- Task 10개, 완료 4개 상태

**테스트 절차:**
1. 페이지 접속
2. Worker Bar 확인

**기대 결과:**
- "4/10 (40%)" 표시
- 프로그레스 바 40% 채움

**검증 방법:**
```python
async def test_progress_display(page):
    await page.goto("http://localhost:8080")
    progress_text = await page.text_content("#workers-bar")
    assert "4/10" in progress_text
    assert "40%" in progress_text
```

### TC-E03: Task 상세 자동 갱신

**전제 조건:**
- 페이지 접속
- Task 선택

**테스트 절차:**
1. Task 클릭
2. 상세 정보 확인
3. 6초 대기
4. 상세 정보 갱신 확인

**기대 결과:**
- Task 선택 후 상세 표시
- 5초 후 자동 갱신 발생

### TC-E04: UI 깜빡임 테스트

**전제 조건:**
- 페이지 접속

**테스트 절차:**
1. 갱신 전 스크린샷
2. 갱신 후 스크린샷
3. 시각적 비교

**기대 결과:**
- 깜빡임 없이 콘텐츠만 변경
- settle 시간 적용 확인

### TC-E05: 네트워크 오류 처리

**전제 조건:**
- 페이지 접속 후 서버 중단 시뮬레이션

**테스트 절차:**
1. 정상 로드 확인
2. 네트워크 오프라인 설정
3. 갱신 시도 (5초 대기)
4. 에러 메시지 확인
5. 네트워크 복구
6. 자동 복구 확인

**기대 결과:**
- 오류 시 "연결 오류. 자동 재시도 중..." 표시
- 복구 후 정상 콘텐츠 표시

---

## 4. 테스트 환경

### 4.1 단위 테스트

| 항목 | 값 |
|------|-----|
| 프레임워크 | pytest |
| 비동기 | pytest-asyncio |
| HTTP 클라이언트 | httpx |

### 4.2 E2E 테스트

| 항목 | 값 |
|------|-----|
| 프레임워크 | pytest-playwright |
| 브라우저 | Chromium |
| 타임아웃 | 10초 |

---

## 5. 테스트 실행

```bash
# 단위 테스트
cd orchay
pytest tests/test_web_progress.py -v

# E2E 테스트
pytest tests/test_web_e2e.py -v --headed
```

---

## 변경 이력

| 버전 | 일자 | 작성자 | 변경 내용 |
|------|------|--------|----------|
| 1.0 | 2025-12-28 | Claude | 최초 작성 |
