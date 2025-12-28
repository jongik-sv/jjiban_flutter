# 테스트 명세서 (026-test-specification.md)

**Template Version:** 1.0.0 — **Last Updated:** 2025-12-28

> **목적**: 단위 테스트, E2E 테스트, 매뉴얼 테스트 시나리오 및 테스트 데이터 정의
>
> **참조**: 이 문서는 `010-design.md`와 `025-traceability-matrix.md`와 함께 사용됩니다.
>
> **활용 단계**: `/wf:build`, `/wf:test` 단계에서 테스트 코드 생성 기준으로 사용

---

## 0. 문서 메타데이터

| 항목 | 내용 |
|------|------|
| Task ID | TSK-02-02 |
| Task명 | 트리 템플릿 구현 |
| 설계 참조 | `010-design.md` |
| 추적성 매트릭스 참조 | `025-traceability-matrix.md` |
| 작성일 | 2025-12-28 |
| 작성자 | Claude |

---

## 1. 테스트 전략 개요

### 1.1 테스트 범위

| 테스트 유형 | 범위 | 목표 커버리지 |
|------------|------|--------------|
| 단위 테스트 | Jinja2 매크로, 템플릿 렌더링 | 80% 이상 |
| E2E 테스트 | 트리 UI 렌더링, 인터랙션 | 100% 시나리오 커버 |
| 매뉴얼 테스트 | 시각적 표현, 색상, 레이아웃 | 전체 화면 |

### 1.2 테스트 환경

| 항목 | 내용 |
|------|------|
| 테스트 프레임워크 (단위) | pytest |
| 테스트 프레임워크 (E2E) | Playwright |
| 템플릿 엔진 | Jinja2 |
| 브라우저 | Chromium (기본) |
| 베이스 URL | `http://localhost:8080` |

---

## 2. 단위 테스트 시나리오

### 2.1 테스트 케이스 목록

| 테스트 ID | 대상 | 시나리오 | 예상 결과 | 요구사항 |
|-----------|------|----------|----------|----------|
| UT-001 | render_node | WP/ACT/TSK 노드 렌더링 | 노드 타입별 HTML 생성 | FR-001 |
| UT-002 | status_colors | 상태별 색상 클래스 반환 | 올바른 Tailwind 클래스 | FR-002, BR-03 |
| UT-003 | render_wp_node | WP 노드에 진행률 표시 | progress 필드 포함 | FR-003, BR-05 |
| UT-004 | toggle 아이콘 | 확장/축소 상태 표시 | ▶/▼ 아이콘 렌더링 | FR-004, BR-01 |
| UT-005 | render_task_node | Task 클릭 시 hx-get 속성 | /api/detail/{id} 포함 | BR-02 |
| UT-006 | selected 상태 | 선택된 노드 스타일 | ring-2 클래스 포함 | BR-04 |

### 2.2 테스트 케이스 상세

#### UT-001: 노드 타입별 렌더링

| 항목 | 내용 |
|------|------|
| **파일** | `orchay/tests/test_tree_template.py` |
| **테스트 블록** | `describe('render_node') → it('should render WP node with correct structure')` |
| **Mock 데이터** | TreeNode(id="WP-01", type="wp", title="웹서버", progress=25.0) |
| **검증 포인트** | `data-type="wp"`, `icon text-blue-400`, `font-medium` 포함 |
| **커버리지 대상** | render_node, render_wp_node 매크로 |
| **관련 요구사항** | FR-001 |

**테스트 코드 예시:**
```python
def test_render_wp_node():
    """WP 노드가 올바른 구조로 렌더링되는지 확인"""
    node = TreeNode(id="WP-01", type="wp", title="웹서버 기본 구조", progress=25.0)
    html = render_template("partials/tree.html", nodes=[node], status_colors=STATUS_COLORS)

    assert 'data-id="WP-01"' in html
    assert 'data-type="wp"' in html
    assert "text-blue-400" in html  # WP 아이콘 색상
    assert "(25%)" in html  # 진행률
```

