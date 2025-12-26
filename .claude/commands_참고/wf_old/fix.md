---
name: wf:fix
description: "결함 수정 시작. 분석 → 수정 전환"
category: workflow
complexity: complex
wave-enabled: true
performance-profile: optimized
auto-flags:
  - --c7
  - --token-efficient
  - --delegate auto
  - --task-manage
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash, Task, MultiEdit]
mcp-servers: [context7, playwright]
personas: [backend-architect, frontend-architect, quality-engineer, refactoring-expert]
hierarchy-input: true
parallel-processing: true
---

# /wf:fix - 결함 수정 시작

> **상태 전환**: `[an] 분석` → `[fx] 수정`
>
> **적용 category**: defect
>
> **계층 입력 지원**: Work Package, Activity, Task 단위 입력 가능 (WP/ACT 입력 시 하위 Task 병렬 처리)

## 사용법

```bash
/wf:fix [WP-ID | ACT-ID | Task-ID]

# Task 단위 (기존)
/wf:fix TSK-01-01-01

# Activity 단위 (ACT 내 모든 분석 완료 Task 병렬 처리)
/wf:fix ACT-01-01

# Work Package 단위 (WP 내 모든 분석 완료 Task 병렬 처리)
/wf:fix WP-01
```

## 계층 입력 처리

@.claude/includes/wf-hierarchy-input.md

### 입력 타입별 처리

| 입력 | 처리 방식 | 상태 필터 |
|------|----------|----------|
| `TSK-XX-XX-XX` | 단일 Task 처리 | `[an]` 분석 |
| `ACT-XX-XX` | ACT 내 모든 Task 병렬 처리 | `[an]` 분석 |
| `WP-XX` | WP 내 모든 Task 병렬 처리 | `[an]` 분석 |

## 상태 전환 규칙

| category | 현재 상태 | 다음 상태 | 생성 문서 |
|----------|----------|----------|----------|
| defect | `[an]` 분석 | `[fx]` 수정 | `030-implementation.md` |

## 문서 경로

@.claude/includes/wf-common.md

## 개념 충돌 해결

@.claude/includes/wf-conflict-resolution.md

**Task 폴더**: `.jjiban/projects/{project}/tasks/{TSK-ID}/`

---

## Behavioral Flow

> troubleshoot 명령어의 체계적 진단/해결 접근법 적용

1. **Analyze**: 결함 분석 문서(010-defect-analysis.md) 검토 및 수정 범위 확인
2. **Investigate**: 영향받는 코드 탐색 및 근본 원인 재확인
3. **Debug**: 수정 전략 수립 및 회귀 영향 분석
4. **Implement**: 결함 수정 코드 작성 (TDD 기반)
5. **Verify**: 수정 검증 및 회귀 테스트 실행

---

## 실행 과정

### 1단계: 결함 분석 문서 검토 및 수정 환경 준비
**Auto-Persona**: requirements-analyst
**MCP**: context7

**자동 실행 단계**:

1. **Task 정보 추출 및 파싱**:
   - Task JSON (`.jjiban/projects/{project}/tasks/{TSK-ID}/task.json`)에서 Task 정보 조회
   - category가 `defect`인지 확인
   - 현재 상태가 `[an]` 분석인지 확인

2. **결함 분석 문서 로드**:
   - `010-defect-analysis.md` 읽기
   - 추출 정보:
     - 결함 현상 및 재현 방법
     - 근본 원인 (Root Cause)
     - 영향받는 파일 목록
     - 수정 방안 및 범위
     - 회귀 테스트 범위

3. **수정 유형 분석 및 플래그 설정**:
   - **Backend 수정 여부** (`hasBackend`):
     - 영향받는 파일에 Controller, Service, Repository, API 포함
   - **Frontend 수정 여부** (`hasFrontend`):
     - 영향받는 파일에 Component, Vue, Page, UI 포함

4. **Task 유형별 실행 플로우 결정**:
   - **Backend-only** (`hasBackend=true`, `hasFrontend=false`):
     - 1단계 → **2단계** → 4단계 → 5단계
   - **Frontend-only** (`hasBackend=false`, `hasFrontend=true`):
     - 1단계 → **3단계** → 4단계 → 5단계
   - **Full-stack** (`hasBackend=true`, `hasFrontend=true`):
     - 1단계 → **2단계** → **3단계** → 4단계 → 5단계

---

### 2단계: Backend 결함 수정 (Agent 위임)
**Auto-Persona**: backend-architect
**MCP**: context7

**활성화 조건**:
- 영향받는 파일에 백엔드 코드 포함
- 결함 원인이 서버/API 로직에 있는 경우

**자동 실행 단계**:

1. **회귀 테스트 작성** (Red Phase):
   - 결함 재현 테스트 케이스 작성
   - 결함 분석 문서의 "재현 방법" 기반
   - 테스트가 **실패**하는지 확인 (결함 존재 증명)

2. **결함 수정** (Green Phase):
   - 근본 원인에 따른 코드 수정
   - 최소한의 변경으로 결함 해결
   - 기존 기능 영향 최소화

3. **코드 개선** (Refactor Phase):
   - 관련 코드 정리 (결함 재발 방지)
   - 유사 패턴 점검 및 예방적 수정

4. **회귀 테스트 실행**:
   - 결함 재현 테스트 → **통과** 확인
   - 기존 테스트 전체 실행 → 회귀 없음 확인
   - 결함 분석 문서의 "회귀 테스트 범위" 항목 수행

5. **TDD 테스트 결과 저장**:
   ```
   .jjiban/projects/{project}/tasks/{TSK-ID}/test-results/
   ├── tdd/
   │   ├── coverage/
   │   ├── test-results.json
   │   └── regression-test.json  ← 회귀 테스트 결과
   ```

**품질 기준**:
- 결함 재현 테스트 통과
- 기존 테스트 100% 통과 (회귀 없음)
- 코드 커버리지 유지 또는 향상

---

### 3단계: Frontend 결함 수정 및 E2E 검증 (Agent 위임)
**Auto-Persona**: frontend-architect
**MCP**: context7 + playwright

**활성화 조건**:
- 영향받는 파일에 프론트엔드 코드 포함
- 결함 원인이 UI/화면 로직에 있는 경우

**자동 실행 단계**:

1. **결함 재현 E2E 테스트 작성**:
   - 결함 분석 문서의 "재현 방법" 기반
   - Playwright로 결함 재현 시나리오 작성
   - 테스트가 **실패**하는지 확인

2. **Frontend 결함 수정**:
   - 컴포넌트 로직 수정
   - 상태 관리 버그 수정
   - API 연동 오류 수정

3. **E2E 테스트 실행 및 자동 수정 루프**:
   - **최대 재시도 횟수**: 5회

   ```
   🔄 E2E 테스트-수정 루프 (최대 5회)
   ┌─────────────────────────────────────────────────────────┐
   │ while (e2eAttempt < 5) {                                │
   │   e2eAttempt++                                          │
   │                                                         │
   │   1️⃣ Playwright E2E 테스트 실행                        │
   │   2️⃣ 결과 분석                                          │
   │      - if (모든 테스트 통과) → break                    │
   │      - if (실패 존재) → 수정 단계로                     │
   │   3️⃣ 실패 원인 분석 및 추가 수정                        │
   │   4️⃣ 재시도 히스토리 기록                               │
   │ }                                                       │
   │                                                         │
   │ if (e2eAttempt >= 5 && 여전히 실패) {                   │
   │   ⚠️ 경고: "E2E 테스트 5회 시도 후에도 실패"            │
   │   🛑 수동 개입 필요                                      │
   │ }                                                       │
   └─────────────────────────────────────────────────────────┘
   ```

4. **테스트 결과 저장**:
   ```
   .jjiban/projects/{project}/tasks/{TSK-ID}/test-results/
   ├── e2e/
   │   ├── e2e-test-report.html
   │   ├── e2e-test-results.md
   │   └── screenshots/
   │       └── defect-fix-*.png
   ```

**품질 기준**:
- 결함 재현 E2E 테스트 통과
- 기존 E2E 테스트 회귀 없음
- 화면 동작 정상 확인

---

### 4단계: 회귀 영향 분석 및 추가 검증
**Auto-Persona**: quality-engineer

**활성화 조건**:
- 결함 수정으로 인한 Side Effect 가능성 존재
- 연관 기능이 많은 모듈 수정

**자동 실행 단계**:

1. **영향 분석**:
   - 수정된 코드의 의존성 분석
   - 호출 관계 파악
   - 영향받을 수 있는 다른 기능 식별

2. **추가 회귀 테스트**:
   - 연관 기능 테스트 실행
   - 통합 테스트 실행

3. **결과 정리**:
   - 회귀 테스트 결과 문서화
   - Side Effect 발견 시 추가 수정

---

### 5단계: 수정 보고서 생성 및 Task 상태 업데이트
**Auto-Persona**: technical-writer

**자동 실행 단계**:

1. **수정 결과 수집**:
   - 수정된 파일 목록
   - 변경 내용 요약
   - 테스트 결과 (TDD/E2E)
   - 회귀 테스트 결과

2. **수정 보고서 작성** (`030-implementation.md`):

