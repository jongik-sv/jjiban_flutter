---
subagent:
  primary: backend-architect
  conditions:
    backend: backend-architect
    frontend: frontend-architect
  description: 결함 분석 및 수정
mcp-servers: [context7, playwright]
hierarchy-input: true
parallel-processing: true
---

# /wf:fix - 결함 수정 (Lite)

> **상태 전환**: `[an] 분석` → `[fx] 수정`
> **적용 category**: defect only
> **계층 입력**: WP/ACT/Task 단위 (하위 Task 병렬 처리)

## 사용법

```bash
/wf:fix [PROJECT/]<WP-ID | ACT-ID | Task-ID>
```

| 예시 | 설명 |
|------|------|
| `/wf:fix TSK-01-01` | Task 단위 |
| `/wf:fix ACT-01-01` | ACT 내 모든 `[an]` Task 병렬 |
| `/wf:fix WP-01` | WP 내 모든 Task 병렬 |

---

## 수정 유형 판정 ⭐

| 유형 | 조건 | 실행 단계 |
|------|------|----------|
| Backend-only | 영향 파일에 Controller/Service/API 포함 | 1 → 2 → 4 → 5 |
| Frontend-only | 영향 파일에 Component/Vue/Page 포함 | 1 → 3 → 4 → 5 |
| Full-stack | 백엔드 + 프론트엔드 모두 | 1 → 2 → 3 → 4 → 5 |

---

## 실행 과정

### 1단계: 결함 분석 문서 로드

```
010-defect-analysis.md 추출:
├── 결함 현상 및 재현 방법
├── 근본 원인 (Root Cause)
├── 영향받는 파일 목록
├── 수정 방안 및 범위
└── 회귀 테스트 범위
```

### 2단계: Backend 결함 수정 (TDD) ⭐

**Red → Green → Refactor**:

```
🔴 Red Phase:
├── 결함 재현 테스트 작성
└── 테스트 실패 확인 (결함 존재 증명)

🟢 Green Phase:
├── 근본 원인에 따른 코드 수정
└── 최소한의 변경으로 해결

🔵 Refactor Phase:
├── 관련 코드 정리 (재발 방지)
└── 유사 패턴 예방적 수정
```

**회귀 테스트 실행**:
- 결함 재현 테스트 → **통과** 확인
- 기존 테스트 100% → 회귀 없음 확인

### 3단계: Frontend 결함 수정 (E2E) ⭐

**E2E 테스트-수정 루프** (최대 5회):

```
🔄 E2E 테스트-수정 루프:
├── 1️⃣ 결함 재현 E2E 테스트 작성
├── 2️⃣ Playwright 테스트 실행
├── 3️⃣ 실패 분석
│   ├── Locator 실패 → data-testid 확인
│   ├── Timeout → waitFor 추가
│   └── Network 에러 → API 연동 수정
├── 4️⃣ 코드 수정
└── 5️⃣ 재실행 (최대 5회)
```

### 4단계: 회귀 영향 분석

- 수정된 코드의 의존성 분석
- 호출 관계 파악
- Side Effect 발견 시 추가 수정

### 5단계: 수정 보고서 생성

**030-implementation.md 주요 섹션**:

| 섹션 | 내용 |
|------|------|
| 1. 결함 요약 | 현상, 근본 원인 |
| 2. 수정 내용 | 변경 파일, 코드 변경 상세 |
| 3. 테스트 결과 | 수정 전/후 비교, 회귀 결과 |
| 4. 영향 분석 | 영향 기능, Side Effect |
| 5. 재발 방지 대책 | 예방적 수정, 권장 사항 |

---

## 수정 원칙

| 원칙 | 설명 |
|------|------|
| 근본 원인 | 증상이 아닌 원인 해결 |
| 최소 변경 | 필요한 부분만 수정 |
| 테스트 추가 | 재발 방지 테스트 필수 |
| 회귀 방지 | 기존 기능 영향 없음 확인 |

---

## 출력 예시

### Backend 수정

```
[wf:fix] 결함 수정

Task: TSK-02-01-01 | Category: defect
수정 유형: Backend-only
상태 전환: [an] → [fx]

📋 결함 분석:
├── 현상: Null pointer exception in user service
├── 원인: 사용자 조회 시 null 체크 누락
└── 영향 파일: UserService.ts, UserController.ts

🔧 TDD 기반 수정:
├── 🔴 Red: 결함 재현 테스트 → ❌ Fail
├── 🟢 Green: null 체크 로직 추가
├── 🔵 Refactor: 유사 패턴 3곳 예방적 수정
└── 테스트: 결함 재현 ✅ | 회귀 45/45 ✅

📄 생성: 030-implementation.md

다음: /wf:audit 또는 /wf:verify
```

### Full-stack 수정

```
[wf:fix] 결함 수정

Task: TSK-02-02-01 | Category: defect
수정 유형: Full-stack
상태 전환: [an] → [fx]

🔧 Backend 수정:
├── 응답 구조 정규화
└── 회귀 테스트: 30/30 ✅

🎨 Frontend 수정:
├── 로딩 상태 해제 로직 추가
├── 🔄 E2E 루프: 2회 시도
│   ├── 1차: 1/3 실패 → 에러 핸들링 추가
│   └── 2차: 3/3 ✅
└── E2E: 3/3 ✅

📄 생성: 030-implementation.md

다음: /wf:audit 또는 /wf:verify
```

---

## 에러 케이스

| 에러 | 메시지 |
|------|--------|
| 잘못된 category | `[ERROR] defect만 지원합니다` |
| 잘못된 상태 | `[ERROR] 분석 상태가 아닙니다` |
| 분석 문서 없음 | `[ERROR] 010-defect-analysis.md가 없습니다` |
| 회귀 테스트 실패 | `[WARN] 회귀 테스트 실패: N건 - Side Effect 발생` |
| E2E 5회 초과 | `[ERROR] E2E 5회 시도 후 실패. 수동 개입 필요` |

---

## 다음 명령어

- `/wf:test` - 테스트 실행
- `/wf:audit` - 코드 리뷰
- `/wf:verify` - 통합테스트

---

## 공통 모듈 참조

@.claude/includes/wf-common-lite.md
@.claude/includes/wf-conflict-resolution-lite.md
@.claude/includes/wf-auto-commit-lite.md

---

<!--
wf:fix lite
Version: 1.1
-->
