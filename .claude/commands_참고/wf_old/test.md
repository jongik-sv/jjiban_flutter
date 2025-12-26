---
name: wf:test
description: "TDD 단위테스트 및 E2E 테스트 실행. 상태 변경 없음"
category: workflow
complexity: moderate
wave-enabled: true
performance-profile: optimized
hierarchy-input: true
parallel-processing: true
auto-flags:
  - --c7
  - --token-efficient
  - --delegate auto
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash, Task]
mcp-servers: [context7, playwright]
personas: [backend-architect, frontend-architect, quality-engineer]
---

# /wf:test - TDD 및 E2E 테스트 실행

> **테스트 전문화**: 상세설계서 기반으로 TDD 단위테스트 및 E2E 테스트를 독립적으로 실행하고 테스트 결과서를 생성합니다.
>
> **상태 전환**: 없음 (테스트만 실행, 반복 가능)
> **적용 category**: 모든 카테고리 (구현 완료 상태 이후)
> **실행 조건**: 구현 완료 상태 (`[im]`, `[fx]`) 이후에만 실행 가능

## 사용법

```bash
/wf:test [WP-ID | ACT-ID | Task-ID] [--type tdd|e2e|all]

# 예시
/wf:test TSK-01-01-01              # 단일 Task (TDD + E2E)
/wf:test TSK-01-01-01 --type tdd   # TDD 단위테스트만 실행
/wf:test TSK-01-01-01 --type e2e   # E2E 테스트만 실행
/wf:test ACT-01-01                 # Activity 내 모든 Task 병렬 처리
/wf:test WP-01                     # Work Package 내 모든 Task 병렬 처리
```

## 계층 입력 처리

@.claude/includes/wf-hierarchy-input.md

| 입력 타입 | 처리 방식 | 상태 필터 |
|-----------|----------|----------|
| `TSK-XX-XX-XX` | 단일 Task 처리 | 구현 완료 이후 상태 (카테고리별 조건 충족 시) |
| `ACT-XX-XX` | ACT 내 Task 병렬 처리 | 구현 완료 이후 상태 Task만 |
| `WP-XX` | WP 내 Task 병렬 처리 | 구현 완료 이후 상태 Task만 |

### 카테고리별 실행 가능 상태

| 카테고리 | 실행 가능 상태 | 설명 |
|----------|---------------|------|
| `development` | `[im]`, `[vf]`, `[xx]` | 구현 완료 이후 |
| `defect` | `[fx]`, `[vf]`, `[xx]` | 수정 완료 이후 |
| `infrastructure` | `[im]`, `[xx]` | 구현 완료 이후 |

## 테스트 유형

| 옵션 | 설명 | 실행 단계 |
|------|------|----------|
| `--type tdd` | Backend 단위테스트만 | 1단계 → 2단계 → 4단계 |
| `--type e2e` | Frontend E2E 테스트만 | 1단계 → 3단계 → 4단계 |
| `--type all` (기본값) | TDD + E2E 모두 | 1단계 → 2단계 → 3단계 → 4단계 |

## 문서 경로

@.claude/includes/wf-common.md

**Task 폴더**: `.jjiban/projects/{project}/tasks/{TSK-ID}/`

---

## 자동 실행 플로우

### 단계별 실행 Agent 설정

| 단계 | Agent | 활성화 조건 |
|------|-------|------------|
| TDD 테스트 | `backend-architect` | `--type tdd` 또는 `--type all` |
| E2E 테스트 | `frontend-architect` | `--type e2e` 또는 `--type all` |
| 결과 분석 | `quality-engineer` | 항상 |

---

## 실행 과정

### 1단계: 테스트 환경 준비 및 설계 분석
**Auto-Persona**: quality-engineer
**MCP**: context7

**자동 실행 단계**:

1. **Task 정보 추출 및 파싱**:
   - WBS에서 Task-ID로 Task 정보 조회
   - category 확인 (`development`, `defect`, `infrastructure`)
   - 현재 상태 확인 및 **실행 조건 검증** ⭐:
     ```
     카테고리별 실행 가능 상태 검증:
     ┌─────────────────────────────────────────────────────┐
     │ category       │ 실행 가능 상태                     │
     ├────────────────┼───────────────────────────────────┤
     │ development    │ [im], [vf], [xx]                  │
     │ defect         │ [fx], [vf], [xx]                  │
     │ infrastructure │ [im], [xx]                        │
     └─────────────────────────────────────────────────────┘

     if (현재 상태 ∉ 실행 가능 상태) {
       [ERROR] 테스트 실행 불가: {category}의 현재 상태 [{status}]
       → 구현 완료 후 테스트 실행 필요
     }
     ```

