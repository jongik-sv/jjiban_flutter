# Chain을 Module로 분리하는 명령어

Chain PRD 문서를 분석하여 **Module 단위 (1-4주 User Story)**로 분리하고, Module 폴더 구조를 생성합니다.

## ⚠️ 중요 지침

**이 명령어는 Module 레벨 문서화 작업 전용입니다:**
- ✅ Chain PRD 분석 및 Module 분할
- ✅ Module PRD 문서 생성
- ✅ Module 기본설계 문서 생성
- ✅ Module 레벨 폴더 구조 생성
- ✅ 의존성 분석 및 매핑
- ❌ **Task 폴더/문서 생성 금지** - Module 레벨까지만
- ❌ **코드 작성 금지** - 구현은 별도 명령어 사용
- ❌ **코드 생성 금지** - 설계 문서만 작성

---

## 📊 Module 개념

### Module-Level 정의

**Module = User Story = 사용자 관점 기능 단위 (1-4주)**

| 레벨 | 크기 | 목적 | 예시 |
|------|------|------|------|
| **EPIC-Level** | 3-6개월 | 전략적 비즈니스 역량 | "orchay - AI-Assisted Kanban Tool" |
| **Chain-Level** | 1-3개월 | 실행 가능한 Feature | "Core Project Management System" |
| **Module-Level** | 1-4주 | User Story | "칸반 보드 UI" |
| **Task-Level** | 1-5일 | 구현 작업 | "드래그 앤 드롭 구현" |

### Module 크기 가이드라인

**적절한 Module 크기 (✅ 1-4주 규모)**:
```
✅ MODULE-01: Portal & Layout System (2주)
   ├── 전역 헤더 구현
   ├── 사이드바 네비게이션
   ├── 라우팅 시스템
   └── 반응형 레이아웃
→ 사용자 스토리: "사용자가 일관된 UI에서 앱을 탐색할 수 있다"

✅ MODULE-02: Design System & Component Library (3주)
   ├── 색상/타이포그래피 시스템
   ├── 공통 컴포넌트 20개+
   └── Storybook 문서화
→ 사용자 스토리: "개발자가 재사용 가능한 컴포넌트를 활용할 수 있다"
```

**너무 작은 경우 (❌ Task 수준)**:
```
❌ MODULE-01: 버튼 컴포넌트 (1-2일)
   └── 단일 컴포넌트
→ 문제: Module이 Task 수준으로 너무 작음

해결: "Design System & Component Library"로 통합
```

**너무 큰 경우 (❌ Chain 수준)**:
```
❌ MODULE-01: 전체 프로젝트 관리 시스템 (2개월)
→ 문제: Module이 Chain 수준으로 너무 큼

해결: "칸반 보드", "Gantt 차트", "Task 상세"로 분할
```

---

## 🎯 MECE 원칙 (Mutually Exclusive, Collectively Exhaustive)

### MECE 개념

**MECE는 효과적인 Module 분할을 위한 핵심 원칙입니다:**

- **Mutually Exclusive (상호 배타적)**: 각 Module이 **겹치지 않음**
- **Collectively Exhaustive (전체를 포괄)**: 모든 User Story가 **어떤 Module에든 포함됨**

```
❌ MECE 위반 (겹침 + 빠짐):
MODULE-01: Portal & 레이아웃 (헤더, 사이드바, 라우팅)
MODULE-02: 헤더 구현 (포함된 부분 반복)
MODULE-03: 라우팅 (포함된 부분 반복)
→ "헤더", "라우팅"이 MODULE-01, 02, 03에 겹침
→ "404 페이지" 누락

✅ MECE 준수 (겹치지 않음 + 빠지지 않음):
MODULE-01: Portal & 레이아웃 시스템 (헤더, 사이드바, 라우팅, 404)
MODULE-02: 디자인 시스템 & 컴포넌트 (색상, 타이포그래피, UI컴포넌트)
MODULE-03: 데이터베이스 스키마 (DB 설계, 마이그레이션, 시드)
MODULE-04: 사용자 인증 (로그인, JWT, 세션, 권한)
→ 각 Module이 명확하게 구분됨
→ Chain의 모든 기능이 포함됨
```

