---
name: wf:build
description: "TDD 기반 Task 구현. 상세설계 → 구현 전환"
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
personas: [requirements-analyst, backend-architect, frontend-architect, quality-engineer, refactoring-expert]
hierarchy-input: true
parallel-processing: true
---

# /wf:build - TDD 기반 Task 구현

> **최적화된 구현 전문화**: 상세설계서를 바탕으로 TDD 방식으로 Task를 구현하고 구현 보고서를 자동 생성합니다.
>
> **상태 전환**: `[dd] 상세설계` → `[im] 구현` (development)
> **상태 전환**: `[dd] 상세설계` → `[im] 구현` (infrastructure)
> **적용 category**: development, infrastructure
>
> **계층 입력 지원**: Work Package, Activity, Task 단위 입력 가능 (WP/ACT 입력 시 하위 Task 병렬 처리)

## 사용법

```bash
/wf:build [WP-ID | ACT-ID | Task-ID]

# Task 단위 (기존)
/wf:build TSK-01-01-01

# Activity 단위 (ACT 내 모든 상세설계/설계 완료 Task 병렬 처리)
/wf:build ACT-01-01

# Work Package 단위 (WP 내 모든 상세설계/설계 완료 Task 병렬 처리)
/wf:build WP-01
```

## 계층 입력 처리

@.claude/includes/wf-hierarchy-input.md

### 입력 타입별 처리

| 입력 | 처리 방식 | 상태 필터 |
|------|----------|----------|
| `TSK-XX-XX-XX` | 단일 Task 처리 | `[dd]` 상세설계 |
| `ACT-XX-XX` | ACT 내 모든 Task 병렬 처리 | `[dd]` 상세설계 |
| `WP-XX` | WP 내 모든 Task 병렬 처리 | `[dd]` 상세설계 |

## 상태 전환 규칙

| category | 현재 상태 | 다음 상태 | 생성 문서 |
|----------|----------|----------|----------|
| development | `[dd]` 상세설계 | `[im]` 구현 | `030-implementation.md` |
| infrastructure | `[dd]` 상세설계 | `[im]` 구현 | `030-implementation.md` |

## 문서 경로

@.claude/includes/wf-common.md

## 개념 충돌 해결

@.claude/includes/wf-conflict-resolution.md

**Task 폴더**: `.orchay/projects/{project}/tasks/{TSK-ID}/`

---

## 자동 실행 플로우

### 단계별 실행 Agent 설정 (최적화 핵심)

| 단계 | Agent | 활성화 조건 |
|------|-------|------------|
| Backend 구현 | `backend-architect` | API/서버 로직 Task |
| Frontend 구현 | `frontend-architect` | UI/화면 Task |
| 테스트 작성 | `quality-engineer` | 조건부 |
| Refactoring | `refactoring-expert` | 필요시 |

---

## 실행 과정

### 1단계: 구현 환경 준비 및 설계 분석
**Auto-Persona**: requirements-analyst
**MCP**: context7

**자동 실행 단계**:

1. **Task 정보 추출 및 파싱**:
   - Task JSON (`.orchay/projects/{project}/tasks/{TSK-ID}/task.json`)에서 Task 정보 조회
   - category가 `development` 또는 `infrastructure`인지 확인
   - 현재 상태 확인:
     - development: `[dd]` 상세설계
     - infrastructure: `[dd]` 상세설계