2. **설계 문서 분석** (분할된 3개 문서 로드):
   - `020-detail-design.md`: 상세설계 본문
   - `025-traceability-matrix.md`: 요구사항 추적성 매트릭스 ⭐
     - FR-XXX → 테스트 ID 매핑
     - BR-XXX → 테스트 ID 매핑
   - `026-test-specification.md`: 테스트 명세 ⭐
     - 단위 테스트 시나리오 (테스트 ID, 대상 메서드, 시나리오, 예상 결과)
     - E2E 테스트 시나리오 (테스트 ID, 사용자 액션, 검증 포인트, data-testid)
     - 테스트 데이터 명세 (Fixture 정의)
     - data-testid 셀렉터 목록

3. **기존 구현 코드 확인**:
   - Backend 코드 존재 여부 확인 (`hasBackend`)
   - Frontend 코드 존재 여부 확인 (`hasFrontend`)
   - 기존 테스트 코드 존재 여부 확인

4. **테스트 유형별 실행 플로우 결정**:
   - **TDD-only** (`--type tdd`):
     - 1단계 → **2단계** → 4단계
   - **E2E-only** (`--type e2e`):
     - 1단계 → **3단계** → 4단계
   - **All** (`--type all` 또는 기본값):
     - 1단계 → **2단계** → **3단계** → 4단계

---

### 2단계: TDD 단위테스트 실행 (Agent 위임)
**Auto-Persona**: backend-architect
**MCP**: context7

**활성화 조건**:
- `--type tdd` 또는 `--type all`
- Backend 코드가 존재하는 경우

**자동 실행 단계**:

1. **테스트 코드 생성/업데이트** (분할 문서 기반):
   - **`026-test-specification.md` 참조**: 단위 테스트 시나리오 표 기반으로 테스트 코드 생성
   - **`025-traceability-matrix.md` 참조**: 요구사항 추적성 매트릭스로 커버리지 확인
   - 테스트 시나리오 표 → Vitest 테스트 코드 변환:
     ```
     상세설계 단위 테스트 시나리오:
     | UT-001 | createProject | 정상 생성 | Project 객체 반환 |

     → 생성되는 테스트 코드:
     describe('createProject', () => {
       it('UT-001: 정상 생성 시 Project 객체 반환', async () => { ... });
     });
     ```

2. **테스트 실행 및 자동 수정 루프** ⭐:
   - **최대 재시도 횟수**: 5회 (무한 루프 방지)
   - **재시도 카운터**: `tddAttempt = 0` 초기화

   ```
   🔄 TDD 테스트-수정 루프 (최대 5회)
   ┌─────────────────────────────────────────────────────────┐
   │ while (tddAttempt < 5) {                                │
   │   tddAttempt++                                          │
   │                                                         │
   │   1️⃣ Vitest 단위테스트 실행                            │
   │      - npm run test -- --reporter=json                  │
   │      - 결과 JSON 파싱                                   │
   │                                                         │
   │   2️⃣ 결과 분석                                          │
   │      - if (모든 테스트 통과) → break (루프 종료)        │
   │      - if (실패 존재) → 3️⃣ 수정 단계로                   │
   │                                                         │
   │   3️⃣ 실패 원인 분석 및 코드 수정                        │
   │      - 실패한 테스트 ID 추출 (UT-XXX)                   │
   │      - 에러 메시지 분석:                                │
   │        • AssertionError → 비즈니스 로직 수정           │
   │        • TypeError → 타입/인터페이스 수정              │
   │        • ReferenceError → import/export 확인           │
   │        • Mock 실패 → 테스트 Mock 설정 수정             │
   │      - 스택 트레이스 분석                               │
   │      - 해당 코드 수정 후 다음 루프                      │
   │                                                         │
   │   4️⃣ 문서 동기화 (코드 수정 발생 시) ⭐                 │
   │      - 수정된 코드와 설계문서 비교                      │
   │      - 불일치 발생 시 문서 업데이트:                    │
   │        • 020-detail-design.md: API 시그니처, 로직 변경  │
   │        • 026-test-specification.md: 테스트 시나리오     │
   │        • 030-implementation.md: 구현 내용 반영          │
   │      - 변경 이력 기록 (change_log에 추가)               │
   │                                                         │
   │   5️⃣ 재시도 상태 기록                                   │
   │      - attempt_history에 시도 번호, 실패 테스트, 수정 내용 기록 │
   │ }                                                       │
   │                                                         │
   │ if (tddAttempt >= 5 && 여전히 실패) {                   │
   │   ⚠️ 경고 출력: "TDD 테스트 5회 시도 후에도 실패"       │
   │   📋 실패 테스트 목록 및 시도 히스토리 출력             │
   │   🛑 루프 종료 (수동 개입 필요)                         │
   │ }                                                       │
   └─────────────────────────────────────────────────────────┘
   ```

   **에러 유형별 자동 수정 전략**:
   | 에러 유형 | 감지 패턴 | 수정 전략 |
   |----------|----------|----------|
   | AssertionError | `expect(...).toBe` | 비즈니스 로직 확인/수정 |
   | TypeError | `Cannot read property` | 타입 정의 및 null 체크 |
   | ReferenceError | `is not defined` | import/export 확인 |
   | Mock 실패 | `mock.calls` | Mock 설정 및 반환값 수정 |
   | Async 오류 | `Promise rejected` | async/await 처리 확인 |