#### UT-002: 상태별 색상 매핑

| 항목 | 내용 |
|------|------|
| **파일** | `orchay/tests/test_tree_template.py` |
| **테스트 블록** | `describe('status_colors') → it('should return correct color for each status')` |
| **테스트 데이터** | 10가지 상태 코드 |
| **검증 포인트** | 각 상태별 올바른 bg-{color}-500 클래스 반환 |
| **커버리지 대상** | status_colors 딕셔너리 |
| **관련 요구사항** | FR-002, BR-03 |

**테스트 코드 예시:**
```python
@pytest.mark.parametrize("status,expected_class", [
    ("[ ]", "bg-gray-500"),
    ("[bd]", "bg-blue-500"),
    ("[dd]", "bg-purple-500"),
    ("[ap]", "bg-green-500"),
    ("[im]", "bg-yellow-500"),
    ("[xx]", "bg-emerald-500"),
])
def test_status_color_mapping(status, expected_class):
    """상태 코드별 올바른 색상 클래스 반환"""
    assert STATUS_COLORS.get(status) == expected_class
```

#### UT-003: WP 진행률 표시

| 항목 | 내용 |
|------|------|
| **파일** | `orchay/tests/test_tree_template.py` |
| **테스트 블록** | `describe('render_wp_node') → it('should show progress percentage')` |
| **Mock 데이터** | TreeNode(type="wp", progress=75.5) |
| **검증 포인트** | `(76%)` 표시 (반올림), `text-gray-400` 클래스 |
| **커버리지 대상** | render_wp_node 매크로 진행률 부분 |
| **관련 요구사항** | FR-003, BR-05 |

#### UT-004: 확장/축소 토글 아이콘

| 항목 | 내용 |
|------|------|
| **파일** | `orchay/tests/test_tree_template.py` |
| **테스트 블록** | `describe('toggle icon') → it('should show toggle for WP with children')` |
| **Mock 데이터** | TreeNode(type="wp", children=[...]) |
| **검증 포인트** | `▶` 아이콘, `data-expanded="false"` 속성 |
| **커버리지 대상** | toggle 아이콘 렌더링 |
| **관련 요구사항** | FR-004, BR-01 |

#### UT-005: Task 클릭 HTMX 속성

| 항목 | 내용 |
|------|------|
| **파일** | `orchay/tests/test_tree_template.py` |
| **테스트 블록** | `describe('render_task_node') → it('should include hx-get for detail')` |
| **Mock 데이터** | TreeNode(id="TSK-02-01", type="task") |
| **검증 포인트** | `hx-get="/api/detail/TSK-02-01"` 포함 |
| **커버리지 대상** | render_task_node 매크로 |
| **관련 요구사항** | BR-02 |

#### UT-006: 선택된 노드 스타일

| 항목 | 내용 |
|------|------|
| **파일** | `orchay/tests/test_tree_template.py` |
| **테스트 블록** | `describe('selected state') → it('should highlight selected task')` |
| **Mock 데이터** | TreeNode(id="TSK-02-01"), selected_id="TSK-02-01" |
| **검증 포인트** | `ring-2 ring-blue-500` 클래스 포함 |
| **커버리지 대상** | is_selected 조건 분기 |
| **관련 요구사항** | BR-04 |

---

## 3. E2E 테스트 시나리오

### 3.1 테스트 케이스 목록

| 테스트 ID | 시나리오 | 사전조건 | 실행 단계 | 예상 결과 | 요구사항 |
|-----------|----------|----------|----------|----------|----------|
| E2E-001 | 트리 렌더링 | 서버 실행 | 페이지 접속 | 트리 표시됨 | FR-001, FR-002 |
| E2E-002 | 진행률 확인 | Task 데이터 존재 | WP 노드 확인 | 진행률 % 표시 | FR-003 |
| E2E-003 | WP 확장/축소 | 트리 표시됨 | WP 클릭 | 하위 노드 토글 | FR-004, BR-01 |
| E2E-004 | Task 선택 | 트리 확장됨 | Task 클릭 | 상세 패널 로드 | BR-02, BR-04 |