### Module 분할에서의 MECE 적용

#### 1. 상호 배타적 (Mutually Exclusive)

**각 Module은 명확하게 구분되어야 함:**

```markdown
**기능 영역별 경계 설정**:
- Portal 레이아웃 전체 → MODULE-01에만 포함
- 디자인 시스템 전체 → MODULE-02에만 포함
- 인증 기능 전체 → MODULE-04에만 포함

**기능 중복 예방**:
❌ "로그인 버튼" → MODULE-02(컴포넌트)와 MODULE-04(인증) 모두에 포함 (겹침)
✅ "로그인 버튼" → MODULE-02에서 컴포넌트로 정의, MODULE-04에서 로직 구현 (역할 구분)

**특정 기능이 여러 Module에 필요한 경우**:
→ 해당 기능을 설계 단계에서 먼저 구현하는 Module에 배치
→ 다른 Module에서는 해당 Module의 산출물을 재사용
```

#### 2. 전체를 포괄 (Collectively Exhaustive)

**Chain의 모든 사용자 스토리가 어떤 Module에든 포함:**

```markdown
**체크리스트: Chain PRD의 모든 섹션이 커버되었나?**

User Story 1: "사용자가 일관된 UI에서 앱을 탐색할 수 있다"
→ MODULE-01 (Portal & 레이아웃)에 포함

User Story 2: "개발자가 재사용 가능한 컴포넌트를 활용할 수 있다"
→ MODULE-02 (디자인 시스템)에 포함

User Story 3: "사용자가 안전하게 로그인할 수 있다"
→ MODULE-04 (인증)에 포함

...모든 User Story가 어떤 Module에든 할당됨
```

### MECE 검증 체크리스트

분할 완료 후 다음을 확인하세요:

```markdown
## 상호 배타적 검증

□ 각 Module의 사용자 스토리가 명확하게 정의되었는가?
□ 기능이 여러 Module에 중복되지 않는가?
□ Module 간의 경계가 명확한가?

**기능 중복 검사 (5분)**:
1. Chain PRD에서 각 기능 추출
2. 해당 기능이 포함된 Module 확인
3. 1개 Module에만 포함되었나? 확인

## 전체를 포괄 검증

□ Chain PRD의 모든 User Story가 어떤 Module에 할당되었는가?
□ Chain의 모든 기능 영역이 포함되었는가?
□ 빠진 기능이 없는가?

**누락 검사 (5분)**:
1. Chain PRD의 모든 기능 목록화
2. 각 기능이 어떤 Module에 포함되었는지 매핑
3. 미할당 기능이 있나? 확인

## 실제 예시

**❌ MECE 위반 사례**:
```
MODULE-01: Portal & 레이아웃
  - 전역 헤더
  - 사이드바
  - 라우팅

MODULE-02: 기본 컴포넌트
  - 버튼
  - Input
  - 헤더 (일부) ← 겹침!

MODULE-03: 인증
  - 로그인 페이지

누락: 404 페이지, 색상 시스템 없음
```

**✅ MECE 준수 사례**:
```
MODULE-01: Portal & 레이아웃 시스템 (2주)
  - 전역 헤더
  - 사이드바 네비게이션
  - 메인 레이아웃 템플릿
  - 라우팅 시스템
  - 404 페이지

MODULE-02: 디자인 시스템 & 컴포넌트 라이브러리 (3주)
  - 색상 팔레트
  - 타이포그래피
  - 공통 컴포넌트 (Button, Input, Modal 등)
  - 아이콘 시스템
  - Storybook 문서화

MODULE-03: 데이터베이스 스키마 & ORM (2주)
  - Prisma Schema 정의
  - 마이그레이션 설정
  - 기본 시드 데이터
  - 인덱스 설정

MODULE-04: 사용자 인증 & 권한 관리 (2주)
  - 로그인/로그아웃
  - JWT 토큰 관리
  - 세션 관리
  - RBAC 설정
```
```

---

## 사용자 스토리 기반 분할 원칙

### 1. 사용자 관점 그룹핑

**사용자 시나리오별로 그룹핑**

