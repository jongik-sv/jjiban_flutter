# EPIC을 Chain으로 분리하는 명령어

EPIC PRD 문서를 분석하여 **Chain 단위 (1-3개월 배포 가능 Feature)**로 분리하고, Chain 폴더 구조를 생성합니다.

## ⚠️ 중요 지침

**이 명령어는 Chain 레벨 문서화 작업 전용입니다:**
- ✅ EPIC PRD 분석 및 Chain 분할
- ✅ Chain PRD 문서 생성
- ✅ Chain 기본설계 문서 생성
- ✅ Chain 레벨 폴더 구조 생성
- ✅ 의존성 분석 및 매핑
- ❌ **Module 폴더/문서 생성 금지** - Chain 레벨까지만
- ❌ **코드 작성 금지** - 구현은 별도 명령어 사용
- ❌ **코드 생성 금지** - 설계 문서만 작성

---

## 📊 Chain 개념

### Chain-Level 정의

**Chain = Feature = 출시 가능한 기능 단위 (1-3개월)**

| 레벨 | 크기 | 목적 | 예시 |
|------|------|------|------|
| **EPIC-Level** | 3-6개월 | 전략적 비즈니스 역량 | "orchay - AI-Assisted Kanban Tool" |
| **Chain-Level** | 1-3개월 | 실행 가능한 Feature | "Core Project Management System" |
| **Module-Level** | 1-4주 | User Story | "칸반 보드 UI" |
| **Task-Level** | 1-5일 | 구현 작업 | "드래그 앤 드롭 구현" |

### Chain 크기 가이드라인

**적절한 Chain 크기 (✅ 1-3개월 규모)**:
```
✅ CHAIN-01: Core Project Management (2-3개월)
   ├── 칸반 보드 (드래그 앤 드롭, 필터링, 검색)
   ├── Gantt 차트 (타임라인, 계층 구조)
   └── Task 상세 화면 (문서 연동, 편집)
→ 독립적으로 배포 가능한 기능 묶음

✅ CHAIN-02: LLM Integration & Automation (2-3개월)
   ├── 웹 터미널 (xterm.js, WebSocket)
   ├── LLM 명령어 실행 (Claude, Gemini)
   └── 워크플로우 자동화 (Auto-Pilot)
→ 비즈니스 가치를 제공하는 기능 세트
```

**너무 작은 경우 (❌ Module 수준)**:
```
❌ CHAIN-01: 칸반 보드 (1-2주)
   └── 단일 UI 컴포넌트
→ 문제: Chain이 Module 수준으로 너무 작음

해결: "Core Project Management"로 통합
```

---

## 🎯 MECE 원칙 (Mutually Exclusive, Collectively Exhaustive)

### MECE 개념

**MECE는 효과적인 분할을 위한 핵심 원칙입니다:**

- **Mutually Exclusive (상호 배타적)**: 각 Chain이 **겹치지 않음**
- **Collectively Exhaustive (전체를 포괄)**: 모든 기능이 **어떤 Chain에든 포함됨**

```
❌ MECE 위반 (겹침 + 빠짐):
CHAIN-01: 프로젝트 관리 (칸반, Gantt, Task)
CHAIN-02: 칸반 보드 (프로젝트 내 일부)
CHAIN-03: 자동화 (워크플로우만)
→ "칸반"이 CHAIN-01, CHAIN-02에 겹침
→ "문서 관리" 누락

✅ MECE 준수 (겹치지 않음 + 빠지지 않음):
CHAIN-01: Platform Foundation (Portal, 디자인시스템, DB, 인증)
CHAIN-02: Core Project Management (칸반, Gantt, Task 상세)
CHAIN-03: Workflow & Automation (워크플로우, 자동화)
CHAIN-04: Document Management (문서, 템플릿, WBS)
→ 각 Chain이 명확하게 구분됨
→ EPIC의 모든 기능이 포함됨
```