2. **설계 문서 분석**:
   - **development**: 분할된 3개 문서 로드
     - `020-detail-design.md`: 상세설계 본문
     - `025-traceability-matrix.md`: 요구사항 추적성 매트릭스 ⭐
       - FR-XXX → 테스트 ID 매핑
       - BR-XXX → 테스트 ID 매핑
     - `026-test-specification.md`: 테스트 명세 ⭐ (draft 연계)
       - 단위 테스트 시나리오 (테스트 ID, 대상 메서드, 시나리오, 예상 결과)
       - E2E 테스트 시나리오 (테스트 ID, 사용자 액션, 검증 포인트, data-testid)
       - 테스트 데이터 명세 (Fixture 정의)
       - data-testid 셀렉터 목록
   - **infrastructure**: `010-tech-design.md` 로드
   - **UI Assets (화면 설계)** (Frontend 포함 Task인 경우) ⭐:
     - Task 폴더 내 `ui-assets/` 디렉토리 탐색
     - 화면 설계 이미지 로드: `*.png`, `*.jpg`, `*.svg`, `*.webp`
     - 와이어프레임, 목업, 디자인 시안 분석
     - 레이아웃 구조, 컴포넌트 배치, 색상/폰트 추출
     - 이미지 없을 경우 `011-ui-design.md` 문서 참조
   - **UI 테마 가이드** (Frontend 포함 Task인 경우):
     - `.orchay/{project}/ui-theme-*.md` 로드 (glob 패턴으로 모든 테마 파일 탐색)
     - 색상 시스템, 타이포그래피, 컴포넌트 스타일 가이드 참조
     - TRD문서의 디자인 시스템 적용 지침 확인 ⭐

3. **구현 유형 분석 및 플래그 설정**:
   - **Backend 구현 여부** (`hasBackend`):
     - Task 정보에서 "Backend", "API", "서버", "Service", "Controller" 키워드 검색
     - 상세설계서에 API 설계 또는 서버 로직 섹션 존재 확인
   - **Frontend 구현 여부** (`hasFrontend`):
     - Task 정보에서 "Frontend", "UI", "화면", "xfdl", "Nexacro", "React", "Vue" 키워드 검색
     - 상세설계서에 화면 설계 섹션 존재 확인

4. **Task 유형별 실행 플로우 결정**:
   - **Backend-only** (`hasBackend=true`, `hasFrontend=false`):
     - 1단계 → **2단계** → 4단계 → 5단계
   - **Frontend-only** (`hasBackend=false`, `hasFrontend=true`):
     - 1단계 → **3단계** → 4단계 → 5단계
   - **Full-stack** (`hasBackend=true`, `hasFrontend=true`):
     - 1단계 → **2단계** → **3단계** → 4단계 → 5단계
   - **infrastructure**: 1단계 → 2단계 (간소화) → 5단계

---

### 2단계: TDD 기반 백엔드 구현 (Agent 위임)
**Auto-Persona**: backend-architect
**MCP**: context7

**활성화 조건**:
- Task에 백엔드 구현이 포함된 경우
- 상세설계서에 API 설계 또는 서버 로직 섹션 존재

**자동 실행 단계**:

1. **테스트 우선 작성** (Red Phase) ⭐ 분할 문서 기반:
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
   - API 엔드포인트 테스트 작성 (`020-detail-design.md` 섹션 7 기반)
   - 비즈니스 로직 유닛 테스트 작성 (`020-detail-design.md` 섹션 10 BR-XXX 매핑)

2. **최소 구현** (Green Phase):
   - 중복 코드 지양 (공통코드 분리하여 재사용)
   - Controller, Service, Repository 패턴 구현 (NestJS)
   - Prisma 스키마 및 모델 구현
   - API 라우팅 및 미들웨어 구현

3. **코드 개선** (Refactor Phase):
   - 코드 품질 향상 및 중복 제거
   - 성능 최적화 및 보안 강화

4. **백엔드 테스트 실행 및 검증** (개발 중 검증용):
   - 작성된 테스트 전체 실행하여 구현 검증
   - Green Phase 통과 확인
   - ⚠️ **테스트 결과 저장은 4단계 `/wf:test` 호출에서 처리**

**품질 기준**:
- TDD 사이클 완료 (Red → Green → Refactor)
- 모든 단위 테스트 통과
- 정적 분석 통과

---

### 3단계: 프론트엔드 구현 및 E2E 검증 (Agent 위임)
**Auto-Persona**: frontend-architect (Agent 위임)
**MCP**: context7 + playwright

**활성화 조건**:
- Task에 프론트엔드 구현이 포함된 경우
- 상세설계서에 화면 설계가 존재하는 경우