3. **커버리지 측정**:
   - 라인 커버리지 (목표: 80% 이상)
   - 브랜치 커버리지
   - 함수 커버리지

4. **테스트 결과 저장**:
   ```
   # 폴더명 형식: test-results/[YYYYMMDDHHmm] (예: test-results/202512081430)
   .jjiban/projects/{project}/tasks/{TSK-ID}/test-results/[timestamp]/
   ├── tdd/
   │   ├── coverage/
   │   │   ├── lcov-report/
   │   │   └── coverage-summary.json
   │   ├── test-results.json
   │   └── junit.xml
   ```

**품질 기준**:
- 테스트 커버리지 80% 이상
- 모든 단위 테스트 통과
- 상세설계 UT-XXX 시나리오 100% 반영

---

### 3단계: E2E 테스트 실행 (Agent 위임)
**Auto-Persona**: frontend-architect
**MCP**: context7 + playwright

**활성화 조건**:
- `--type e2e` 또는 `--type all`
- Frontend 코드가 존재하는 경우

**자동 실행 단계**:
0. **MCP 또는 E2E 테스트 도구** 활성화
   - **E2E 테스트 도구** : Browser 도구 또는 playwright MCP
   - 도구가 없으면 없다고 보고 하고 어떻게 할 것인지 물어볼 것

1. **E2E 테스트 코드 생성/업데이트** (분할 문서 기반):
   - **`026-test-specification.md` 참조**: E2E 테스트 시나리오 표 기반으로 테스트 코드 생성
   - **`026-test-specification.md` 섹션 6 참조**: data-testid 셀렉터 목록 활용
   - E2E 테스트 시나리오 표 → Playwright 테스트 코드 변환:
     ```
     상세설계 E2E 테스트 시나리오:
     | E2E-001 | 프로젝트 생성 버튼 클릭 | 모달 표시 | btn-create-project |

     → 생성되는 테스트 코드:
     test('E2E-001: 프로젝트 생성 버튼 클릭 시 모달 표시', async ({ page }) => {
       await page.getByTestId('btn-create-project').click();
       await expect(page.getByTestId('modal-create-project')).toBeVisible();
     });
     ```
   - **`026-test-specification.md` 섹션 5 참조**: Fixture 데이터 생성

2. **테스트 환경 준비**:
   - 개발 서버 실행 상태 확인
   - 테스트 데이터베이스 초기화
   - Fixture 데이터 로드

