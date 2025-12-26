---
name: plan:wbs
description: "PRD를 이슈 계층 구조로 분할하여 WBS를 생성합니다. 프로젝트 규모에 따라 4단계/3단계 구조 선택."
category: planning
complexity: complex
wave-enabled: true
performance-profile: complex
auto-flags:
  - --seq
  - --token-efficient
mcp-servers: [sequential]
personas: [architect, analyzer, scribe]
---

# /plan:wbs - PRD 기반 WBS 생성

> **PRD → WBS 자동 변환**: PRD 문서를 분석하여 계층적 WBS를 `wbs.md` 파일로 생성합니다.

## 트리거
- PRD 문서를 이슈 계층 구조로 분할이 필요한 경우
- 체계적인 WBS(Work Breakdown Structure) 생성이 필요한 경우
- Task category별 워크플로우 적용이 필요한 경우

## 사용법
```bash
/plan:wbs [PRD 파일 경로]
/plan:wbs [PRD 파일 경로] --scale [large|medium|small]

# 예시
/plan:wbs .jjiban/projects/jjiban/prd.md
/plan:wbs .jjiban/projects/jjiban/prd.md --scale large
```

## 핵심 특징
- **프로젝트 초기화 자동 감지**: 프로젝트 미존재 시 WP-00 자동 추가
- **프로젝트 규모 자동 산정**: 대규모/중간규모 자동 판별
- **규모별 계층 구조**: 4단계(대규모) / 3단계(중간/소규모)
- **Task category별 워크플로우**: development, defect, infrastructure 구분
- **워크플로우 상태 표시**: `[ ]`, `[dd]`, `[ap]`, `[im]`, `[xx]`
- **MECE 원칙**: 상호 배타적 + 전체 포괄 분할
- **일정 자동 계산**: category별 기간 추정 + 의존성 기반 일정 산출

---

## 계층 구조

```
Project (프로젝트) - 6~24개월
├── Work Package #1 (주요 기능 묶음) - 1~3개월
│   ├── Activity #1.1 (세부 활동) - 1~4주          ← 4단계만
│   │   ├── Task #1.1.1 (실제 작업) - 1일~1주
│   │   └── Task #1.1.2
│   └── Activity #1.2
│       └── Task #1.2.1
├── Work Package #2
│   └── Task #2.1 (Activity 생략 가능)             ← 3단계
└── Work Package #3
    └── Task #3.1
```

### 계층 타입

| 레벨 | 명칭 | 설명 | 기간 |
|------|------|------|------|
| Level 1 | **Project** | 전체 프로젝트 | 6~24개월 |
| Level 2 | **Work Package** | 주요 기능 단위의 작업 묶음 | 1~3개월 |
| Level 3 | **Activity** | 세부 활동 단위 (4단계에서만 사용) | 1~4주 |
| Level 4 | **Task** | 실제 수행 작업 단위 | 1일~1주 |

### Task category

| category | 설명 | 워크플로우 |
|----------|------|------------|
| `development` | 신규 기능 개발 | `[ ]` → `[dd]` → `[ap]` → `[im]` → `[xx]` |
| `defect` | 결함 수정 | `[ ]` → `[an]` → `[fx]` → `[vf]` → `[xx]` |
| `infrastructure` | 인프라/기술 작업 | `[ ]` → `[dd]?` → `[im]` → `[xx]` |

### Task domain (기술 영역)

| domain | 설명 | 대표 작업 |
|--------|------|----------|
| `frontend` | 클라이언트 UI/UX | Vue 컴포넌트, 페이지, 스타일링, 상태관리 |
| `backend` | 서버 비즈니스 로직 | API 엔드포인트, 서비스, 미들웨어 |
| `database` | 데이터 계층 | 스키마, 마이그레이션, 쿼리 최적화 |
| `infra` | 인프라/DevOps | 배포, CI/CD, 모니터링, 환경설정 |
| `fullstack` | 전체 스택 | E2E 기능, 통합 작업 |
| `docs` | 문서화 | API 문서, 사용자 가이드, README |
| `test` | 테스트 전용 | 단위/통합/E2E 테스트 작성 |

---

## 프로젝트 규모 산정

### 규모 판별 기준

| 기준 | 대규모 (4단계) | 중간/소규모 (3단계) |
|------|---------------|-------------------|
| **예상 기간** | 12개월+ | 12개월 미만 |
| **팀 규모** | 10명+ | 10명 미만 |
| **기능 영역 수** | 5개+ | 5개 미만 |
| **예상 Task 수** | 50개+ | 50개 미만 |