**자동 실행 단계**:

1. **Frontend 화면 구현** ⭐ UI Assets + 테마 가이드 필수 참조:
   - **UI Assets 기반 구현** (Task 폴더 `ui-assets/` 참조) ⭐:
     - 화면 설계 이미지 분석 → 레이아웃 구조 파악
     - 컴포넌트 배치: 이미지 내 요소 위치 그대로 반영
     - 간격/여백: 이미지에서 추출한 spacing 값 적용
     - 색상/폰트: 이미지에서 추출 또는 테마 가이드 참조
     - 아이콘/이미지: 디자인 시안과 동일하게 적용
     - **구현 우선순위**: ui-assets 이미지 > 011-ui-design.md > 테마 가이드
   - **UI 테마 적용** (`.orchay/{project}/ui-theme-*.md` 참조):
     - 색상 시스템: Primary, Secondary, Surface, Text 색상 코드 사용
     - 컴포넌트 스타일: 버튼, 카드, 입력필드, 태그 등 가이드 준수
     - 그라디언트/글로우 효과: 정의된 CSS 클래스 활용
     - 칸반 상태 색상: 상태별 지정 색상 적용
   - TRD문서의 UI/스타일링 스택 준수
   - Pinia 상태 관리
   - 화면 간 네비게이션 구현

2. **API 연동 구현**:
   - useFetch/useAsyncData로 HTTP 클라이언트 설정
   - 데이터 송수신 로직 구현
   - 에러 처리 및 사용자 피드백

3. **E2E 테스트 코드 작성** ⭐ 분할 문서 기반:
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
   - ⚠️ **E2E 테스트 실행 및 결과 저장은 4단계 `/wf:test` 호출에서 처리**

**품질 기준**:
- UI 구현 완료 (ui-assets 기반 디자인 일치)
- API 연동 구현 완료
- E2E 테스트 코드 작성 완료

---

### 4단계: 구현 보고서 생성 및 WBS 업데이트
**Auto-Persona**: technical-writer

**자동 실행 단계**:

1. **구현 결과 수집** (Task 유형별):
   - 구현된 기능 목록 정리
   - **Backend** (2단계 실행된 경우):
     - TDD 테스트 결과 링크
     - 커버리지 리포트 경로
   - **Frontend** (3단계 실행된 경우):
     - E2E 테스트 결과 링크
     - 스크린샷 경로
   - 주요 기술적 결정사항 정리

2. **구현 보고서 작성**:
   - 아래 템플릿 활용하여 `030-implementation.md` 생성

3. **Task JSON 상태 업데이트**:
   - `[dd]` → `[im]` (development) - Task JSON의 status 필드
   - `[dd]` → `[im]` (infrastructure) - Task JSON의 status 필드
   - updated_at 필드 업데이트

---

## 구현 보고서 템플릿

> **템플릿 파일**: `@.orchay/templates/030-implementation.md`
>
> 구현 보고서는 위 템플릿을 기반으로 `030-implementation.md`를 생성합니다.

### 템플릿 주요 섹션

| # | 섹션 | 내용 |
|---|------|------|
| 0 | 문서 메타데이터 | Task ID, 참조 설계서, 구현 기간, 상태 |
| 1 | 구현 개요 | 목적, 범위, 기술 스택 |
| 2 | Backend 구현 결과 | Controller/Service/Repository, TDD 테스트 결과 |
| 3 | Frontend 구현 결과 | ui-assets 기반 화면 구성, API 연동, E2E 테스트 결과 |
| 4 | 선택적 품질 검증 | 성능/보안/접근성 (고복잡도 Task만) |
| 5 | 기술적 결정사항 | 아키텍처 결정, 구현 패턴 |
| 6 | 알려진 이슈 | 이슈 목록, 제약사항, 향후 개선 |
| 7 | 구현 완료 체크리스트 | Backend/Frontend/통합 체크 |
| 8 | 참고 자료 | 관련 문서, 테스트 결과 파일, 소스 위치 |