3. **E2E 테스트 실행 및 자동 수정 루프** ⭐:
   - **최대 재시도 횟수**: 5회 (무한 루프 방지)
   - **재시도 카운터**: `e2eAttempt = 0` 초기화

   ```
   🔄 E2E 테스트-수정 루프 (최대 5회)
   ┌─────────────────────────────────────────────────────────┐
   │ while (e2eAttempt < 5) {                                │
   │   e2eAttempt++                                          │
   │                                                         │
   │   1️⃣ Playwright E2E 테스트 실행                        │
   │      - npx playwright test --reporter=json,html         │
   │      - 결과 JSON 파싱                                   │
   │                                                         │
   │   2️⃣ 결과 분석                                          │
   │      - if (모든 테스트 통과) → break (루프 종료)        │
   │      - if (실패 존재) → 3️⃣ 수정 단계로                   │
   │                                                         │
   │   3️⃣ 실패 원인 분석 및 코드 수정                        │
   │      - 실패한 테스트 ID 추출 (E2E-XXX)                  │
   │      - 에러 메시지 분석:                                │
   │        • Locator 실패 → data-testid 확인/수정          │
   │        • Timeout → 대기 시간 조정 또는 비동기 처리     │
   │        • Assertion 실패 → 컴포넌트 로직 수정           │
   │        • Network 에러 → API 연동 코드 수정             │
   │      - 스크린샷 분석 (failure-*.png)                   │
   │      - 해당 코드 수정 후 다음 루프                      │
   │                                                         │
   │   4️⃣ 문서 동기화 (코드 수정 발생 시) ⭐                 │
   │      - 수정된 코드와 설계문서 비교                      │
   │      - 불일치 발생 시 문서 업데이트:                    │
   │        • 011-ui-design.md: UI 컴포넌트, data-testid     │
   │        • 020-detail-design.md: 컴포넌트 구조 변경       │
   │        • 026-test-specification.md: E2E 시나리오        │
   │        • 030-implementation.md: 프론트엔드 구현 내용    │
   │      - 변경 이력 기록 (change_log에 추가)               │
   │                                                         │
   │   5️⃣ 재시도 상태 기록                                   │
   │      - attempt_history에 시도 번호, 실패 테스트, 수정 내용 기록 │
   │ }                                                       │
   │                                                         │
   │ if (e2eAttempt >= 5 && 여전히 실패) {                   │
   │   ⚠️ 경고 출력: "E2E 테스트 5회 시도 후에도 실패"       │
   │   📋 실패 테스트 목록 및 시도 히스토리 출력             │
   │   🛑 루프 종료 (수동 개입 필요)                         │
   │ }                                                       │
   └─────────────────────────────────────────────────────────┘
   ```

   **에러 유형별 자동 수정 전략**:
   | 에러 유형 | 감지 패턴 | 수정 전략 |
   |----------|----------|----------|
   | Locator 실패 | `locator.click: Error` | data-testid 확인, 셀렉터 수정 |
   | Timeout | `Timeout exceeded` | waitFor 추가, 타임아웃 증가 |
   | Assertion | `expect.toBeVisible` | 컴포넌트 렌더링 로직 확인 |
   | Network | `net::ERR_` | API 엔드포인트, CORS 확인 |
   | Element 없음 | `not attached to DOM` | 조건부 렌더링 로직 수정 |

4. **테스트 결과 저장**:
   ```
   # 폴더명 형식: test-results/[YYYYMMDDHHmm] (예: test-results/202512081430)
   .jjiban/projects/{project}/tasks/{TSK-ID}/test-results/[timestamp]/
   ├── e2e/
   │   ├── e2e-test-report.html    ← HTML 시각화 보고서 (스크린샷 포함)
   │   ├── e2e-test-results.md     ← 마크다운 결과서
   │   ├── results.json
   │   ├── junit.xml
   │   └── screenshots/
   │       ├── e2e-001-*.png       ← 시나리오별 스크린샷
   │       ├── e2e-002-*.png
   │       ├── failure-*.png       ← 실패 시점 스크린샷
   │       └── trace/
   ```

5. **HTML 보고서 생성** ⭐:
   - **템플릿**: `@.jjiban/templates/e2e-html-report.html` 사용
   - **출력 파일**: `e2e-test-report.html`
   - **포함 내용**:
     - 테스트 요약 (총 테스트 수, 통과/실패/스킵)
     - 통과율 시각화 프로그레스 바
     - 시나리오별 테스트 결과 테이블
     - 실패한 테스트 상세 (에러 메시지 + 스크린샷)
     - 스크린샷 갤러리 (클릭 시 확대)
     - 요구사항 커버리지 (FR/BR 매핑)
   - **스크린샷 연동**:
     - 각 테스트 시나리오별 스크린샷 캡처
     - 실패 시 자동 스크린샷
     - HTML에서 상대 경로로 참조
   - **브라우저에서 열기**: 테스트 완료 후 `e2e-test-report.html` 열어서 결과 확인

