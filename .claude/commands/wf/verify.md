---
subagent:
  primary: quality-engineer
  description: 통합테스트 실행 및 검증
mcp-servers: [playwright]
hierarchy-input: true
parallel-processing: true
---

# /wf:verify - 통합테스트 (Lite)

> **상태 전환**: `[fx] 수정` → `[vf] 검증`
> **적용 category**: defect only
> **계층 입력**: WP/ACT/Task 단위 (하위 Task 병렬 처리)
>
> ⚠️ **development 카테고리는 `/wf:done`으로 바로 완료 처리하세요.**

## 사용법

```bash
/wf:verify [PROJECT/]<WP-ID | ACT-ID | Task-ID>
```

| 예시 | 설명 |
|------|------|
| `/wf:verify TSK-01-01` | Task 단위 |
| `/wf:verify ACT-01-01` | ACT 내 모든 `[im]`/`[fx]` Task 병렬 |
| `/wf:verify WP-01` | WP 내 모든 Task 병렬 |

---

## 상태 전환 규칙

| category | 현재 상태 | 다음 상태 | 생성 문서 |
|----------|----------|----------|----------|
| defect | `[fx]` 수정 | `[vf]` 검증 | `070-regression-test.md` |

---

## 실행 과정

### 1단계: 수정 완료 검증

**defect 체크리스트**:
- [ ] 구현 문서 (`030-implementation.md`) 완료
- [ ] 결함 수정 완료
- [ ] 단위 테스트 통과

### 2단계: 회귀 테스트 실행 (defect)

| 영역 | 검증 항목 |
|------|----------|
| API | 엔드포인트, 인증, 에러 처리 |
| UI | 화면 동작, 상태 변화 |
| 연동 | Frontend ↔ Backend 통신 |
| 데이터 | CRUD, 무결성, 트랜잭션 |

### 3단계: 회귀테스트 실행 (defect)

```
회귀 테스트 범위:
├── 결함 재현 테스트 → 수정됨 확인
├── 영향받는 기능 테스트 → 정상 확인
└── 새로운 이슈 점검
```

### 4단계: WBS 테스트 결과 업데이트 ⭐

```
테스트 결과 판정:
├── 모든 통합테스트 통과 → pass
└── 하나라도 실패 → fail

WBS 업데이트:
└── test-result: none → pass | fail
```

### 5단계: 상태 전환

```bash
npx tsx .jjiban/script/transition.ts {Task-ID} verify -p {project}
```
- 성공: `{ "success": true, "newStatus": "vf" }`

---

## 070-integration-test.md 주요 섹션

| 섹션 | 내용 |
|------|------|
| 1. 테스트 개요 | 범위, 환경, 대상 |
| 2. 테스트 시나리오 | 시나리오별 결과 |
| 3. API 통합 테스트 | 엔드포인트별 결과/응답시간 |
| 4. UI 통합 테스트 | 화면별 테스트 결과 |
| 5. 테스트 요약 | 통계, 발견된 이슈 |
| 6. 다음 단계 | /wf:done 안내 |

---

## 출력 예시

### development

```
[wf:verify] 통합테스트

Task: TSK-01-01-01 | Category: development
상태 전환: [im] → [vf]

구현 검증:
├── 030-implementation.md ✅
├── 단위 테스트: 15/15 ✅
└── E2E 테스트: 5/5 ✅

통합테스트:
├── 시나리오: 5/5 ✅
├── API: 12/12 ✅
└── UI: 8/8 ✅

📋 WBS 업데이트:
└── test-result: none → pass ✅

📄 생성: 070-integration-test.md

다음: /wf:done TSK-01-01-01
```

### defect

```
[wf:verify] 회귀테스트

Task: TSK-02-01-01 | Category: defect
상태 전환: [fx] → [vf]

수정 검증:
├── 030-implementation.md ✅
└── 단위 테스트: 18/18 ✅

회귀테스트:
├── 결함 수정 확인: ✅
├── 영향 기능: 10/10 ✅
└── 새 이슈: 없음

📋 WBS 업데이트:
└── test-result: none → pass ✅

📄 생성: 070-test-results.md

다음: /wf:done TSK-02-01-01
```

---

## 에러 케이스

| 에러 | 메시지 |
|------|--------|
| 잘못된 category | `[ERROR] development/defect만 지원합니다` |
| 잘못된 상태 (dev) | `[ERROR] 구현 상태가 아닙니다` |
| 잘못된 상태 (defect) | `[ERROR] 수정 상태가 아닙니다` |
| 구현 문서 없음 | `[ERROR] 030-implementation.md가 없습니다` |
| 테스트 실패 | `[ERROR] 통합테스트 실패: N건` |

---

## 다음 명령어

- `/wf:done` - 작업 완료

---

## 완료 신호

작업 완료 후 **반드시** 다음 형식으로 출력:

**성공:**
```
ORCHAY_DONE:{task-id}:verify:success
```

**실패:**
```
ORCHAY_DONE:{task-id}:verify:error:{에러 요약}
```

> ⚠️ 이 출력은 orchay 스케줄러가 작업 완료를 감지하는 데 사용됩니다. 반드시 정확한 형식으로 출력하세요.

---

## 공통 모듈 참조

@.claude/includes/wf-common-lite.md
@.claude/includes/wf-auto-commit-lite.md

---

<!--
wf:verify lite
Version: 1.1
-->