예시:
- **화면 영역**: 헤더 + 사이드바 + 레이아웃 → Module
- **기능 흐름**: 로그인 + 회원가입 + 프로필 → Module
- **데이터 도메인**: DB 스키마 + 마이그레이션 + 시드 → Module

### 2. 인수 조건 중심

**각 Module이 명확한 인수 조건(Acceptance Criteria)을 가짐**

```
✅ 인수 조건 예시:
- [ ] 모든 화면에서 일관된 헤더/사이드바 표시
- [ ] 반응형 디자인 (모바일, 태블릿, 데스크톱)
- [ ] 라우팅 전환 시 레이아웃 유지
```

### 3. 독립적 테스트 가능성

**각 Module이 독립적으로 테스트 가능**

### 4. Module 개수 제한

**⚠️ 중요: Chain당 3-10개 Module**
- 너무 많으면 → 관리 복잡
- 너무 적으면 → Module이 너무 거대

---

## 사전 요구사항

사용자에게 다음 정보를 요청하세요:
1. **Chain PRD 파일 경로** (예: `projects/orchay/CHAIN-orchay-01-platform-foundation/chain-prd.md`)
2. **Chain 폴더 경로** (예: `projects/orchay/CHAIN-orchay-01-platform-foundation/`)
3. **Module 분류 방식** (자동 추론 또는 수동 지정)

---

## 실행 단계

### 1단계: Chain PRD 분석

1. Chain PRD 파일 읽기
2. 문서 구조 파악 (섹션, 헤더 레벨)
3. **기존 Module 정의 추출**:
   - `### MODULE-{chain-id}-{nn}:` 형식 파싱
   - 비전, 기능, 인수 조건 추출
4. Module이 정의되어 있지 않으면 **자동 생성**

### 2단계: Module 추출 또는 생성

#### 2-1. 기존 Module 정의 파싱

Chain PRD에서 다음 형식의 Module 정의를 파싱:

```markdown
### MODULE-{chain-id}-{nn}: {Module 이름} ({예상 기간})
**비전**: "{Module의 사용자 관점 가치}"

**기능**:
- {기능 1}
- {기능 2}

**인수 조건**:
- [ ] {검증 가능한 조건 1}
- [ ] {검증 가능한 조건 2}

**예상 Task 수**: {3-7개}
```

#### 2-2. 자동 Module 생성 (정의가 없는 경우)

**기능 영역 키워드 매칭:**
- **UI/화면**: "화면", "UI", "페이지", "컴포넌트", "레이아웃"
- **인증**: "로그인", "인증", "Auth", "JWT", "사용자"
- **데이터**: "데이터베이스", "DB", "스키마", "Prisma", "모델"
- **API**: "API", "엔드포인트", "REST", "서비스"
- **보안**: "보안", "Security", "CORS", "Helmet"
- **설정**: "설정", "Config", "환경", "로깅"

#### 2-3. Module 크기 검증

각 Module 후보를 다음 기준으로 검증:

**✅ 적절한 Module 기준:**
- 예상 기간: 1-4주
- 포함 Task 수: 3-7개 (각 1-5일)
- 사용자 스토리: 명확한 사용자 가치 제공
- 독립적 테스트: 단독으로 테스트 가능

**❌ Task로 강등 기준:**
- 예상 기간: 1-3일 (너무 작음)
- 단일 기능/컴포넌트
- 다른 Module 없이는 테스트 불가

---

## Module 네이밍 규칙

### Module ID 형식
- **ID 형식**: `MODULE-{chain-id}-{01-99}`
- **폴더명**: `MODULE-{chain-id}-{number}-{kebab-case-name}`
- **예시**:
  - `MODULE-orchay-01-01-portal-layout-system`
  - `MODULE-orchay-01-02-design-system-components`
  - `MODULE-orchay-01-03-database-schema-orm`

---

## 폴더 구조

**⚠️ 이 명령어는 Module 레벨까지만 생성합니다. Task는 module-prd.md에 정의만 하고 폴더는 생성하지 않습니다.**