### 상세설계 연계 필수 항목 ⭐

구현 보고서 작성 시 **분할된 설계 문서 연계 정보**를 반드시 포함:

**섹션 2.2 TDD 테스트 결과** (`026-test-specification.md` 기반):
```markdown
#### 상세설계 테스트 시나리오 매핑
| 테스트 ID | 상세설계 시나리오 | 결과 | 비고 |
|-----------|------------------|------|------|
| UT-001 | createProject 정상 생성 | ✅ Pass | |
| UT-002 | createProject 중복 이름 | ✅ Pass | BR-001 검증 |
```

**섹션 3.3 E2E 테스트 결과** (`026-test-specification.md` 기반):
```markdown
#### 상세설계 E2E 시나리오 매핑
| 테스트 ID | 상세설계 시나리오 | data-testid | 결과 |
|-----------|------------------|-------------|------|
| E2E-001 | 프로젝트 생성 버튼 클릭 | btn-create-project | ✅ Pass |
| E2E-002 | 모달에서 이름 입력 | input-project-name | ✅ Pass |
```

**요구사항 커버리지** (`025-traceability-matrix.md` 기반):
```markdown
#### 요구사항 커버리지
| 요구사항 ID | 테스트 ID | 결과 | 비고 |
|-------------|-----------|------|------|
| FR-001 | UT-001, E2E-001 | ✅ | |
| BR-001 | UT-002 | ✅ | 중복 이름 검증 |
```

### 다음 단계

구현 보고서 작성 완료 후:
- `/wf:test [Task-ID]` - 테스트 실행 (TDD/E2E)
- `/wf:audit [Task-ID]` - LLM 코드 리뷰 실행 (선택)
- `/wf:patch [Task-ID]` - 리뷰 내용 반영 (선택)
- `/wf:verify [Task-ID]` - 통합테스트 시작

---

## 출력 예시