**품질 기준**:
- 주요 사용자 시나리오 E2E 테스트 100% 통과
- 상세설계 E2E-XXX 시나리오 100% 반영
- 스크린샷/트레이스 자동 저장
- HTML 보고서에서 모든 스크린샷 정상 표시

---

### 4단계: 테스트 결과서 생성 및 아티팩트 수집
**Auto-Persona**: quality-engineer

**자동 실행 단계**:

1. **테스트 결과 수집**:
   - TDD 테스트 결과 (실행된 경우)
   - E2E 테스트 결과 (실행된 경우)
   - 커버리지 데이터

2. **테스트 결과서 작성** (Task 폴더에 저장):
   - **TDD 실행 시**: `@.jjiban/templates/070-tdd-test-results.md` 기반으로 `070-tdd-test-results.md` 생성
   - **E2E 실행 시**: `@.jjiban/templates/070-e2e-test-results.md` 기반으로 `070-e2e-test-results.md` 생성
   - 결과서 파일은 **Task 폴더 루트**에 저장 (예: `TSK-01-01-02/070-e2e-test-results.md`)

3. **테스트 아티팩트 수집 및 저장** ⭐:
   - **타임스탬프 폴더 생성**: `[Task-ID]/test-results/[YYYYMMDDHHmm]/`
   - **Playwright MCP 스크린샷 복사**:
     ```bash
     # .playwright-mcp/에서 e2e-*.png 파일을 test-results로 복사
     mkdir -p [Task-ID]/test-results/[timestamp]/e2e/screenshots/
     cp .playwright-mcp/e2e-*.png [Task-ID]/test-results/[timestamp]/e2e/screenshots/
     ```
   - **HTML 보고서 생성**:
     - 템플릿: `@.jjiban/templates/e2e-html-report.html`
     - 출력: `test-results/[timestamp]/e2e/e2e-test-report.html`
     - 스크린샷 상대 경로: `./screenshots/e2e-001-*.png`
   - **TDD 커버리지 복사** (실행 시):
     ```bash
     cp -r api/coverage/* [Task-ID]/test-results/[timestamp]/tdd/coverage/
     ```

4. **상세설계 연계 매핑**:
   - 테스트 ID → 상세설계 시나리오 매핑
   - 요구사항 커버리지 (FR/BR → 테스트 ID)
   - 미반영 시나리오 식별

5. **정리 작업**:
   - 070 결과서에 스크린샷 경로 업데이트 (상대 경로로)
   - `.playwright-mcp/` 폴더의 해당 Task 스크린샷은 복사 후 유지 (재사용 가능)

6. **문서 일관성 검증 및 최종 동기화** ⭐:
   - **코드 수정 발생 여부 확인**: 테스트-수정 루프에서 코드 변경이 있었는지 확인
   - **문서 동기화 검증** (코드 수정 시):
     | 문서 | 검증 항목 |
     |------|----------|
     | `010-basic-design.md` | 아키텍처 변경 여부 |
     | `011-ui-design.md` | UI 컴포넌트, data-testid 일치 |
     | `020-detail-design.md` | API 시그니처, 비즈니스 로직 |
     | `025-traceability-matrix.md` | 요구사항-테스트 매핑 |
     | `026-test-specification.md` | 테스트 시나리오 일치 |
     | `030-implementation.md` | 실제 구현 코드 반영 |
   - **불일치 항목 업데이트**:
     - 변경된 코드와 문서 내용 비교
     - 차이점 발견 시 문서 자동 업데이트
     - 변경 사유 및 테스트 ID 기록
   - **변경 이력 생성**:
     ```markdown
     ## 테스트 중 문서 변경 이력
     | 시각 | 문서 | 변경 내용 | 관련 테스트 |
     |------|------|----------|------------|
     | HH:mm | 020-detail-design.md | API 반환값 수정 | UT-003 |
     | HH:mm | 030-implementation.md | 에러 처리 로직 추가 | E2E-005 |
     ```
   - **최종 확인**: 모든 문서가 현재 코드와 일치하는지 검증