```markdown
# 결함 수정 보고서: [Task명]

## 문서 정보
| 항목 | 내용 |
|------|------|
| Task ID | [Task-ID] |
| Category | defect |
| 이전 상태 | [an] 분석 |
| 현재 상태 | [fx] 수정 |
| 결함 분석 문서 | 010-defect-analysis.md |
| 수정일 | [오늘 날짜] |

---

## 1. 결함 요약

### 1.1 결함 현상
[010-defect-analysis.md에서 요약]

### 1.2 근본 원인
[010-defect-analysis.md에서 요약]

---

## 2. 수정 내용

### 2.1 수정된 파일
| 파일 | 변경 유형 | 변경 내용 |
|------|----------|----------|
| [파일 경로] | 수정/추가/삭제 | [변경 설명] |

### 2.2 코드 변경 상세

#### [파일명 1]
**변경 전**:
```[언어]
[기존 코드]
```

**변경 후**:
```[언어]
[수정된 코드]
```

**변경 이유**: [왜 이렇게 수정했는지]

---

## 3. 테스트 결과

### 3.1 결함 재현 테스트
| 테스트 | 수정 전 | 수정 후 |
|--------|--------|--------|
| [결함 재현 테스트명] | ❌ Fail | ✅ Pass |

### 3.2 회귀 테스트 결과
| 범위 | 테스트 수 | 통과 | 실패 |
|------|----------|------|------|
| 단위 테스트 | [N] | [N] | 0 |
| 통합 테스트 | [N] | [N] | 0 |
| E2E 테스트 | [N] | [N] | 0 |

### 3.3 테스트 결과 파일
- TDD 결과: `test-results/tdd/test-results.json`
- E2E 결과: `test-results/e2e/e2e-test-report.html`

---

## 4. 영향 분석

### 4.1 영향받는 기능
| 기능 | 영향 | 검증 결과 |
|------|------|----------|
| [기능명] | [영향 설명] | ✅ 정상 |

### 4.2 Side Effect
- [발견된 Side Effect 또는 "없음"]

---

## 5. 재발 방지 대책

### 5.1 코드 개선
- [예방적 수정 내용]

### 5.2 권장 사항
- [향후 유사 결함 방지를 위한 권장사항]

---

## 6. 수정 완료 체크리스트

- [ ] 결함 재현 테스트 작성 완료
- [ ] 결함 수정 완료
- [ ] 결함 재현 테스트 통과
- [ ] 회귀 테스트 통과 (기존 기능 정상)
- [ ] 코드 리뷰 준비 완료

---

## 7. 다음 단계
- `/wf:audit [Task-ID]` - 코드 리뷰 (선택)
- `/wf:verify [Task-ID]` - 회귀 테스트 및 검증
```

3. **Task JSON 상태 업데이트**:
   - `[an]` → `[fx]` - Task JSON의 status 필드
   - updated_at 필드 업데이트

---

## 출력 예시

### defect (Backend 수정)
```
[wf:fix] 결함 수정 시작

Task: TSK-02-01-01
Category: defect
수정 유형: Backend-only
상태 전환: [an] 분석 → [fx] 수정

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 1단계: 결함 분석 문서 검토
├── 010-defect-analysis.md ✅
├── 결함: Null pointer exception in user service
├── 근본 원인: 사용자 조회 시 null 체크 누락
├── 영향 파일: UserService.ts, UserController.ts
└── 수정 플래그: hasBackend=true, hasFrontend=false

🔧 2단계: Backend 결함 수정 (backend-architect)
├── Red Phase: 결함 재현 테스트 작성 → ❌ Fail (결함 존재 확인)
├── Green Phase: null 체크 로직 추가
├── Refactor Phase: 유사 패턴 3곳 예방적 수정
├── 테스트 결과:
│   ├── 결함 재현 테스트: ✅ Pass (수정 완료)
│   └── 회귀 테스트: 45/45 Pass ✅
└── 커버리지: 87% (유지)

📊 품질 메트릭:
├── 결함 수정: ✅ 완료
├── 회귀 테스트: ✅ 100% Pass
└── Side Effect: 없음

📁 생성된 문서:
├── 030-implementation.md (수정 보고서)
└── test-results/
    └── tdd/
        ├── test-results.json
        └── regression-test.json

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

다음 단계:
- 코드 리뷰: /wf:audit TSK-02-01-01
- 검증: /wf:verify TSK-02-01-01
```