### Chain 분할에서의 MECE 적용

#### 1. 상호 배타적 (Mutually Exclusive)

**각 Chain은 명확하게 구분되어야 함:**

```markdown
**기능 영역별 경계 설정**:
- 칸반 보드 기능 전체 → CHAIN-02에만 포함
- 자동화 기능 전체 → CHAIN-03에만 포함
- 문서 기능 전체 → CHAIN-04에만 포함

**기능 중복 예방**:
❌ "Task 상세" → CHAIN-02와 CHAIN-03 모두에 포함 (겹침)
✅ "Task 상세" → CHAIN-02에만 포함 (명확한 소속)

**특정 기능이 여러 Chain에 필요한 경우**:
→ 해당 기능을 CHAIN-01 (Platform Foundation)에 포함
→ 모든 Chain에서 공유 가능하게 설계
```

#### 2. 전체를 포괄 (Collectively Exhaustive)

**EPIC의 모든 기능이 어떤 Chain에든 포함:**

```markdown
**체크리스트: EPIC PRD의 모든 섹션이 커버되었나?**

Section 2.1: 이슈 타입 체계
→ CHAIN-01 (Platform Foundation)에 포함

Section 2.2: 워크플로우 체계
→ CHAIN-03 (Workflow & Automation)에 포함

Section 3.1: 칸반 보드
→ CHAIN-02 (Core Project Management)에 포함

...모든 섹션이 어떤 Chain에든 할당됨
```

### MECE 검증 체크리스트

분할 완료 후 다음을 확인하세요:

```markdown
## 상호 배타적 검증

□ 각 Chain의 주요 기능이 명확하게 정의되었는가?
□ 기능이 여러 Chain에 중복되지 않는가?
□ Chain 간의 경계가 명확한가?

**기능 중복 검사 (5분)**:
1. PRD에서 각 주요 기능 추출
2. 해당 기능이 포함된 Chain 확인
3. 1개 Chain에만 포함되었나? 확인

## 전체를 포괄 검증

□ EPIC PRD의 모든 섹션이 어떤 Chain에 할당되었는가?
□ 프로젝트에 필수적인 요소(인증, DB, UI시스템)가 모두 포함되었는가?
□ 빠진 기능이 없는가?

**누락 검사 (5분)**:
1. EPIC PRD의 모든 섹션 목록화
2. 각 섹션이 어떤 Chain에 포함되었는지 매핑
3. 미할당 섹션이 있나? 확인

## 실제 예시

**❌ MECE 위반 사례**:
```
CHAIN-01: Platform Foundation
  - Portal & 레이아웃
  - 디자인 시스템
  - 인증 (기본)

CHAIN-02: Project Management
  - 칸반 보드
  - Task 상세
  - 워크플로우 (일부)

CHAIN-03: Automation
  - 워크플로우 (일부)  ← 겹침!
  - 자동화

누락: 문서 관리 기능 없음
```

**✅ MECE 준수 사례**:
```
CHAIN-01: Platform Foundation
  - Portal & 레이아웃
  - 디자인 시스템
  - 데이터베이스 스키마
  - 인증 & 권한 관리
  - 기본 설정 & 로깅

CHAIN-02: Project Management
  - 칸반 보드
  - Gantt 차트
  - Task 상세 화면
  - 문서 연동

CHAIN-03: Workflow & Automation
  - 워크플로우 설정
  - 상태 전환
  - 자동화 규칙
  - 템플릿 기반 자동화

CHAIN-04: Document Management
  - 문서 CRUD
  - 템플릿 관리
  - WBS 구조
  - 버전 관리
```
```

---

## 비즈니스 요구사항 중심 분할 원칙

### 1. 기능 영역 그룹핑

**비즈니스 기능 도메인으로 그룹핑**