### development (Full-stack)
```
[wf:build] TDD 기반 구현 시작

Task: TSK-01-01-01
Category: development
구현 유형: Full-stack (Backend + Frontend)
상태 전환: [dd] 상세설계 → [im] 구현

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 1단계: 설계 분석 (분할 문서 연계)
├── 020-detail-design.md ✅ (상세설계 본문)
├── 025-traceability-matrix.md ✅ (추적성 매트릭스)
│   ├── FR-XXX → 테스트 ID 매핑: 6개
│   └── BR-XXX → 테스트 ID 매핑: 6개
├── 026-test-specification.md ✅ (테스트 명세)
│   ├── 단위 테스트 시나리오: 12건 (UT-001 ~ UT-012)
│   ├── E2E 테스트 시나리오: 8건 (E2E-001 ~ E2E-008)
│   ├── 테스트 데이터 명세: 5건 (FX-001 ~ FX-005)
│   └── data-testid: 15개 정의됨
├── ui-assets/ ✅ (화면 설계 이미지) ⭐
│   ├── 이미지 파일: 3개 (main.png, modal.png, list.png)
│   ├── 레이아웃 구조 분석 완료
│   └── 컴포넌트 배치 정보 추출
├── ui-theme-dark.md ✅ (UI 테마 가이드)
│   ├── 색상 시스템: Primary(Purple), Surface(Dark) 정의
│   ├── 컴포넌트 스타일: 버튼, 카드, 입력필드 등
│   └── UI/스타일링 스택 적용 지침
└── 구현 플래그: hasBackend=true, hasFrontend=true

🔧 2단계: Backend 구현 (java-developer)
├── Red Phase: 상세설계 UT-001~UT-012 기반 테스트 작성
├── Green Phase: Controller/Service/Repository 구현
├── Refactor Phase: 중복 제거 완료
├── 테스트 결과: 12/12 통과 (100%)
├── 요구사항 커버리지: FR 6/6, BR 6/6 ✅
└── 코드 커버리지: 85%

🎨 3단계: Frontend 구현 (frontend-architect)
├── UI Assets 기반 구현 ✅ ⭐
│   ├── 화면 설계 이미지 분석: 3개 (main.png, modal.png, list.png)
│   ├── 레이아웃: 이미지 기준 그리드/플렉스 구조 반영
│   └── 컴포넌트 배치: 디자인 시안과 동일하게 구현
├── UI 테마 적용: ui-theme-dark.md 기반 ✅
│   ├── 색상: Primary(#8b5cf6), Surface(#121218) 적용
│   ├── 컴포넌트: Card, Button, Input 스타일 준수
│   └── TailwindCSS 확장 클래스 활용
├── Vue 컴포넌트: 5개 생성
├── Pinia Store: 2개 생성
├── E2E 테스트 코드 작성: 상세설계 E2E-001~E2E-008 기반
│   ├── data-testid 셀렉터 15개 활용
│   └── Fixture: FX-001~FX-005 기반 생성
└── API 연동: useFetch 활용

🧪 4단계: 테스트 실행 (/wf:test 호출) ⭐
├── wf:test subagent 호출: /wf:test TSK-01-01-01 --type all
├── 🔄 TDD 테스트-수정 루프:
│   ├── 1차 시도: 2/12 실패 → Service 로직 수정
│   └── 2차 시도: 12/12 통과 ✅ (루프 종료)
├── TDD 결과: 12/12 통과 (100%) [2회 시도]
├── 🔄 E2E 테스트-수정 루프:
│   ├── 1차 시도: 3/8 실패 → Locator 수정
│   ├── 2차 시도: 1/8 실패 → waitFor 추가
│   └── 3차 시도: 8/8 통과 ✅ (루프 종료)
├── E2E 결과: 8/8 통과 (100%) [3회 시도]
└── 테스트 결과서 생성 완료

📊 품질 메트릭:
├── TDD 커버리지: 85% ✅ (목표: 80%)
├── E2E 통과율: 100% ✅ (목표: 100%)
├── 요구사항 커버리지: 100% ✅ (FR 6/6, BR 6/6)
└── 정적 분석: Pass ✅

📁 생성된 문서:
├── 030-implementation.md
│   └── 상세설계 테스트 시나리오 ↔ 실제 테스트 매핑 표 포함
├── 070-tdd-test-results.md ← wf:test가 생성
├── 070-e2e-test-results.md ← wf:test가 생성
└── test-results/[timestamp]/
    ├── tdd/
    │   ├── coverage/
    │   └── test-results.json
    └── e2e/
        ├── e2e-test-report.html  ← 📊 브라우저에서 열기
        ├── results.json
        └── screenshots/

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

다음 단계:
- 코드 리뷰: /wf:audit TSK-01-01-01
- 통합테스트: /wf:verify TSK-01-01-01
```

### infrastructure
```
[wf:build] 구현 시작

Task: TSK-03-01-01
Category: infrastructure
상태 전환: [dd] 상세설계 → [im] 구현

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 1단계: 설계 분석
└── 010-tech-design.md ✅

🔧 2단계: 구현
├── 설정 파일 생성
├── 스크립트 작성
└── 환경 검증 완료

📁 생성된 문서:
└── 030-implementation.md

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

다음 단계:
- 코드 리뷰: /wf:audit TSK-03-01-01
- 작업 완료: /wf:done TSK-03-01-01
```

---

## 에러 케이스

| 에러 | 메시지 |
|------|--------|
| 잘못된 category | `[ERROR] development 또는 infrastructure만 지원합니다` |
| 잘못된 상태 (dev) | `[ERROR] 상세설계 상태가 아닙니다. 현재 상태: [상태]` |
| 잘못된 상태 (infra) | `[ERROR] 상세설계 상태가 아닙니다. 현재 상태: [상태]` |
| 설계 문서 없음 | `[ERROR] 설계 문서가 없습니다` |
| UI Assets 없음 | `[INFO] ui-assets/ 폴더 없음. 011-ui-design.md 또는 테마 가이드 참조` |
| 테스트 실패 | `[WARNING] 테스트 커버리지 미달: [N]% (목표: 80%)` |
| E2E 실패 | `[WARNING] E2E 테스트 실패: [N]건` |
| E2E 5회 재시도 초과 | `[ERROR] E2E 테스트 5회 시도 후에도 실패. 수동 개입 필요` |
| TDD 5회 재시도 초과 | `[ERROR] TDD 테스트 5회 시도 후에도 실패. 수동 개입 필요` |