### 3.2 테스트 케이스 상세

#### E2E-001: 트리 렌더링 확인

| 항목 | 내용 |
|------|------|
| **파일** | `orchay/tests/e2e/test_tree.py` |
| **테스트명** | `test_tree_renders_with_nodes` |
| **사전조건** | 웹서버 실행, WBS 데이터 로드됨 |
| **data-testid 셀렉터** | |
| - 트리 컨테이너 | `[data-testid="tree-root"]` |
| - WP 노드 | `[data-testid="tree-node-wp"]` |
| - Task 노드 | `[data-testid="tree-node-task"]` |
| **실행 단계** | |
| 1 | `await page.goto("http://localhost:8080")` |
| 2 | `await page.wait_for_selector('[data-testid="tree-root"]')` |
| **검증 포인트** | `expect(page.locator('[data-testid="tree-root"]')).to_be_visible()` |
| **스크린샷** | `e2e-001-tree-rendered.png` |
| **관련 요구사항** | FR-001, FR-002 |

#### E2E-002: 진행률 표시 확인

| 항목 | 내용 |
|------|------|
| **파일** | `orchay/tests/e2e/test_tree.py` |
| **테스트명** | `test_wp_shows_progress_percentage` |
| **사전조건** | 트리 렌더링 완료 |
| **data-testid 셀렉터** | |
| - 진행률 | `[data-testid="wp-progress"]` |
| **검증 포인트** | `expect(page.locator('[data-testid="wp-progress"]')).to_contain_text('%')` |
| **스크린샷** | `e2e-002-progress.png` |
| **관련 요구사항** | FR-003, BR-05 |

#### E2E-003: WP 확장/축소 인터랙션

| 항목 | 내용 |
|------|------|
| **파일** | `orchay/tests/e2e/test_tree.py` |
| **테스트명** | `test_wp_expand_collapse_toggle` |
| **사전조건** | 트리 렌더링 완료, WP 축소 상태 |
| **data-testid 셀렉터** | |
| - WP 노드 | `[data-id="WP-02"]` |
| - 토글 아이콘 | `[data-testid="toggle-icon"]` |
| - 하위 노드 컨테이너 | `.children` |
| **실행 단계** | |
| 1 | `await page.click('[data-id="WP-02"]')` |
| 2 | `await page.wait_for_selector('[data-id="WP-02"] + .children.open')` |
| **검증 포인트** | `expect(page.locator('.children.open')).to_be_visible()` |
| **스크린샷** | `e2e-003-expand.png`, `e2e-003-collapse.png` |
| **관련 요구사항** | FR-004, BR-01 |

#### E2E-004: Task 선택 및 상세 로드

| 항목 | 내용 |
|------|------|
| **파일** | `orchay/tests/e2e/test_tree.py` |
| **테스트명** | `test_task_click_loads_detail` |
| **사전조건** | WP 확장됨, Task 노드 보임 |
| **data-testid 셀렉터** | |
| - Task 노드 | `[data-id="TSK-02-01"]` |
| - 상세 패널 | `[data-testid="detail-panel"]` |
| **실행 단계** | |
| 1 | `await page.click('[data-id="TSK-02-01"]')` |
| 2 | `await page.wait_for_selector('[data-testid="detail-panel"]')` |
| **API 확인** | `GET /api/detail/TSK-02-01` → 200 |
| **검증 포인트** | `expect(page.locator('[data-testid="detail-panel"]')).to_contain_text('TSK-02-01')` |
| **스크린샷** | `e2e-004-task-selected.png` |
| **관련 요구사항** | BR-02, BR-04 |

---

## 4. UI 테스트케이스 (매뉴얼)

### 4.1 테스트 케이스 목록

