---
subagent:
  primary: system-architect
  description: 통합 설계 문서 생성 (기본설계 + 상세설계)
mcp-servers: [sequential-thinking, context7]
hierarchy-input: true
parallel-processing: true
---

# /wf:design - 통합 설계 (Lite)

> **상태 전환**: `[ ] Todo` → `[dd]`
> **적용 category**: `development`, `simple-dev`
> **계층 입력**: WP/ACT/Task 단위 (WP/ACT 입력 시 하위 Task 병렬 처리)

## 사용법

```bash
/wf:design [PROJECT/]<WP-ID | ACT-ID | Task-ID>
```

| 예시 | 설명 |
|------|------|
| `/wf:design TSK-01-01` | Task 단위 처리 |
| `/wf:design ACT-01-01` | ACT 내 모든 Todo Task 병렬 |
| `/wf:design WP-01` | WP 내 모든 Todo Task 병렬 |
| `/wf:design jjiban/TSK-01-01` | 프로젝트 명시 |

---

## 상태 전환 규칙

| category | 현재 | 다음 | 생성 문서 |
|----------|------|------|----------|
| development | `[ ]` | `[dd]` | `010-design.md` |
| simple-dev | `[ ]` | `[dd]` | `010-design.md` |

**defect, infrastructure 카테고리는 `/wf:start` 사용**

---

## 실행 과정

### Phase 1: 입력 검증

| 검증 | 확인 | 조치 |
|------|------|------|
| Task 존재 | wbs.md에서 Task ID 확인 | 없으면 에러 |
| 상태 확인 | `[ ]` Todo 상태여야 함 | 아니면 에러 |
| 카테고리 확인 | `development` 또는 `simple-dev` 여야 함 | 아니면 `/wf:start` 안내 |

### Phase 2: 컨텍스트 수집

```markdown
# WBS 예시
- [ ] **TSK-01-01**: 기능 구현 `[simple-dev]`
  - 기능 설명
  - _요구사항: PRD 3.1_
```

**추출 항목**:
- Task ID, Task명, category
- PRD 참조 섹션
- 구현 범위 (WBS Task 설명 기준)

**참조 문서 읽기**:
1. **PRD**: `.jjiban/projects/{project}/prd.md`
2. **TRD**: `.jjiban/projects/{project}/trd.md`

### Phase 3: 범위 검증

| 검증 | 확인 | 조치 |
|------|------|------|
| 누락 | Task 설명 항목 모두 포함? | 누락 추가 |
| 초과 | Task 설명에 없는 기능 포함? | 초과 제거 |
| 정합성 | PRD 내용과 일치? | PRD 기준 |

### Phase 4: 문서 생성

**생성 위치**: `.jjiban/projects/{project}/tasks/{TSK-ID}/`

| 문서 | 용도 |
|------|------|
| `010-design.md` | 통합 설계 (기본+상세) |
| `025-traceability-matrix.md` | 요구사항 추적성 |
| `026-test-specification.md` | 테스트 명세 |

**010-design.md 주요 섹션** (템플릿 참조: `.jjiban/templates/010-design.md`):

| 섹션 | 내용 |
|------|------|
| 1. 개요 | 배경, 목적, 범위 |
| 2. 사용자 분석 | 대상 사용자, 페르소나 |
| 3. 유즈케이스 | 다이어그램, 상세 |
| 4. 사용자 시나리오 | 단계별 진행 |
| 5. 화면 설계 | 와이어프레임, 흐름도 |
| 6. 인터랙션 설계 | 액션-피드백, 상태별 변화 |
| 7. 데이터 요구사항 | 필요 데이터, 관계, 유효성 |
| 8. 비즈니스 규칙 | 핵심 규칙, 상세 설명 |
| 9. 에러 처리 | 예상 에러, 표시 방식 |
| 10. 연관 문서 | 025, 026 참조 |
| 11. 구현 범위 | 영향 영역, 의존성, 제약 |
| 12. 체크리스트 | 설계 완료 확인 |

### Phase 5: 상태 전환

```bash
npx tsx .jjiban/script/transition.ts {Task-ID} design -p {project}
```

- 성공: `{ "success": true, "oldStatus": "[ ]", "newStatus": "[dd]" }`

---

## 출력 예시

```
[wf:design] 통합 설계 시작

입력: TSK-01-01
카테고리: simple-dev

📋 컨텍스트 수집 완료
├── PRD 참조: 섹션 3.1
├── TRD 참조: 확인됨
└── 범위 검증: 통과

📝 문서 생성:
├── 010-design.md ✅
├── 025-traceability-matrix.md ✅
└── 026-test-specification.md ✅

🔄 상태 전환: [ ] → [dd]

✅ 완료

다음 명령어:
- /wf:ui (선택): UI 상세 설계
- /wf:review (선택): 설계 리뷰
- /wf:approve: 설계 승인 ([dd] → [ap])
- /wf:build: 구현 시작 ([ap] → [im])
```

---

## 병렬 처리 (WP/ACT 입력)

```
[wf:design] 통합 설계 (병렬 처리)

입력: WP-01
대상 Task: 5개 ([ ] Todo + simple-dev 필터)

📦 병렬 처리:
├── [1/5] TSK-01-01 ✅ → [dd]
├── [2/5] TSK-01-02 ✅ → [dd]
├── [3/5] TSK-01-03 ✅ → [dd]
├── [4/5] TSK-02-01 ✅ → [dd]
└── [5/5] TSK-02-02 ✅ → [dd]

📊 결과: 성공 5, 실패 0, 스킵 3 (다른 category)
```

---

## 에러 케이스

| 에러 | 메시지 |
|------|--------|
| Task 없음 | `[ERROR] Task를 찾을 수 없습니다` |
| 잘못된 상태 | `[ERROR] Todo 상태가 아닙니다 (현재: {status})` |
| 잘못된 카테고리 | `[ERROR] development 또는 simple-dev 카테고리가 아닙니다. /wf:start 사용` |
| PRD 참조 없음 | `[WARN] PRD 참조를 찾을 수 없습니다` |
| 템플릿 없음 | `[ERROR] 010-design.md 템플릿을 찾을 수 없습니다` |

---

## 다음 명령어

| 명령어 | 필수 | 설명 |
|--------|------|------|
| `/wf:ui` | 선택 | UI 상세 설계 (SVG 생성) |
| `/wf:review` | 선택 | 설계 리뷰 |
| `/wf:apply` | 선택 | 리뷰 반영 |
| `/wf:approve` | **필수** | 설계 승인 (`[dd]` → `[ap]`) |
| `/wf:build` | **필수** | 구현 시작 (`[ap]` → `[im]`) |

---

## 공통 모듈 참조

@.claude/includes/wf-common-lite.md
@.claude/includes/wf-conflict-resolution-lite.md
@.claude/includes/wf-auto-commit-lite.md

---

<!--
wf:design lite
Version: 1.0
-->
