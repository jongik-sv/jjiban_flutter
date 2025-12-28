# TSK-02-01 구현 보고서

## 문서 정보

| 항목 | 내용 |
|------|------|
| Task ID | TSK-02-01 |
| Task 제목 | 트리 데이터 API |
| 구현일 | 2025-12-28 |
| 상태 | 완료 |

---

## 1. 구현 개요

### 1.1 구현 목표

WBS 트리 구조를 웹 API로 제공하여 브라우저에서 Task 계층 구조를 시각화

### 1.2 주요 구현 내용

| 항목 | 파일 | 설명 |
|------|------|------|
| 트리 구조 변환 모듈 | `orchay/web/tree.py` | TreeNode 데이터클래스, 계층 변환 로직 |
| WP 하위 노드 API | `orchay/web/server.py` | GET /api/tree/{wp_id} 엔드포인트 |
| 진행률 계산 | `orchay/web/tree.py` | calculate_progress 함수 |
| 트리 템플릿 | `partials/tree.html` | TreeNode 구조 기반 렌더링 |
| WP 하위 템플릿 | `partials/wp_children.html` | WP 확장 시 하위 노드 렌더링 |

---

## 2. 구현 상세

### 2.1 tree.py 모듈

```python
@dataclass
class TreeNode:
    id: str           # WP-01, ACT-01-01, TSK-01-01
    type: str         # "wp", "act", "task"
    title: str        # 노드 제목
    status: str | None  # Task 상태 코드
    progress: float   # 진행률 (0.0-100.0)
    children: list[TreeNode]
    level: int        # 들여쓰기 레벨
```

**주요 함수:**

| 함수 | 설명 |
|------|------|
| `build_tree(tasks)` | Task 목록 → TreeNode 리스트 변환 |
| `build_wp_children(tasks, wp_id)` | 특정 WP 하위 노드만 반환 |
| `calculate_progress(tasks)` | 완료 비율 계산 |
| `parse_task_hierarchy(task_id)` | Task ID → WP/ACT/TSK 파싱 |

### 2.2 API 엔드포인트

| 엔드포인트 | 메서드 | 응답 |
|-----------|--------|------|
| `/api/tree` | GET | 전체 트리 HTML |
| `/api/tree/{wp_id}` | GET | WP 하위 노드 HTML |

**에러 처리:**
- WP 미존재 시 404 + 에러 메시지 HTML

### 2.3 템플릿 구조

```
templates/partials/
├── tree.html        # 전체 트리 (WP → ACT → Task)
└── wp_children.html # WP 하위 노드 (HTMX 파셜)
```

**진행률 표시:**
- WP 노드: `(50%)` 형식으로 우측에 표시
- ACT 노드: 동일하게 진행률 표시

---

## 3. 테스트 결과

### 3.1 단위 테스트

| TC ID | 테스트 | 결과 |
|-------|--------|------|
| TC-01 | 전체 트리 API 정상 응답 | ✅ PASS |
| TC-02 | WP 하위 노드 API 정상 응답 | ✅ PASS |
| TC-03 | 트리 구조에 진행률 포함 | ✅ PASS |
| TC-04 | 진행률 계산 정확성 | ✅ PASS |
| TC-05 | 존재하지 않는 WP 404 응답 | ✅ PASS |

### 3.2 테스트 실행

```bash
cd orchay && uv run pytest tests/test_web_server.py -v
# 결과: 13 passed in 0.54s
```

---

## 4. 요구사항 추적

| 설계 요구사항 | 구현 위치 | 테스트 |
|-------------|----------|--------|
| GET /api/tree | server.py:59-68 | TC-01 |
| GET /api/tree/{wp_id} | server.py:70-87 | TC-02, TC-05 |
| 진행률 계산 | tree.py:151-169 | TC-04 |
| TreeNode 구조 | tree.py:15-26 | TC-03 |
| WP 하위 필터링 | tree.py:122-148 | TC-02 |

---

## 5. 파일 변경 목록

| 파일 | 변경 유형 | 설명 |
|------|----------|------|
| `orchay/src/orchay/web/tree.py` | 신규 | 트리 구조 변환 모듈 |
| `orchay/src/orchay/web/server.py` | 수정 | WP 하위 API 추가, build_tree 호출 변경 |
| `orchay/src/orchay/web/templates/partials/tree.html` | 수정 | TreeNode 구조 기반 렌더링 |
| `orchay/src/orchay/web/templates/partials/wp_children.html` | 신규 | WP 하위 노드 템플릿 |
| `orchay/tests/test_web_server.py` | 수정 | TSK-02-01 테스트 추가 |

---

## 6. 제약 및 특이사항

### 6.1 설계 준수

- SSR 전용: HTMX + Jinja2 조합 유지
- 메모리 직접 참조: Orchestrator.tasks에서 직접 데이터 획득

### 6.2 개선 가능 항목

- WP/ACT 제목은 현재 ID만 표시 (WBS에 제목 정보 없음)
- 확장/축소 애니메이션은 TSK-02-03에서 구현 예정

---

## 변경 이력

| 버전 | 일자 | 변경 내용 |
|------|------|----------|
| 1.0 | 2025-12-28 | 최초 작성 |