### 규모별 구조

**4단계 (대규모)**: `Project → WP → ACT → TSK`
```
## WP-01: Work Package Name
### ACT-01-01: Activity Name
#### TSK-01-01-01: Task Name
```

**3단계 (중간/소규모)**: `Project → WP → TSK`
```
## WP-01: Work Package Name
### TSK-01-01: Task Name
```

---

## 워크플로우 상태 기호

### 칸반 컬럼 매핑

| 칸반 컬럼 | 통합 상태 | 의미 |
|-----------|-----------|------|
| Todo | `[ ]` | 대기 |
| Design | `[dd]`, `[an]` | 설계/분석 |
| Approve | `[ap]` | 승인 |
| Implement | `[im]`, `[fx]` | 구현/수정 |
| Verify | `[vf]` | 검증 |
| Done | `[xx]` | 완료 |

### 카테고리별 세부 상태

| 기호 | 의미 | 사용 카테고리 |
|------|------|--------------|
| `[ ]` | Todo (대기) | 공통 |
| `[dd]` | 설계 | development, infrastructure |
| `[an]` | 분석 | defect |
| `[ap]` | 승인 | development |
| `[im]` | 구현 | development, infrastructure |
| `[fx]` | 수정 | defect |
| `[vf]` | 검증/테스트 | defect |
| `[xx]` | 완료 | 공통 |

---

## 자동 실행 플로우

### 0단계: 프로젝트 존재 확인 및 초기화

1. `.jjiban/projects/{project}/` 폴더 존재 확인
2. **존재하지 않으면**:
   - WBS에 `WP-00: 프로젝트 초기화` Work Package 자동 추가
   - jjiban-init 스킬 실행하여 프로젝트 구조 생성
3. **존재하면**: 기존 프로젝트 메타데이터 로드

### 1단계: PRD 분석 및 프로젝트 규모 산정

1. PRD 파일 읽기 및 구조 분석
2. 프로젝트 규모 산정 (기능 영역 수, 예상 복잡도)
3. 규모 결정: 4단계 / 3단계
4. 사용자에게 규모 확인 (옵션)

### 2단계: PRD 섹션 → Work Package 매핑

| PRD 섹션 | Work Package 매핑 |
|----------|------------------|
| 핵심 기능 (Core Features) | WP-01 ~ WP-0N |
| 플랫폼 기능 (Platform Features) | WP-0N+1 ~ WP-0M |
| 지원 기능 (Support Features) | WP-0M+1 ~ WP-0K |

### 3단계: Work Package → Activity 분해 (4단계만)

- 사용자 관점 기능 단위
- 1~4주 규모 검증
- 독립적 테스트 가능 여부
- MECE 원칙 적용

### 4단계: Activity → Task 분해 및 category 분류

| category | 식별 기준 |
|----------|----------|
| **development** | 신규 기능 구현, 설계 필요 |
| **defect** | 결함 수정, 기존 코드 패치 |
| **infrastructure** | 리팩토링, 인프라, 성능개선 |

**Task 크기 검증**:
- 최소: 4시간
- 권장: 1~3일
- 최대: 1주 (초과 시 분할)

### 5단계: 일정 계산

**Task 기간 추정 (category별 기본값)**:

| category | 기본 기간 | 범위 |
|----------|----------|------|
| development | 10일 | 5~15일 |
| defect | 3일 | 2~5일 |
| infrastructure | 5일 | 2~10일 |

### 6단계: WBS 문서 생성

**생성 파일**: `.jjiban/projects/{project}/wbs.md`

---

## 출력 형식

### wbs.md 파일 형식

```markdown
# WBS - {프로젝트명}

> version: 1.0
> depth: 4
> updated: {날짜}

---

## WP-00: 프로젝트 초기화 (자동 생성 - 프로젝트 미존재 시)
- status: planned
- priority: critical
- schedule: {시작일} ~ {시작일}
- progress: 0%
- note: 프로젝트 폴더가 존재하지 않아 자동 추가됨

### TSK-00-01: jjiban 프로젝트 구조 초기화
- category: infrastructure
- domain: infra
- status: [ ]
- priority: critical
- assignee: -
- schedule: {시작일} ~ {시작일}
- tags: setup, init
- depends: -
- note: jjiban-init 스킬 실행 필요

---

## WP-01: {Work Package명}
- status: planned
- priority: high
- schedule: {시작일} ~ {종료일}
- progress: 0%

### ACT-01-01: {Activity명}
- status: todo
- schedule: {시작일} ~ {종료일}

#### TSK-01-01-01: {Task명}
- category: development
- domain: backend
- status: [ ]
- priority: high
- assignee: -
- schedule: {시작일} ~ {종료일}
- tags: api, crud
- depends: -

#### TSK-01-01-02: {Task명}
- category: development
- domain: frontend
- status: [ ]
- priority: medium
- assignee: -
- schedule: {시작일} ~ {종료일}
- tags: form, validation
- depends: TSK-01-01-01

---

## WP-02: {Work Package명}
- status: planned
- priority: medium
- schedule: {시작일} ~ {종료일}
- progress: 0%

### TSK-02-01: {Task명} (3단계 예시 - ACT 생략)
- category: development
- domain: fullstack
- status: [ ]
- priority: high
- assignee: -
- note: 3단계 구조 예시
```