7. **WBS 테스트 결과 업데이트** ⭐:
   - **테스트 결과 판정**:
     - 모든 테스트 통과 → `pass`
     - 하나라도 실패 → `fail`
   - **wbs.md 업데이트**:
     - Task의 `test-result` 필드 업데이트
     - `test-result: none` → `test-result: pass` 또는 `test-result: fail`
   - **업데이트 대상**:
     - TDD 테스트 실행 시: TDD 결과 반영
     - E2E 테스트 실행 시: E2E 결과 반영
     - 둘 다 실행 시: 둘 다 통과해야 `pass`, 하나라도 실패 시 `fail`

---

## 테스트 결과서 출력 위치

### 문서 파일 (Task 폴더 루트)
| 테스트 유형 | 결과서 파일 | 경로 |
|------------|------------|------|
| TDD | `070-tdd-test-results.md` | `[Task-ID]/` |
| E2E | `070-e2e-test-results.md` | `[Task-ID]/` |

### 테스트 아티팩트 (test-results 폴더)
| 유형 | 파일 | 경로 |
|------|------|------|
| TDD 커버리지 | `coverage/` | `[Task-ID]/test-results/[timestamp]/tdd/` |
| TDD JSON | `test-results.json` | `[Task-ID]/test-results/[timestamp]/tdd/` |
| E2E HTML 보고서 | `e2e-test-report.html` | `[Task-ID]/test-results/[timestamp]/e2e/` |
| E2E 스크린샷 | `screenshots/*.png` | `[Task-ID]/test-results/[timestamp]/e2e/` |
| E2E JSON | `results.json` | `[Task-ID]/test-results/[timestamp]/e2e/` |

**타임스탬프 형식**: `YYYYMMDDHHmm` (예: `202512081430` = 2025년 12월 8일 14시 30분)

---

## 출력 예시

### TDD + E2E 모두 실행
```
[wf:test] 테스트 실행 시작

Task: TSK-01-01-01
Category: development
테스트 유형: all (TDD + E2E)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 1단계: 테스트 환경 분석
├── 020-detail-design.md ✅ (상세설계 본문)
├── 025-traceability-matrix.md ✅ (추적성 매트릭스)
├── 026-test-specification.md ✅ (테스트 명세)
│   ├── 단위 테스트 시나리오: 12건 (UT-001 ~ UT-012)
│   ├── E2E 테스트 시나리오: 8건 (E2E-001 ~ E2E-008)
│   └── 테스트 데이터 명세: 5건 (FX-001 ~ FX-005)
├── Backend 코드: ✅ 존재
└── Frontend 코드: ✅ 존재

🧪 2단계: TDD 단위테스트 (backend-architect)
├── 테스트 코드: 12개 생성/업데이트
├── 🔄 TDD 테스트-수정 루프:
│   ├── 1차 시도: 2/12 실패 → Service 로직 수정
│   │   └── 📝 문서 동기화: 020-detail-design.md (API 반환값)
│   └── 2차 시도: 12/12 통과 ✅ (루프 종료)
├── 실행 결과: 12/12 통과 (100%) [2회 시도]
├── 커버리지: 85% (목표: 80%)
│   ├── Lines: 85%
│   ├── Branches: 78%
│   └── Functions: 92%
└── 요구사항 매핑: FR 6/6, BR 6/6 ✅

🎭 3단계: E2E 테스트 (frontend-architect)
├── 테스트 코드: 8개 생성/업데이트
├── data-testid 셀렉터: 15개 활용
├── 🔄 E2E 테스트-수정 루프:
│   ├── 1차 시도: 3/8 실패 → Locator 수정
│   │   └── 📝 문서 동기화: 011-ui-design.md (data-testid 추가)
│   ├── 2차 시도: 1/8 실패 → waitFor 추가
│   │   └── 📝 문서 동기화: 030-implementation.md (비동기 처리)
│   └── 3차 시도: 8/8 통과 ✅ (루프 종료)
├── 실행 결과: 8/8 통과 (100%) [3회 시도]
├── 스크린샷: 0 failures
└── 요구사항 매핑: E2E-001~E2E-008 ✅

📊 4단계: 테스트 결과서 생성 및 아티팩트 수집
├── 070-tdd-test-results.md ✅ (Task 폴더)
├── 070-e2e-test-results.md ✅ (Task 폴더)
├── 스크린샷 복사: .playwright-mcp/ → test-results/ ✅
├── HTML 보고서 생성 ✅
├── 📝 문서 일관성 검증:
│   ├── 변경된 문서: 3개
│   │   ├── 011-ui-design.md (data-testid 2개 추가)
│   │   ├── 020-detail-design.md (API 반환값 수정)
│   │   └── 030-implementation.md (비동기 처리 추가)
│   └── 코드-문서 일치: ✅ 확인 완료
└── 📋 WBS 테스트 결과 업데이트:
    └── test-result: none → pass ✅

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 테스트 요약:
├── TDD: 12/12 (100%) ✅
├── E2E: 8/8 (100%) ✅
├── 커버리지: 85% ✅
├── 요구사항 커버리지: 100% ✅
└── 📝 문서 동기화: 3개 문서 업데이트 완료

📁 생성/수정된 파일:
├── TSK-01-01-01/
│   ├── 070-tdd-test-results.md  ← 📄 결과서 문서
│   ├── 070-e2e-test-results.md  ← 📄 결과서 문서
│   └── test-results/202512081430/
│       ├── tdd/
│       │   ├── coverage/
│       │   └── test-results.json
│       ├── e2e/
│       │   ├── e2e-test-report.html  ← 📊 브라우저에서 열기
│       │   ├── results.json
│       │   └── screenshots/
│       │       ├── e2e-001-*.png
│       │       └── e2e-002-*.png
│       └── doc-sync-log.md  ← 📝 문서 변경 이력
│
├── 📝 수정된 설계/구현 문서:
│   ├── 011-ui-design.md (data-testid 추가)
│   ├── 020-detail-design.md (API 반환값 수정)
│   └── 030-implementation.md (비동기 처리 추가)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

다음 단계:
- 테스트 실패 시: 코드 수정 후 /wf:test 재실행
- 테스트 통과 시: /wf:verify TSK-01-01-01 (통합테스트)
```