```
projects/
└── {epic-name}/                                         # EPIC 폴더
    ├── {epic-name}-prd.md                               # EPIC PRD
    │
    └── CHAIN-{epic-id}-{nn}-{chain-name}/               # Chain 폴더
        ├── chain-prd.md                                 # Chain PRD
        ├── chain-basic-design.md                        # Chain 기본설계
        │
        ├── MODULE-{chain-id}-01-{module-name}/          # Module 폴더
        │   ├── module-prd.md                            # Module PRD
        │   └── module-basic-design.md                   # Module 기본설계
        │
        ├── MODULE-{chain-id}-02-{module-name}/
        │   ├── module-prd.md
        │   └── module-basic-design.md
        │
        └── MODULE-{chain-id}-03-{module-name}/
            ├── module-prd.md
            └── module-basic-design.md
```

---

## Module PRD 템플릿

```markdown
# Module PRD: {Module 이름}

## 문서 정보

| 항목 | 내용 |
|------|------|
| Module ID | MODULE-{chain-id}-{번호} |
| Module 이름 | {이름} |
| 문서 버전 | 1.0 |
| 작성일 | {오늘 날짜} |
| 상태 | Draft |
| Module 유형 | User Story |
| 예상 기간 | {1-4}주 |
| 상위 Chain | {Chain 이름} |
| 원본 Chain PRD | {Chain PRD 파일 경로} |

---

## 1. Module 개요

### 1.1 User Story
**"As a {사용자 역할}, I want {기능/행동} so that {달성하려는 가치}"**

{사용자 스토리 상세 설명}

### 1.2 범위 (Scope)

**포함:**
- {기능 1}
- {기능 2}
- {기능 3}

**제외:**
- {명시적으로 제외되는 것들}

### 1.3 인수 조건 (Acceptance Criteria)
- [ ] {검증 가능한 조건 1}
- [ ] {검증 가능한 조건 2}
- [ ] {검증 가능한 조건 3}

---

## 2. Task 목록

**⚠️ Task는 문서로만 정의하며, 별도 폴더나 task-prd.md는 생성하지 않습니다.**

이 Module은 다음 Task들로 구성됩니다:

### TASK-{module-id}-01: {Task 이름} ({예상 기간: 1-5일})
**설명**: "{Task 상세 설명}"

**작업 내용**:
- {작업 1}
- {작업 2}

**완료 조건**:
- [ ] {완료 조건 1}
- [ ] {완료 조건 2}

---

### TASK-{module-id}-02: {Task 이름} ({예상 기간})
...

---

## 3. 의존성

### 3.1 선행 Modules
- {필요한 선행 Module 목록}

### 3.2 후행 Modules (이 Module에 의존)
- {이 Module에 의존하는 Module 목록}

### 3.3 외부 의존성
- {라이브러리, 서비스, API 등}

---

## 4. 주요 화면/API 목록

### 4.1 화면 목록
| 화면 이름 | 경로 | 설명 | 관련 Task |
|----------|------|------|-----------|
| {화면명} | {URL} | {설명} | TASK-{id} |

### 4.2 API 목록
| API | Method | 경로 | 설명 | 관련 Task |
|-----|--------|------|------|-----------|
| {API명} | GET/POST | {경로} | {설명} | TASK-{id} |

---

## 5. 기술 스택

| 레이어 | 기술 | 비고 |
|--------|------|------|
| Frontend | {기술} | {설명} |
| Backend | {기술} | {설명} |
| Database | {기술} | {설명} |
| 기타 | {기술} | {설명} |

---

## 6. 참조 문서

- 상위 Chain PRD: {파일 경로}
- Chain 기본설계: {파일 경로}
- 관련 Module PRD: {파일 경로}

---

## 7. 변경 이력

| 버전 | 날짜 | 변경 내용 |
|------|------|-----------|
| 1.0 | {날짜} | 초안 작성 |
```

---

## Module 기본설계 템플릿

```markdown
# Module 기본설계: {Module 이름}

## 문서 정보

| 항목 | 내용 |
|------|------|
| Module ID | MODULE-{chain-id}-{번호} |
| 관련 PRD | module-prd.md |
| 문서 버전 | 1.0 |
| 작성일 | {오늘 날짜} |
| 상태 | Draft |

---

## 1. 아키텍처 개요

### 1.1 컴포넌트 구조

```
[컴포넌트 다이어그램 또는 구조 설명]
```

### 1.2 주요 컴포넌트
- {컴포넌트 1}: {역할}
- {컴포넌트 2}: {역할}

---

## 2. 데이터 모델

### 2.1 관련 Prisma Models

```prisma
model {ModelName} {
  // 주요 필드
}
```

### 2.2 데이터 흐름

```
[데이터 흐름 다이어그램]
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