### ID 패턴

| 레벨 | 마크다운 | ID 패턴 | 예시 |
|------|----------|---------|------|
| WP (초기화) | `## WP-00:` | `WP-00` (예약) | `## WP-00: 프로젝트 초기화` |
| WP | `## WP-XX:` | `WP-{2자리}` | `## WP-01: 플랫폼 기반` |
| ACT (4단계) | `### ACT-XX-XX:` | `ACT-{WP}-{순번}` | `### ACT-01-01: 프로젝트 관리` |
| TSK (4단계) | `#### TSK-XX-XX-XX:` | `TSK-{WP}-{ACT}-{순번}` | `#### TSK-01-01-01: API 구현` |
| TSK (3단계) | `### TSK-XX-XX:` | `TSK-{WP}-{순번}` | `### TSK-02-01: 칸반 구현` |

### Task 속성

| 속성 | 필수 | 설명 | 예시 |
|------|------|------|------|
| category | O | 작업 유형 | `development`, `defect`, `infrastructure` |
| domain | O | 기술 영역 | `frontend`, `backend`, `database`, `infra`, `fullstack`, `docs`, `test` |
| status | O | 상태 + 기호 | `todo [ ]`, `implement [im]`, `done [xx]` |
| priority | O | 우선순위 | `critical`, `high`, `medium`, `low` |
| assignee | - | 담당자 ID | `hong`, `-` (미지정) |
| schedule | - | 일정 | `2026-01-15 ~ 2026-01-21` |
| tags | - | 태그 목록 | `auth, crud, validation` |
| depends | - | 선행 Task | `TSK-01-01-01` |
| blocked-by | - | 차단 Task | `TSK-01-01-01` |
| note | - | 비고 | 자유 텍스트 |

---

## 고급 옵션

```bash
# 규모 강제 지정
/plan:wbs --scale large .jjiban/projects/jjiban/prd.md
/plan:wbs --scale medium .jjiban/projects/myapp/prd.md

# 시작일 지정
/plan:wbs --start-date 2026-01-15 .jjiban/projects/jjiban/prd.md

# 규모 산정만 실행 (WBS 생성 없이)
/plan:wbs --estimate-only .jjiban/projects/jjiban/prd.md
```

| 옵션 | 설명 | 기본값 |
|------|------|--------|
| `--scale [large\|medium]` | 프로젝트 규모 강제 지정 | 자동 산정 |
| `--start-date [YYYY-MM-DD]` | 프로젝트 시작일 지정 | 오늘 날짜 |
| `--estimate-only` | 규모 산정만 실행 | - |

---

## 산출물 위치

| 산출물 | 경로 |
|--------|------|
| WBS 문서 | `.jjiban/projects/{project}/wbs.md` |

---

## 다음 단계

1. WBS 검토 및 수정
2. Task 우선순위 결정
3. `/wf:start` → 설계 시작
4. `/wf:approve` → 설계 승인
5. `/wf:build` → TDD 기반 구현
6. `/wf:done` → 작업 완료

---

## 성공 기준

- **요구사항 커버리지**: PRD 모든 기능이 Task로 분해됨
- **적정 규모**: 모든 Task가 1일~1주 범위 내
- **추적성**: 각 Task에 PRD 요구사항 연결
- **워크플로우 준비**: 모든 Task에 상태 기호 및 category 표시

---

## 참조 문서

- `jjiban-prd.md`: 프로젝트 요구사항 문서
- `/wf:start`: 설계 시작 (Todo → Design)
- `/wf:approve`: 설계 승인 (Design → Approve)
- `/wf:build`: TDD 기반 구현 (Approve → Implement)
- `/wf:done`: 작업 완료 (Implement → Done)

<!--
jjiban 프로젝트 - Command Documentation
Command: plan:wbs
Category: planning
Version: 2.0
-->