### TDD만 실행
```
[wf:test] TDD 테스트 실행 시작

Task: TSK-01-01-01
테스트 유형: tdd (단위테스트만)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 1단계: 테스트 환경 분석
├── 단위 테스트 시나리오: 12건 (UT-001 ~ UT-012)
└── Backend 코드: ✅ 존재

🧪 2단계: TDD 단위테스트
├── 실행 결과: 12/12 통과 (100%)
└── 커버리지: 85%

📊 4단계: 테스트 결과서 생성 및 아티팩트 수집
├── 070-tdd-test-results.md ✅ (Task 폴더)
└── test-results/202512081430/tdd/ ✅ (커버리지, JSON)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### E2E만 실행
```
[wf:test] E2E 테스트 실행 시작

Task: TSK-01-01-01
테스트 유형: e2e (E2E 테스트만)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 1단계: 테스트 환경 분석
├── E2E 테스트 시나리오: 8건 (E2E-001 ~ E2E-008)
└── Frontend 코드: ✅ 존재

🎭 3단계: E2E 테스트
├── 실행 결과: 8/8 통과 (100%)
└── 스크린샷: 7장 캡처

📊 4단계: 테스트 결과서 생성 및 아티팩트 수집
├── 070-e2e-test-results.md ✅ (Task 폴더)
├── 스크린샷 복사: .playwright-mcp/ → test-results/ ✅
└── test-results/202512081435/e2e/
    ├── e2e-test-report.html  ← 📊 브라우저에서 열기
    └── screenshots/ (7개 파일)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 에러 케이스