### 4.1 화면 구조

```
[와이어프레임 또는 ASCII 아트]
```

### 4.2 사용자 흐름

```
[사용자 흐름도]
```

---

## 5. 구현 가이드

### 5.1 파일 구조

```
src/
├── components/
│   └── {module-name}/
│       ├── index.ts
│       └── ...
├── pages/
│   └── ...
└── services/
    └── ...
```

### 5.2 주요 구현 포인트
- {구현 포인트 1}
- {구현 포인트 2}

---

## 6. 테스트 전략

### 6.1 단위 테스트
- {테스트 범위}

### 6.2 통합 테스트
- {테스트 시나리오}

### 6.3 E2E 테스트
- {테스트 케이스}

---

## 7. 변경 이력

| 버전 | 날짜 | 변경 내용 |
|------|------|-----------|
| 1.0 | {날짜} | 초안 작성 |
```

---

## 품질 기준

- ✅ **적정 규모**: 각 Module이 1-4주 단위
- ✅ **적정 개수**: Chain당 3-10개 Module
- ✅ **사용자 스토리**: 각 Module이 명확한 사용자 가치 제공
- ✅ **인수 조건**: 검증 가능한 완료 기준
- ✅ **완전성**: Chain PRD의 모든 내용이 적절히 분배됨
- ✅ **일관성**: 모든 Module이 동일한 템플릿 구조 사용
- ✅ **추적성**: Chain PRD와의 연결 명확히 표시
- ✅ **명확한 의존성**: Module 간 선후행 관계 명시

---

## 고급 옵션

사용자 요청 시 다음 옵션 지원:

1. **Module 개수 제한**: `--max-modules N` (기본값: 10)
2. **최소 기간**: `--min-duration N` (기본값: 1주)
3. **출력 디렉토리**: `--output-dir PATH` (기본값: Chain 폴더)
4. **의존성 시각화**: `--visualize-deps` (Mermaid 다이어그램)
5. **기존 정의 사용**: `--use-existing` (Chain PRD의 Module 정의 활용)

---

## 사용 워크플로우

```
1. 사용자: /split-modules
2. AI: Chain PRD 파일 경로 요청
3. AI: Chain PRD 분석 → Module 정의 추출/생성
4. AI: Module 후보 생성 및 크기 검증
5. 사용자: Module 구조 승인 (y/n)
6. AI: 3-10개 Module 폴더 생성
7. AI: Task 구조 정의 (module-prd.md 내부에만)
8. AI: module-prd.md, module-basic-design.md 생성
9. 완료!
```

---

## 📋 다음 단계

```
1. 각 Module PRD 검토
2. 필요 시 Task 폴더 및 task-prd.md 별도 생성 (별도 명령어)
3. Module 우선순위 결정
4. Module 순차 구현
5. 일정 및 담당자 할당
```

---

## 사용 예시

### 단일 Chain 처리

```bash
/split-modules projects/orchay/CHAIN-orchay-01-platform-foundation/chain-prd.md
```

### 전체 EPIC의 모든 Chain 처리

```bash
/split-modules --all projects/orchay/
```

### 기존 Module 정의 활용

```bash
/split-modules --use-existing projects/orchay/CHAIN-orchay-01-platform-foundation/chain-prd.md
```

---

## 주의사항

1. **Chain PRD에 Module 정의가 있는지 먼저 확인**
   - 있으면 기존 정의 활용
   - 없으면 자동 생성

2. **Module ID는 Chain ID 기반으로 생성**
   - Chain: `CHAIN-orchay-01` → Module: `MODULE-orchay-01-01`

3. **폴더명은 kebab-case 사용**
   - `MODULE-orchay-01-01-portal-layout-system`

4. **Task는 문서에만 정의**
   - Task 폴더와 task-prd.md는 별도 명령어로 생성
