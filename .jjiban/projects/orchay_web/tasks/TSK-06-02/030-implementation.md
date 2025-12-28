# TSK-06-02 - 구현 보고서

## 문서 정보

| 항목 | 내용 |
|------|------|
| Task ID | TSK-06-02 |
| Task명 | Task Detail 패널 개선 |
| 구현 완료일 | 2025-12-28 |
| 상태 | 구현 완료 |

---

## 1. 구현 요약

### 1.1 구현 범위

| 구현 항목 | 상태 | 비고 |
|----------|------|------|
| 카드 기반 섹션 분리 | ✅ | 기본정보, 진행상태, 요구사항, 기술스펙, 문서 |
| Task ID 배지 | ✅ | 프로젝트 + 카테고리 + ID |
| 워크플로우 스테퍼 | ✅ | 6단계 (시작전→설계→승인→구현→검증→완료) |
| 진행률 바 | ✅ | 상태별 0-100% |
| 요구사항 섹션 | ✅ | PRD 참조, requirements, acceptance |
| 기술 스펙 섹션 | ✅ | tech-spec, api-spec, ui-spec |
| 접기/펼치기 | ✅ | JavaScript toggle + CSS transition |

### 1.2 변경 파일

| 파일 | 변경 내용 |
|------|----------|
| `orchay/src/orchay/models/task.py` | 요구사항/기술 스펙 필드 추가 (prd_ref, requirements, acceptance, tech_spec, api_spec, ui_spec) |
| `orchay/src/orchay/wbs_parser.py` | 중첩 리스트 파싱 로직 추가, Task 생성 시 새 필드 매핑 |
| `orchay/src/orchay/web/server.py` | 워크플로우 단계/진행률 계산 함수 추가, API 응답 확장 |
| `orchay/src/orchay/web/templates/partials/detail.html` | 카드 기반 UI 전면 재구성 |
| `orchay/tests/test_web_server.py` | Mock 객체에 새 필드 추가 |

---

## 2. 설계 → 구현 매핑

### 2.1 요구사항 커버리지

| 요구사항 ID | 설계 섹션 | 구현 | 테스트 |
|------------|----------|------|--------|
| FR-001 | 5.2 기본 정보 카드 | `detail.html` basic-info-card | TC-001 |
| FR-002 | 5.2 Task ID 배지 | project-badge, category-badge, task-id-badge | TC-001 |
| FR-003 | 5.2 워크플로우 스테퍼 | workflow-stepper, step-item | TC-002 |
| FR-004 | 8.2 진행률 계산 | `get_task_progress()`, progress-bar | TC-002 |
| FR-005 | 5.2 요구사항 섹션 | requirements-section, prd-ref | TC-003 |
| FR-006 | 5.2 기술 스펙 섹션 | tech-spec-section, tech-spec-content | TC-004 |
| FR-007 | 6.1 접기/펼치기 | `toggleSection()` JavaScript | TC-005 |

### 2.2 비즈니스 규칙 구현

| 규칙 ID | 구현 |
|---------|------|
| BR-001 | `STATUS_TO_STEP` 딕셔너리로 상태 → 단계 매핑 |
| BR-002 | `STATUS_TO_PROGRESS` 딕셔너리로 상태 → 진행률 매핑 |
| BR-003 | 요구사항/기술 스펙 섹션 기본 접힘 상태 (rotate-[-90deg]) |

---

## 3. 코드 변경 상세

### 3.1 Task 모델 확장

```python
# orchay/src/orchay/models/task.py
class Task(BaseModel):
    # ... 기존 필드 ...
    # TSK-06-02: 요구사항/기술 스펙 필드
    prd_ref: str = Field(default="", description="PRD 참조 섹션")
    requirements: list[str] = Field(default_factory=list)
    acceptance: list[str] = Field(default_factory=list)
    tech_spec: list[str] = Field(default_factory=list)
    api_spec: list[str] = Field(default_factory=list)
    ui_spec: list[str] = Field(default_factory=list)
```

### 3.2 WBS 파서 확장

```python
# orchay/src/orchay/wbs_parser.py
# 중첩 리스트 파싱 로직 추가
if line.startswith("  - ") and current_list_key:
    item = line[4:].strip()
    if current_list_key not in current_task:
        current_task[current_list_key] = []
    list_val = current_task[current_list_key]
    if isinstance(list_val, list):
        list_val.append(item)
```

### 3.3 워크플로우 단계 계산

```python
# orchay/src/orchay/web/server.py
WORKFLOW_STEPS = ["시작 전", "설계", "승인", "구현", "검증", "완료"]

STATUS_TO_STEP = {
    "[ ]": 0, "[bd]": 1, "[dd]": 1, "[ap]": 2,
    "[im]": 3, "[vf]": 4, "[xx]": 5,
}

STATUS_TO_PROGRESS = {
    "[ ]": 0, "[bd]": 15, "[dd]": 25, "[ap]": 40,
    "[im]": 60, "[vf]": 80, "[xx]": 100,
}
```

### 3.4 접기/펼치기 JavaScript

```javascript
function toggleSection(button) {
    const content = button.nextElementSibling;
    const icon = button.querySelector('.toggle-icon');

    if (content.style.maxHeight && content.style.maxHeight !== '0px') {
        content.style.maxHeight = '0px';
        icon.style.transform = 'rotate(-90deg)';
    } else {
        content.style.maxHeight = content.scrollHeight + 'px';
        icon.style.transform = 'rotate(0deg)';
    }
}
```

---

## 4. 테스트 결과

### 4.1 단위 테스트

| 테스트 | 결과 |
|--------|------|
| test_wbs_parser.py (17 tests) | ✅ PASSED |
| test_web_server.py (관련 테스트) | ✅ PASSED |
| test_tree.py (32 tests) | ✅ PASSED |

### 4.2 테스트 커버리지

- 관련 테스트 109개 통과
- Mock 객체 업데이트로 새 필드 검증

---

## 5. 알려진 이슈

| 이슈 | 설명 | 대응 |
|------|------|------|
| 기존 TUI 테스트 실패 | `test_header_shows_mode` (TSK-06-02와 무관) | 향후 별도 수정 |

---

## 6. 다음 단계

- `/wf:audit`: 코드 리뷰
- `/wf:test`: 테스트 실행
- `/wf:done`: 작업 완료

---

## 변경 이력

| 버전 | 일자 | 변경 내용 |
|------|------|----------|
| 1.0 | 2025-12-28 | 최초 작성 |