### defect (Full-stack 수정)
```
[wf:fix] 결함 수정 시작

Task: TSK-02-02-01
Category: defect
수정 유형: Full-stack (Backend + Frontend)
상태 전환: [an] 분석 → [fx] 수정

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 1단계: 결함 분석 문서 검토
├── 010-defect-analysis.md ✅
├── 결함: 로그인 폼 제출 시 무한 로딩
├── 근본 원인: API 응답 처리 누락 + 로딩 상태 미해제
└── 수정 플래그: hasBackend=true, hasFrontend=true

🔧 2단계: Backend 결함 수정 (backend-architect)
├── 결함 재현 테스트: API 응답 형식 검증
├── 수정: 응답 구조 정규화
└── 회귀 테스트: 30/30 Pass ✅

🎨 3단계: Frontend 결함 수정 (frontend-architect)
├── 결함 재현 E2E: 로그인 폼 무한 로딩 시나리오
├── 수정: finally 블록에 로딩 상태 해제 추가
├── 🔄 E2E 테스트-수정 루프:
│   ├── 1차 시도: 1/3 실패 → 에러 핸들링 추가
│   └── 2차 시도: 3/3 통과 ✅
└── E2E 결과: 3/3 Pass [2회 시도]

📊 품질 메트릭:
├── Backend 회귀: ✅ 100% Pass
├── Frontend E2E: ✅ 100% Pass
└── Side Effect: 없음

📁 생성된 문서:
├── 030-implementation.md
└── test-results/
    ├── tdd/
    └── e2e/
        ├── e2e-test-report.html
        └── screenshots/

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

다음 단계:
- 코드 리뷰: /wf:audit TSK-02-02-01
- 검증: /wf:verify TSK-02-02-01
```

---

## 에러 케이스

| 에러 | 메시지 |
|------|--------|
| 잘못된 category | `[ERROR] defect 카테고리만 지원합니다. 현재: [category]` |
| 잘못된 상태 | `[ERROR] 분석 완료 상태가 아닙니다. 현재 상태: [상태]` |
| 분석 문서 없음 | `[ERROR] 결함 분석 문서(010-defect-analysis.md)가 없습니다` |
| 회귀 테스트 실패 | `[WARNING] 회귀 테스트 실패: [N]건 - Side Effect 발생` |
| E2E 5회 재시도 초과 | `[ERROR] E2E 테스트 5회 시도 후에도 실패. 수동 개입 필요` |

---

## 다음 명령어

| 명령어 | 설명 |
|--------|------|
| `/wf:audit` | LLM 코드 리뷰 (상태 변경 없음, 선택) |
| `/wf:patch` | 코드 리뷰 반영 (상태 변경 없음, 선택) |
| `/wf:verify` | 회귀 테스트 및 검증 시작 |

---

## WP/ACT 단위 병렬 처리

### 병렬 처리 출력 예시

```
[wf:fix] 결함 수정 시작 (병렬 처리)

입력: WP-02 (Work Package)
범위: Defect Fixes - Sprint 3
전체 Task: 10개
대상 Task: 4개 (상태 필터: [an] 분석)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📦 병렬 처리 진행:
├── [1/4] TSK-02-01-01: NullPointer 수정 ✅ [defect] → [fx]
│   └── 회귀: 45/45 ✅ | Backend 수정
├── [2/4] TSK-02-01-02: 로그인 무한로딩 ✅ [defect] → [fx]
│   └── 회귀: 30/30 ✅ | E2E: 3/3 ✅ | Full-stack 수정
├── [3/4] TSK-02-02-01: 메모리 누수 🔄 진행중
└── [4/4] TSK-02-02-02: UI 깨짐 ⏳ 대기

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 처리 결과:
├── 성공: 2개
├── 진행: 1개
├── 대기: 1개
└── 스킵: 6개 (상태 조건 미충족)

다음 단계: /wf:verify WP-02 (또는 개별 Task별 실행)
```

---

## 최적화 특징

### 🐛 체계적 결함 수정 워크플로우
- **TDD 기반**: 결함 재현 테스트 → 수정 → 검증
- **회귀 방지**: 기존 테스트 100% 통과 필수
- **근본 원인 해결**: 분석 문서 기반 체계적 접근

### 🔄 자동 수정 루프
- E2E 테스트 실패 시 자동 재시도 (최대 5회)
- 에러 유형별 자동 수정 전략 적용

### 📊 품질 중심
- 결함 재현 테스트 통과 필수
- 회귀 테스트 100% 통과 필수
- Side Effect 분석 및 문서화

---

## 마지막 단계: 자동 Git Commit

@.claude/includes/wf-auto-commit.md

---

<!--
jjiban 프로젝트 - Workflow Command
author: 장종익
Command: wf:fix
Version: 1.0

Changes (v1.0):
- 생성: defect 카테고리의 결함 수정 워크플로우
- troubleshoot 명령어의 체계적 진단/해결 접근법 적용
- TDD 기반 회귀 테스트 및 E2E 검증 통합
-->