| 에러 | 메시지 |
|------|--------|
| **상태 미달 (development)** | `[ERROR] 테스트 실행 불가: development Task가 [im] 이전 상태 [{status}]입니다. /wf:build로 구현을 완료하세요.` |
| **상태 미달 (defect)** | `[ERROR] 테스트 실행 불가: defect Task가 [fx] 이전 상태 [{status}]입니다. /wf:fix로 수정을 완료하세요.` |
| **상태 미달 (infrastructure)** | `[ERROR] 테스트 실행 불가: infrastructure Task가 [im] 이전 상태 [{status}]입니다. /wf:build로 구현을 완료하세요.` |
| 설계 문서 없음 | `[ERROR] 020-detail-design.md가 없습니다` |
| 테스트 명세 없음 | `[ERROR] 026-test-specification.md가 없습니다` |
| 추적성 매트릭스 없음 | `[WARN] 025-traceability-matrix.md가 없습니다. 요구사항 커버리지 확인 제한` |
| Backend 코드 없음 (TDD) | `[WARNING] Backend 코드가 없어 TDD 테스트를 건너뜁니다` |
| Frontend 코드 없음 (E2E) | `[WARNING] Frontend 코드가 없어 E2E 테스트를 건너뜁니다` |
| 테스트 실패 | `[FAIL] 테스트 실패: [N]건 - 상세 내용은 결과서 참조` |
| 커버리지 미달 | `[WARNING] 테스트 커버리지 미달: [N]% (목표: 80%)` |
| TDD 5회 재시도 초과 | `[ERROR] TDD 테스트 5회 시도 후에도 실패. 수동 개입 필요` |
| E2E 5회 재시도 초과 | `[ERROR] E2E 테스트 5회 시도 후에도 실패. 수동 개입 필요` |

---

## WP/ACT 단위 병렬 처리

WP 또는 ACT 단위 입력 시, 해당 범위 내 **구현 완료 상태** Task들에 대해 테스트를 병렬로 실행합니다.

### 필터링 로직

```
WP/ACT 내 Task 필터링:
1. 모든 하위 Task 조회
2. 카테고리별 실행 가능 상태 필터:
   - development: [im], [vf], [xx]
   - defect: [fx], [vf], [xx]
   - infrastructure: [im], [xx]
3. 조건 충족 Task만 테스트 대상에 포함
4. 조건 미충족 Task는 스킵 (로그 출력)
```

### 출력 예시

```
[wf:test] 워크플로우 시작 (병렬 처리)

입력: WP-01 (Work Package)
범위: Core - Issue Management
대상 Task: 12개 (구현 완료 상태 필터 적용: 10개, 스킵: 2개)
테스트 유형: all (TDD + E2E)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📦 병렬 처리 진행 상황:
├── [1/10] TSK-01-01-01: Project CRUD 테스트 ✅ (TDD 12/12, E2E 5/5)
├── [2/10] TSK-01-01-02: Project 대시보드 테스트 ✅ (TDD 8/8, E2E 4/4)
├── [3/10] TSK-01-02-01: WP CRUD 테스트 🔄 진행중
├── [4/10] TSK-01-02-02: WP 계층 구조 테스트 ⏳ 대기
...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 처리 결과 요약:
├── 성공: 9개
├── 실패: 1개 (TSK-01-02-03: E2E 2건 실패)
└── 스킵: 0개

📈 통합 테스트 결과:
├── TDD 총계: 85/87 통과 (97.7%)
├── E2E 총계: 38/40 통과 (95.0%)
└── 평균 커버리지: 83%

다음 단계: 실패 Task 수정 후 재테스트
```

---

## 다음 명령어

| 상황 | 명령어 | 설명 |
|------|--------|------|
| 테스트 실패 | `/wf:test` | 코드 수정 후 재실행 |
| 테스트 통과 | `/wf:verify` | 통합테스트 시작 |
| 코드 수정 필요 | `/wf:patch` | 리뷰 내용 반영 |

---

## build 명령어와의 차이점

| 항목 | `/wf:build` | `/wf:test` |
|------|-------------|------------|
| 목적 | 구현 + 테스트 통합 | 테스트만 독립 실행 |
| 상태 전환 | `[dd]` → `[im]` | 없음 |
| 코드 생성 | 구현 코드 + 테스트 코드 | 테스트 코드만 |
| 반복 실행 | 비권장 | 권장 (반복 가능) |
| 사용 시점 | 최초 구현 시 | 테스트 재실행, 리그레션 |

---

## 마지막 단계: 자동 Git Commit

@.claude/includes/wf-auto-commit.md

---

<!--
jjiban 프로젝트 - Workflow Command
author: 장종익
Command: wf:test
Version: 1.1

Changes (v1.1):
- 모든 카테고리 지원 (development, defect, infrastructure)
- 구현 완료 상태 이후에만 실행 가능하도록 조건 추가
  - development: [im], [vf], [xx]
  - defect: [fx], [vf], [xx]
  - infrastructure: [im], [xx]
- WP/ACT 단위 실행 시 구현 완료 상태 필터링 로직 추가
- 에러 케이스에 상태 미달 에러 추가

Changes (v1.0):
- 생성
-->