| TC-ID | 테스트 항목 | 사전조건 | 테스트 단계 | 예상 결과 | 우선순위 | 요구사항 |
|-------|-----------|---------|-----------|----------|---------|----------|
| TC-001 | 트리 계층 구조 | 서버 실행 | 1. 페이지 접속 | WP > Task 계층 표시 | High | FR-001, FR-003 |
| TC-002 | 상태별 색상 확인 | 다양한 상태 Task | 1. 트리 확인 | 각 상태별 색상 구분 | High | FR-002, BR-03 |
| TC-003 | 확장/축소 동작 | 트리 표시됨 | 1. WP 클릭 | 부드러운 애니메이션 | Medium | FR-004, BR-01 |
| TC-004 | 호버 상태 | 트리 표시됨 | 1. 노드에 마우스 올림 | 배경색 변경 | Medium | - |
| TC-005 | 선택 상태 | 트리 확장됨 | 1. Task 클릭 | 테두리 강조 | Medium | BR-04 |
| TC-006 | 빈 상태 | Task 없음 | 1. 페이지 접속 | 빈 상태 메시지 | Low | - |

### 4.2 매뉴얼 테스트 상세

#### TC-001: 트리 계층 구조 확인

**테스트 목적**: WBS 트리가 계층적으로 올바르게 표시되는지 확인

**테스트 단계**:
1. 웹서버 실행 후 브라우저에서 http://localhost:8080 접속
2. 좌측 패널에 WBS 트리가 표시되는지 확인
3. WP 노드들이 나열되고 각각 진행률이 표시되는지 확인
4. WP 클릭하여 하위 Task가 들여쓰기되어 표시되는지 확인

**예상 결과**:
- WP 노드에 [WP] 아이콘과 진행률(%) 표시
- Task 노드가 WP 아래 들여쓰기되어 표시
- 계층 간 시각적 구분 명확

**검증 기준**:
- [ ] WP 노드에 진행률 표시됨
- [ ] Task 노드가 들여쓰기됨 (pl-4)
- [ ] 노드 제목이 truncate 처리됨

#### TC-002: 상태별 색상 확인

**테스트 목적**: 각 Task 상태별로 올바른 색상이 표시되는지 확인

**테스트 단계**:
1. 다양한 상태의 Task가 있는 WBS 파일 준비
2. 웹 UI에서 트리 확장
3. 각 Task의 상태 배지 색상 확인

**예상 결과**:
- `[ ]` Todo → 회색 (gray-500)
- `[bd]` 기본설계 → 파란색 (blue-500)
- `[dd]` 상세설계 → 보라색 (purple-500)
- `[im]` 구현 → 노란색 (yellow-500)
- `[xx]` 완료 → 에메랄드 (emerald-500)

**검증 기준**:
- [ ] 모든 상태가 서로 다른 색상으로 구분됨
- [ ] 색상이 시각적으로 명확하게 구분됨
- [ ] 상태 코드 텍스트가 배지 안에 표시됨

#### TC-003: 확장/축소 동작 확인

**테스트 목적**: WP 노드 클릭 시 확장/축소 애니메이션이 부드럽게 동작하는지 확인

**테스트 단계**:
1. 축소된 WP 노드의 ▶ 아이콘 확인
2. WP 노드 클릭
3. 아이콘이 ▼로 변경되고 하위 노드가 슬라이드되며 나타나는지 확인
4. 다시 클릭하여 축소 확인

**예상 결과**:
- 확장 시 0.3초 슬라이드 애니메이션
- 아이콘 90도 회전 전환
- 축소 시 역방향 애니메이션

**검증 기준**:
- [ ] 애니메이션이 부드럽게 동작
- [ ] 토글 아이콘 상태 변경됨
- [ ] 끊김이나 깜빡임 없음

---

## 5. 테스트 데이터 (Fixture)

### 5.1 단위 테스트용 Mock 데이터