---

## 다음 명령어

| category | 명령어 | 설명 |
|----------|--------|------|
| development | `/wf:audit` | LLM 코드 리뷰 (상태 변경 없음) |
| development | `/wf:patch` | 코드 리뷰 반영 (상태 변경 없음) |
| development | `/wf:verify` | 통합테스트 시작 |
| infrastructure | `/wf:audit` | LLM 코드 리뷰 (상태 변경 없음) |
| infrastructure | `/wf:patch` | 코드 리뷰 반영 (상태 변경 없음) |
| infrastructure | `/wf:done` | 작업 완료 |

---

## 최적화 특징

### ⚡ 에이전트 위임 효율성
- 도메인별 전문 에이전트 자동 배정
- 병렬 처리 가능한 작업 분리
- 각 에이전트의 강점 활용 극대화

### 🧪 TDD + E2E 통합 워크플로우
- **Backend**: TDD로 단위/통합 테스트 (2단계)
- **Frontend**: Playwright E2E로 연동 검증 (3단계)
- **Task 유형별 워크플로우**:
  - Backend-only: 2단계만 실행
  - Frontend-only: 3단계만 실행
  - Full-stack: 2단계 → 3단계 통합 실행

### 📊 품질 중심
- 각 단계에서 품질 보증 완료
- **Backend Task**: 테스트 커버리지 80% 이상
- **Frontend Task**: ui-assets 기반 디자인 일치도 + E2E 주요 시나리오 100% 통과
- **Full-stack Task**: 양쪽 품질 기준 모두 충족

### 🎨 UI Assets 기반 구현
- Task 폴더 내 `ui-assets/` 화면 설계 이미지 우선 참조
- 이미지 분석 → 레이아웃, 컴포넌트 배치, 색상/폰트 추출
- 디자인 시안과 실제 구현 일치도 극대화
- Fallback: `011-ui-design.md` → `ui-theme-*.md`

---

## WP/ACT 단위 병렬 처리

### 병렬 처리 출력 예시

```
[wf:build] TDD 기반 구현 시작 (병렬 처리)

입력: WP-01 (Work Package)
범위: Core - Issue Management
전체 Task: 15개
대상 Task: 6개 (상태 필터: [dd] 상세설계)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📦 병렬 처리 진행:
├── [1/6] TSK-01-01-01: Project CRUD 구현 ✅ [development] → [im]
│   └── TDD: 12/12 ✅ | E2E: 8/8 ✅ | Coverage: 85%
├── [2/6] TSK-01-01-02: Project 대시보드 ✅ [development] → [im]
│   └── TDD: 8/8 ✅ | E2E: 5/5 ✅ | Coverage: 82%
├── [3/6] TSK-01-02-01: WP CRUD 구현 ✅ [development] → [im]
│   └── TDD: 10/10 ✅ | E2E: 6/6 ✅ | Coverage: 88%
├── [4/6] TSK-01-02-02: WP 계층 관리 🔄 진행중
├── [5/6] TSK-01-03-01: ACT CRUD 구현 ⏳ 대기
└── [6/6] TSK-01-03-02: ACT 정렬 기능 ⏳ 대기

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 처리 결과:
├── 성공: 3개
├── 진행: 1개
├── 대기: 2개
└── 스킵: 9개 (상태 조건 미충족)

다음 단계: /wf:audit WP-01 (또는 개별 Task별 실행)
```

---

## 마지막 단계: 자동 Git Commit

@.claude/includes/wf-auto-commit.md

---

<!--
orchay 프로젝트 - Workflow Command
author: 장종익
Command: wf:build
Version: 1.0

Changes (v1.0):
- 생성
-->
