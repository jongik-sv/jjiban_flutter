# TSK-06-01 - 테스트 명세서

## 문서 정보

| 항목 | 내용 |
|------|------|
| Task ID | TSK-06-01 |
| 문서 버전 | 1.0 |
| 작성일 | 2025-12-28 |

---

## 1. 단위 테스트

### TC-01: calculate_stats 함수 테스트

| 항목 | 내용 |
|------|------|
| 테스트 ID | TC-01 |
| 대상 | `calculate_stats()` |
| 목적 | 통계 계산 정확성 검증 |

**테스트 케이스:**

| 입력 | 기대 출력 |
|------|----------|
| 빈 Task 목록 | `{"wp_count": 0, "act_count": 0, "task_count": 0, "percentage": 0}` |
| Task 5개 (완료 2개) | `{"task_count": 5, "done_count": 2, "percentage": 40}` |
| 모두 완료 | `{"percentage": 100}` |

**테스트 코드:**
```python
def test_calculate_stats_empty():
    """빈 목록 테스트."""
    result = calculate_stats([])
    assert result["task_count"] == 0
    assert result["percentage"] == 0

def test_calculate_stats_partial():
    """부분 완료 테스트."""
    tasks = create_mock_tasks(total=10, done=4)
    result = calculate_stats(tasks)
    assert result["task_count"] == 10
    assert result["percentage"] == 40
```

---

### TC-02: get_wp_info 함수 테스트

| 항목 | 내용 |
|------|------|
| 테스트 ID | TC-02 |
| 대상 | `get_wp_info()` |
| 목적 | WP 정보 추출 정확성 검증 |

**테스트 케이스:**

| 입력 | 기대 출력 |
|------|----------|
| 존재하는 WP ID | WP 정보 딕셔너리 |
| 존재하지 않는 WP ID | ValueError 예외 |

---

## 2. 통합 테스트

### TC-03: 통계 API 엔드포인트 테스트

| 항목 | 내용 |
|------|------|
| 테스트 ID | TC-03 |
| 대상 | `GET /api/stats` |
| 목적 | 통계 API 응답 검증 |

**테스트 코드:**
```python
@pytest.mark.asyncio
async def test_stats_endpoint():
    """통계 API 응답 테스트."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/stats")
        assert response.status_code == 200
        assert "WP:" in response.text
        assert "TSK:" in response.text
```

---

### TC-04: WP 상세 API 테스트

| 항목 | 내용 |
|------|------|
| 테스트 ID | TC-04 |
| 대상 | `GET /api/wp/{wp_id}` |
| 목적 | WP 상세 API 응답 검증 |

**테스트 케이스:**

| 입력 | 기대 결과 |
|------|----------|
| `GET /api/wp/WP-01` | 200 OK, WP 정보 HTML |
| `GET /api/wp/WP-99` | 404 Not Found |

---

## 3. E2E 테스트 (Playwright)

### TC-05: 통계 배지 표시 테스트

| 항목 | 내용 |
|------|------|
| 테스트 ID | TC-05 |
| 대상 | 통계 배지 UI |
| 목적 | 통계 배지 렌더링 검증 |

**테스트 시나리오:**
1. 페이지 접속
2. 트리 패널 로드 대기
3. 통계 배지 요소 확인 (WP, ACT, TSK, 진행률)

**Playwright 코드:**
```typescript
test('통계 배지 표시', async ({ page }) => {
  await page.goto('/');
  await page.waitForSelector('[data-testid="stats-badge"]');
  
  const wpBadge = page.locator('text=WP:');
  const tskBadge = page.locator('text=TSK:');
  
  await expect(wpBadge).toBeVisible();
  await expect(tskBadge).toBeVisible();
});
```

---

### TC-06: 검색 필터링 테스트

| 항목 | 내용 |
|------|------|
| 테스트 ID | TC-06 |
| 대상 | 검색창 필터링 |
| 목적 | 검색 시 트리 필터링 검증 |

**테스트 시나리오:**
1. 페이지 접속
2. 검색창에 "TSK-06" 입력
3. TSK-06으로 시작하는 Task만 표시 확인
4. 다른 Task는 숨겨짐 확인

**Playwright 코드:**
```typescript
test('검색 필터링', async ({ page }) => {
  await page.goto('/');
  await page.fill('[data-testid="search-input"]', 'TSK-06');
  
  // 매칭되는 Task만 표시
  const visibleTasks = page.locator('.tree-node.task:visible');
  for (const task of await visibleTasks.all()) {
    const id = await task.getAttribute('data-id');
    expect(id).toContain('TSK-06');
  }
});
```

---

### TC-07: 전체 펼치기/접기 테스트

| 항목 | 내용 |
|------|------|
| 테스트 ID | TC-07 |
| 대상 | 펼치기/접기 버튼 |
| 목적 | 일괄 펼침/접힘 동작 검증 |

**테스트 시나리오:**
1. "전체 펼치기" 버튼 클릭
2. 모든 WP 노드 expanded 상태 확인
3. "전체 접기" 버튼 클릭
4. 모든 WP 노드 collapsed 상태 확인

---

### TC-08: WP 텍스트 클릭 테스트

| 항목 | 내용 |
|------|------|
| 테스트 ID | TC-08 |
| 대상 | WP 텍스트 클릭 |
| 목적 | Detail 패널에 WP 정보 표시 검증 |

**테스트 시나리오:**
1. WP 노드의 텍스트 영역 클릭 (아이콘 제외)
2. Detail 패널에 WP 정보 표시 확인
3. 트리 확장 상태는 변경 없음 확인

**Playwright 코드:**
```typescript
test('WP 텍스트 클릭 시 상세 표시', async ({ page }) => {
  await page.goto('/');
  
  const wpText = page.locator('.tree-node.wp .wp-text').first();
  await wpText.click();
  
  const detailPanel = page.locator('#detail-panel');
  await expect(detailPanel).toContainText('WP-');
  await expect(detailPanel).toContainText('하위 Task');
});
```

---

### TC-09: 아이콘 클릭 분리 테스트

| 항목 | 내용 |
|------|------|
| 테스트 ID | TC-09 |
| 대상 | 아이콘 클릭 동작 |
| 목적 | 아이콘 클릭 시 트리만 토글 검증 |

**테스트 시나리오:**
1. WP 노드의 아이콘(▶) 클릭
2. 트리 확장됨 확인 (아이콘 ▼로 변경)
3. Detail 패널은 변경 없음 확인

---

## 4. 테스트 환경

| 항목 | 요구사항 |
|------|----------|
| Python | >= 3.10 |
| 테스트 프레임워크 | pytest, pytest-asyncio |
| E2E | Playwright |
| Mock | pytest-mock |

---

## 5. 테스트 체크리스트

- [ ] TC-01: calculate_stats 단위 테스트
- [ ] TC-02: get_wp_info 단위 테스트
- [ ] TC-03: 통계 API 통합 테스트
- [ ] TC-04: WP 상세 API 통합 테스트
- [ ] TC-05: 통계 배지 E2E 테스트
- [ ] TC-06: 검색 필터링 E2E 테스트
- [ ] TC-07: 펼치기/접기 E2E 테스트
- [ ] TC-08: WP 텍스트 클릭 E2E 테스트
- [ ] TC-09: 아이콘 클릭 분리 E2E 테스트

---

## 변경 이력

| 버전 | 일자 | 작성자 | 변경 내용 |
|------|------|--------|----------|
| 1.0 | 2025-12-28 | Claude | 최초 작성 |