| 데이터 ID | 용도 | 값 |
|-----------|------|-----|
| MOCK-WP-01 | WP 노드 | `TreeNode(id="WP-01", type="wp", title="웹서버 기본 구조", progress=0.0)` |
| MOCK-WP-02 | WP 노드 (하위 있음) | `TreeNode(id="WP-02", type="wp", title="WBS 트리 UI", progress=25.0, children=[...])` |
| MOCK-TSK-01 | Task 노드 (Todo) | `TreeNode(id="TSK-02-01", type="task", title="트리 데이터 API", status="[ ]")` |
| MOCK-TSK-02 | Task 노드 (설계중) | `TreeNode(id="TSK-02-02", type="task", title="트리 템플릿 구현", status="[dd]")` |
| MOCK-TSK-03 | Task 노드 (완료) | `TreeNode(id="TSK-02-03", type="task", title="완료된 Task", status="[xx]")` |

### 5.2 E2E 테스트용 시드 데이터

| 시드 ID | 용도 | WBS 구조 |
|---------|------|----------|
| SEED-E2E-BASE | 기본 E2E 환경 | WP 4개, Task 12개 |
| SEED-E2E-EMPTY | 빈 환경 | Task 없음 |
| SEED-E2E-MULTI-STATUS | 상태 다양성 | 모든 상태별 Task 1개씩 |

### 5.3 상태 색상 매핑 테스트 데이터

| 상태 코드 | 예상 클래스 | 비고 |
|----------|------------|------|
| `[ ]` | `bg-gray-500` | 기본값 |
| `[bd]` | `bg-blue-500` | 기본설계 |
| `[dd]` | `bg-purple-500` | 상세설계 |
| `[an]` | `bg-indigo-500` | 분석 |
| `[ds]` | `bg-cyan-500` | 설계 |
| `[ap]` | `bg-green-500` | 승인 |
| `[im]` | `bg-yellow-500` | 구현 |
| `[fx]` | `bg-orange-500` | 수정 |
| `[vf]` | `bg-teal-500` | 검증 |
| `[xx]` | `bg-emerald-500` | 완료 |
| `[unknown]` | `bg-gray-500` | 미정의 상태 |

---

## 6. data-testid 목록

> 프론트엔드 요소에 적용할 `data-testid` 속성 정의

### 6.1 트리 요소 셀렉터

| data-testid | 요소 | 용도 |
|-------------|------|------|
| `tree-root` | 트리 컨테이너 | 트리 로드 확인 |
| `tree-node-wp` | WP 노드 | WP 노드 개수 확인 |
| `tree-node-act` | ACT 노드 | ACT 노드 확인 |
| `tree-node-task` | Task 노드 | Task 노드 확인 |
| `toggle-icon` | 확장/축소 아이콘 | 토글 상태 확인 |
| `status-badge` | 상태 배지 | 상태 색상 확인 |
| `wp-progress` | WP 진행률 | 진행률 표시 확인 |
| `empty-tree` | 빈 상태 | Task 없음 상태 확인 |

### 6.2 인터랙션 셀렉터

| data-testid | 요소 | 용도 |
|-------------|------|------|
| `tree-node-{id}` | 특정 노드 | 특정 노드 선택 |
| `detail-panel` | 상세 패널 | 상세 로드 확인 |

---

## 7. 테스트 커버리지 목표

### 7.1 단위 테스트 커버리지

| 대상 | 목표 | 최소 |
|------|------|------|
| Lines | 80% | 70% |
| Branches | 75% | 65% |
| Functions | 85% | 75% |
| Statements | 80% | 70% |

### 7.2 E2E 테스트 커버리지

| 구분 | 목표 |
|------|------|
| 주요 사용자 시나리오 | 100% |
| 기능 요구사항 (FR) | 100% 커버 |
| 비즈니스 규칙 (BR) | 100% 커버 |
| 에러 케이스 | 80% 커버 |

---

## 관련 문서

- 설계: `010-design.md`
- 추적성 매트릭스: `025-traceability-matrix.md`
- 트리 API 설계: `../TSK-02-01/010-design.md`

---

<!--
TSK-02-02 테스트 명세서
Version: 1.0
-->