예시:
- **프로젝트 관리**: 칸반 + Gantt + Task 상세 → Chain
- **LLM 자동화**: 터미널 + 명령어 + 워크플로우 → Chain
- **문서 엔진**: 문서 관리 + 템플릿 + WBS → Chain
- **플랫폼 기반**: Portal + 디자인 시스템 + DB → Chain

### 2. 배포 가능성 우선

**각 Chain이 독립적으로 배포 가능한 가치 제공**

### 3. 사용자 시나리오 기반

**사용자 여정과 워크플로우를 고려한 분할**

### 4. Chain 개수 제한

**⚠️ 중요: EPIC당 3-7개 Chain**
- 너무 많으면 → 관리 복잡
- 너무 적으면 → Chain이 너무 거대

---

## 사전 요구사항

사용자에게 다음 정보를 요청하세요:
1. **EPIC PRD 파일 경로** (예: `projects/orchay/orchay-prd.md`)
2. **EPIC 폴더명** (예: `projects/orchay/`)
3. **Chain 분류 방식** (자동 추론 또는 수동 지정)

---

## 실행 단계

### 1단계: EPIC PRD 분석

1. EPIC PRD 파일 읽기
2. 문서 구조 파악 (섹션, 헤더 레벨)
3. 주요 **기능 영역** 식별:
   - 섹션 헤더 (## 또는 ###)
   - 키워드 패턴 분석
   - 논리적 그룹핑

### 2단계: Chain 추출

#### 2-1. 기능 영역 키워드 매칭

**기능 영역 키워드:**
- **플랫폼/인프라**: "Portal", "레이아웃", "디자인 시스템", "DB", "스키마", "사용자 관리", "인증", "보안", "DevOps", "설정"
- **프로젝트 관리**: "칸반", "Kanban", "Gantt", "차트", "Task 상세", "이슈", "백로그", "마일스톤"
- **워크플로우**: "워크플로우", "Workflow", "상태", "전환", "자동화", "프로세스"
- **문서 관리**: "문서", "Document", "템플릿", "Template", "WBS", "폴더 구조"
- **LLM/AI**: "LLM", "AI", "터미널", "Terminal", "자동화", "Automation", "Claude", "Gemini"
- **배포/CLI**: "배포", "Deployment", "CLI", "npm", "Docker", "설치"

#### 2-2. Chain 후보 추출

PRD 섹션을 분석하여 Chain 후보 생성:

**예시 (orchay PRD 기준)**:
```
Section 2.1-2.3: 핵심 개념
→ CHAIN-01: Platform Foundation
  - 이슈 타입 체계
  - 워크플로우 체계
  - 문서 관리 체계

Section 3.1-3.3: 사용자 기능
→ CHAIN-02: Core Project Management
  - 칸반 보드
  - Gantt 차트
  - Task 상세 및 문서 연동

Section 3.4-3.5: LLM 통합
→ CHAIN-03: LLM Integration & Automation
  - LLM 통합 웹 터미널
  - 워크플로우 자동화

Section 4: 시스템 아키텍처
→ CHAIN-01에 통합 (플랫폼 기반)

Section 5: 배포 및 설치
→ CHAIN-04: Deployment & CLI Tools
  - npm CLI 패키지
  - Docker 지원
```

#### 2-3. Chain 크기 검증

각 Chain 후보를 다음 기준으로 검증:

**✅ 적절한 Chain 기준:**
- 예상 기간: 1-3개월
- 포함 Module 수: 2-5개 (각 1-4주)
- 비즈니스 가치: 독립적으로 배포 가능
- 사용자 시나리오: 완전한 사용자 여정 제공

**❌ Module로 강등 기준:**
- 예상 기간: 1-2주 (너무 작음)
- 단일 화면/기능
- 다른 Chain 없이는 가치 제공 불가

**통합 필요 신호:**
```
만약 다음 패턴이 보이면 통합 고려:
- UI 화면 3개 이상이 개별 Chain → "Project Management" Chain으로 통합
- 관리 기능 여러 개가 개별 Chain → "Core Management" Chain으로 통합
- 인프라 관련 여러 개 → "Platform Foundation" Chain으로 통합
```

### 2-4. Platform Chain (CHAIN-01) 자동 생성

**⚠️ 중요: 모든 프로젝트는 CHAIN-01을 Platform Foundation으로 자동 생성**

**Platform Chain 정의:**
- 기능적 요구사항에는 명시되지 않았지만 시스템이 작동하기 위해 **반드시 필요한 기반 요소**
- 항상 **CHAIN-01**로 생성되며, 모든 다른 Chain의 선행 조건
- PRD에 명시적으로 언급되지 않더라도 자동으로 생성

**CHAIN-01 (Platform Foundation)에 포함되어야 하는 필수 요소:**

1. **Portal & 레이아웃 시스템**
   - 전역 헤더 (Global Header)
   - 사이드바 네비게이션 (Sidebar Navigation)
   - 메인 레이아웃 템플릿 (Layout Templates)
   - 라우팅 시스템

2. **디자인 시스템 & 공통 컴포넌트**
   - 색상 팔레트 (Color Palette)
   - 타이포그래피 (Typography)
   - 공통 UI 컴포넌트 라이브러리 (Button, Input, Modal 등)
   - 아이콘 시스템

3. **데이터베이스 스키마**
   - Prisma Schema 정의
   - 마이그레이션 설정
   - 기본 시드 데이터

4. **사용자 관리 & 인증**
   - User 테이블 및 모델
   - 로그인/로그아웃 시스템
   - JWT 토큰 관리
   - 세션 관리
   - RBAC (Role-Based Access Control)

5. **시스템 설정, 로깅, 에러 처리**
   - 환경 변수 설정 (`.env`)
   - 설정 파일 관리 (config.json)
   - 로깅 시스템 (Winston, Pino 등)
   - 전역 에러 핸들러
   - 에러 바운더리 (Frontend)

6. **보안**
   - CORS 설정
   - Helmet.js (보안 헤더)
   - XSS 방지
   - CSRF 토큰
   - Rate Limiting

7. **DevOps & 인프라**
   - Git 전략 및 브랜치 정책
   - CI/CD 파이프라인 설정
   - 배포 스크립트
   - 환경별 설정 (dev, staging, prod)

**Platform Chain 체크리스트:**
```
PRD 분석 시 다음을 자동으로 체크하고 누락 시 CHAIN-01에 추가:
- [ ] Portal & 레이아웃 시스템
- [ ] 디자인 시스템 & 공통 컴포넌트
- [ ] 데이터베이스 스키마
- [ ] 사용자 관리 & 인증
- [ ] 시스템 설정, 로깅, 에러 처리
- [ ] 보안
- [ ] DevOps & 인프라
```

**Platform Chain 생성 프로세스:**
1. PRD를 분석하여 위 7가지 영역의 언급 여부 확인
2. PRD에서 발견된 요소를 CHAIN-01에 포함
3. 누락된 필수 요소는 자동으로 CHAIN-01에 추가
4. CHAIN-01은 항상 다른 모든 Chain의 선행 조건으로 설정

---

## Chain 네이밍 규칙

### Chain ID 형식
- **ID 형식**: `CHAIN-{epic-id}-{01-99}`
- **폴더명**: `CHAIN-{epic-id}-{number}-{kebab-case-name}`
- **예시**:
  - `CHAIN-orchay-01-platform-foundation`
  - `CHAIN-orchay-02-core-project-management`
  - `CHAIN-orchay-03-llm-integration`

---

## 폴더 구조

**⚠️ 이 명령어는 Chain 레벨까지만 생성합니다. Module은 chain-prd.md에 정의만 하고 폴더는 생성하지 않습니다.**

```
projects/
└── orchay/                                          # EPIC 폴더
    ├── orchay-prd.md                                # EPIC PRD
    │
    ├── CHAIN-orchay-01-platform-foundation/         # Chain 폴더
    │   ├── chain-prd.md                             # Chain PRD
    │   └── chain-basic-design.md                    # Chain 기본설계
    │
    ├── CHAIN-orchay-02-core-project-management/
    │   ├── chain-prd.md
    │   └── chain-basic-design.md
    │
    ├── CHAIN-orchay-03-llm-integration/
    │   ├── chain-prd.md
    │   └── chain-basic-design.md
    │
    └── CHAIN-orchay-04-deployment-cli/
        ├── chain-prd.md
        └── chain-basic-design.md
```

---

## Chain PRD 템플릿

```markdown
# Chain PRD: {Chain 이름}

## 문서 정보

| 항목 | 내용 |
|------|------|
| Chain ID | CHAIN-{epic-id}-{번호} |
| Chain 이름 | {이름} |
| 문서 버전 | 1.0 |
| 작성일 | {오늘 날짜} |
| 상태 | Draft |
| Chain 유형 | Feature |
| 예상 기간 | {1-3}개월 |
| 상위 EPIC | {EPIC 이름} |
| 원본 PRD | {EPIC PRD 파일 경로} |

---

## 1. Chain 개요

### 1.1 Chain 비전
**"{배포 가능한 기능 가치 설명}"**

{이 Chain이 달성하고자 하는 핵심 목표}

### 1.2 범위 (Scope)

**포함:**
- {기능 1}
- {기능 2}
- {기능 3}

**제외:**
- {명시적으로 제외되는 것들}

### 1.3 성공 지표
- ✅ {측정 가능한 성공 기준 1}
- ✅ {측정 가능한 성공 기준 2}
- ✅ {측정 가능한 성공 기준 3}

---

## 2. Module (기능) 목록

**⚠️ Module은 문서로만 정의하며, 별도 폴더나 module-prd.md는 생성하지 않습니다.**

이 Chain은 다음 Module들로 구성됩니다:

### MODULE-{chain-id}-01: {Module 이름} ({예상 기간: 1-4주})
**비전**: "{Module의 사용자 관점 가치}"

**기능**:
- {기능 1}
- {기능 2}
- {기능 3}

**인수 조건**:
- [ ] {검증 가능한 조건 1}
- [ ] {검증 가능한 조건 2}

**예상 Task 수**: {3-7개}

---

### MODULE-{chain-id}-02: {Module 이름} ({예상 기간})
...

---

## 3. 의존성

### 3.1 선행 Chains
- {필요한 선행 Chain 목록}

### 3.2 후행 Chains (이 Chain에 의존)
- {이 Chain에 의존하는 Chain 목록}

### 3.3 외부 의존성
- {라이브러리, 서비스, API 등}

---

## 4. 주요 화면/API 목록

### 4.1 화면 목록
| 화면 이름 | 경로 | 설명 | 관련 Module |
|----------|------|------|-------------|
| {화면명} | {URL} | {설명} | MODULE-{id} |

### 4.2 API 목록
| API | Method | 경로 | 설명 | 관련 Module |
|-----|--------|------|------|-------------|
| {API명} | GET/POST | {경로} | {설명} | MODULE-{id} |

---

## 5. 기술 스택

| 레이어 | 기술 | 비고 |
|--------|------|------|
| Frontend | {기술} | {설명} |
| Backend | {기술} | {설명} |
| Database | {기술} | {설명} |
| 기타 | {기술} | {설명} |

---

## 6. 마일스톤

| 마일스톤 | 목표일 | 산출물 |
|----------|--------|--------|
| M1: {이름} | Week {X} | {산출물} |
| M2: {이름} | Week {Y} | {산출물} |
| M3: {이름} | Week {Z} | {산출물} |

---

## 7. 참조 문서

- 원본 EPIC PRD: {파일 경로}
- 관련 Chain PRD: {파일 경로}

---

## 8. 변경 이력

| 버전 | 날짜 | 변경 내용 |
|------|------|-----------|
| 1.0 | {날짜} | 초안 작성 |
```

---

## Chain 기본설계 템플릿

```markdown
# Chain 기본설계: {Chain 이름}

## 문서 정보

| 항목 | 내용 |
|------|------|
| Chain ID | CHAIN-{epic-id}-{번호} |
| 관련 PRD | chain-prd.md |
| 문서 버전 | 1.0 |
| 작성일 | {오늘 날짜} |
| 상태 | Draft |

---

## 1. 아키텍처 개요

### 1.1 시스템 구조

```
[간단한 아키텍처 다이어그램]
```

### 1.2 주요 컴포넌트
- {컴포넌트 1}: {역할}
- {컴포넌트 2}: {역할}

---

## 2. 데이터 모델

### 2.1 Prisma Schema (주요 모델)

```prisma
model {ModelName} {
  // 주요 필드
}
```

### 2.2 관계도

```
[ERD 또는 관계 설명]
```

---

## 3. API 설계

### 3.1 REST API 엔드포인트

| Method | 경로 | 설명 | 요청 | 응답 |
|--------|------|------|------|------|
| GET | {경로} | {설명} | - | {응답 형식} |
| POST | {경로} | {설명} | {요청 형식} | {응답 형식} |

---

## 4. UI/UX 설계

### 4.1 화면 플로우

```
[화면 흐름도]
```

### 4.2 주요 화면 와이어프레임

```
[와이어프레임 또는 ASCII 아트]
```

---

## 5. 보안 및 성능

### 5.1 보안 고려사항
- {보안 요구사항 1}
- {보안 요구사항 2}

### 5.2 성능 목표
- {성능 목표 1}
- {성능 목표 2}

---

## 6. 변경 이력

| 버전 | 날짜 | 변경 내용 |
|------|------|-----------|
| 1.0 | {날짜} | 초안 작성 |
```

---

## 품질 기준

- ✅ **적정 규모**: 각 Chain이 1-3개월 단위
- ✅ **적정 개수**: EPIC당 3-7개 Chain
- ✅ **독립성**: 각 Chain이 독립적으로 배포 가능
- ✅ **완전성**: EPIC PRD의 모든 내용이 적절히 분배됨
- ✅ **일관성**: 모든 Chain이 동일한 템플릿 구조 사용
- ✅ **추적성**: EPIC PRD와의 연결 명확히 표시
- ✅ **명확한 의존성**: Chain 간 선후행 관계 명시

---

## 고급 옵션

사용자 요청 시 다음 옵션 지원:

1. **Chain 개수 제한**: `--max-chains N` (기본값: 7)
2. **최소 기간**: `--min-duration N` (기본값: 1개월)
3. **출력 디렉토리**: `--output-dir PATH` (기본값: EPIC 폴더)
4. **의존성 시각화**: `--visualize-deps` (Mermaid 다이어그램)

---

## 사용 워크플로우

```
1. 사용자: /split-chains
2. AI: EPIC PRD 파일 경로 요청
3. AI: EPIC PRD 분석 → 기능 영역 추출
4. AI: Chain 후보 생성 및 크기 검증
5. 사용자: Chain 구조 승인 (y/n)
6. AI: 3-7개 Chain 생성
7. AI: Module 구조 정의 (chain-prd.md 내부에만)
8. AI: Chain 폴더 및 chain-prd.md, chain-basic-design.md 생성
9. 완료!
```

---

## 📋 다음 단계

```
1. 각 Chain PRD 검토
2. 필요 시 Module 폴더 및 module-prd.md 별도 생성 (별도 명령어)
3. Chain 우선순위 결정
4. Chain 순차 구현
5. 일정 및 담당자 할당
```
