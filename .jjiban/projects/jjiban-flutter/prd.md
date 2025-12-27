# PRD: jjiban - AI 기반 프로젝트 관리 도구

## 문서 정보

| 항목 | 내용 |
|------|------|
| 문서 버전 | 1.0 |
| 작성일 | 2025-12-26 |
| 플랫폼 | Flutter (Web → Desktop) |
| 상태 | Draft |

---

## 1. 제품 개요

### 1.1 제품 비전

**"jjiban - LLM과 함께 개발하는 차세대 프로젝트 관리 도구"**

개발자의 로컬 환경에서 실행되는 경량 프로젝트 관리 도구입니다. 파일 기반 데이터 저장으로 Git 친화적이며, LLM CLI가 직접 마크다운/JSON 파일을 수정할 수 있어 AI와의 협업이 자연스럽습니다.

### 1.2 핵심 특징

| 특징 | 설명 |
|------|------|
| 로컬 실행 | 설치 후 바로 실행 가능한 데스크톱 앱 |
| 파일 기반 데이터 | wbs.md + JSON으로 Git 친화적 |
| Git 동기화 | Git push/pull이 곧 백업/동기화 |
| LLM CLI 통합 | Claude Code 등이 직접 마크다운 수정 가능 |
| 크로스 플랫폼 | Windows, macOS, Linux 지원 |

### 1.3 타겟 사용자

- **주 사용자**: 소규모 개발팀 (1-10명)
- **환경**: 로컬 개발 환경
- **사용 시나리오**:
  - Git 기반 워크플로우 선호
  - AI 기반 코드 작성 및 리뷰
  - 자동화된 설계 문서 생성
  - LLM을 활용한 테스트 코드 작성

### 1.4 운영 모델

```
GitHub (원격 저장소)
        │
   git clone (각자)
        │
┌───────┼───────┬───────────────┐
│       │       │               │
▼       ▼       ▼               ▼
홍길동   홍길동   김철수          박영희
PC-1    PC-2    노트북          회사PC
(집)    (회사)
```

- **중앙 서버 없음**: 각자 로컬에서 실행
- **동기화**: Git push/pull로 수동 동기화
- **한 사람 여러 PC 가능**: clone만 하면 됨

---

## 2. 작업 분류 체계 (WBS)

### 2.1 계층 구조

| 레벨 | 명칭 | 설명 | 기간 |
|------|------|------|------|
| Level 1 | Project | 전체 프로젝트 | 6~24개월 |
| Level 2 | Work Package | 주요 기능 단위의 작업 묶음 | 1~3개월 |
| Level 3 | Activity | 세부 활동 단위 (선택) | 1~4주 |
| Level 4 | Task | 실제 수행 작업 단위 | 1일~1주 |

### 2.2 계층 다이어그램

**4단계 구조 (대규모)**
```
Project
├── Work Package #1
│   ├── Activity #1.1
│   │   ├── Task #1.1.1
│   │   │   ├── Task #1.1.1-1 (Sub-Task)
│   │   │   └── Task #1.1.1-2 (Sub-Task)
│   │   └── Task #1.1.2
│   └── Activity #1.2
│       └── Task #1.2.1
└── Work Package #2
    └── Activity #2.1
```

**3단계 구조 (소규모)**
```
Project
├── Work Package #1
│   ├── Task #1.1
│   └── Task #1.2
└── Work Package #2
    └── Task #2.1
```

> **Sub-Task**: 프로젝트 진행 중 Task 세분화가 필요할 때 하위 Task로 추가

### 2.3 Task 카테고리

| 카테고리 | 설명 | 아이콘 |
|---------|------|--------|
| development | 신규 기능 개발 작업 | 🚀 |
| defect | 결함 수정 작업 | 🐛 |
| infrastructure | 인프라, 리팩토링 등 기술 작업 | ⚙️ |

### 2.4 작업 관리 기능

**Project 관리**
- Project 생성, 수정, 삭제, 아카이브
- 목표 일정 설정 (시작일, 목표일)
- 진행률 자동 계산 (하위 항목 기반)

**Work Package 관리**
- 상위 Project 연결
- 일정 관리 및 진행률 추적

**Activity 관리**
- 상위 Work Package 연결
- 담당자 지정
- 산출물 정의

**Task 관리**
- 상위 Activity 또는 Work Package 연결
- 담당자 지정
- 우선순위 설정 (critical, high, medium, low)
- 예상 시간 및 실제 시간 기록
- 라벨/태그 관리

### 2.5 계층별 허용 관계

| 상위 계층 | 허용되는 하위 계층 |
|----------|-------------------|
| Project | Work Package |
| Work Package | Activity, Task |
| Activity | Task |
| Task | Task (Sub-Task) |

---

## 3. 워크플로우 관리

### 3.1 워크플로우 설계 원칙

**4단계 + 승인 워크플로우 (Option A)**

기본설계와 상세설계를 통합하고, 설계 승인 단계를 명시적으로 분리한 단순화된 워크플로우입니다.

```
┌────────┬──────────┬──────────┬────────────┬────────┐
│  Todo  │  Design  │ Approve  │ Implement  │  Done  │
│  [ ]   │   [dd]   │   [ap]   │    [im]    │  [xx]  │
├────────┼──────────┼──────────┼────────────┼────────┤
│  대기   │   설계    │   승인    │    구현     │  완료   │
└────────┴──────────┴──────────┴────────────┴────────┘
```

### 3.2 카테고리별 워크플로우

**development (개발)**
```
[ ] → [dd] → [ap] → [im] → [xx]
Todo   설계   승인   구현   완료
```

| 명령어 | 현재 상태 | 다음 상태 | 설명 | 생성 문서 |
|--------|----------|----------|------|----------|
| design | `[ ]` | `[dd]` | 설계 시작 | 010-design.md |
| approve | `[dd]` | `[ap]` | 설계 승인 | - |
| build | `[ap]` | `[im]` | 구현 시작 | 030-implementation.md |
| done | `[im]` | `[xx]` | 작업 완료 | 080-manual.md |

**defect (결함)**
```
[ ] → [an] → [fx] → [vf] → [xx]
Todo  분석   수정   검증   완료
```

| 명령어 | 현재 상태 | 다음 상태 | 설명 | 생성 문서 |
|--------|----------|----------|------|----------|
| start | `[ ]` | `[an]` | 결함 분석 시작 | 010-defect-analysis.md |
| fix | `[an]` | `[fx]` | 수정 시작 | 030-implementation.md |
| verify | `[fx]` | `[vf]` | 회귀 테스트 시작 | 070-test-results.md |
| done | `[vf]` | `[xx]` | 수정 완료 | - |

**infrastructure (인프라)**
```
[ ] → [dd]? → [im] → [xx]
Todo  설계?   구현   완료
```

| 명령어 | 현재 상태 | 다음 상태 | 설명 | 생성 문서 |
|--------|----------|----------|------|----------|
| start | `[ ]` | `[dd]` | 기술 설계 시작 | 010-tech-design.md |
| skip | `[ ]` | `[im]` | 설계 생략, 바로 구현 | - |
| build | `[dd]` | `[im]` | 구현 시작 | 030-implementation.md |
| done | `[im]` | `[xx]` | 작업 완료 | - |

### 3.3 상태 내 액션

상태 변경 없이 반복 가능한 액션입니다.

| 명령어 | 사용 가능 상태 | 적용 카테고리 | 설명 | 생성/수정 문서 |
|--------|---------------|--------------|------|----------------|
| ui | `[dd]` | development | 화면설계 작성 | 011-ui-design.md |
| review | `[dd]` | development | LLM 설계 리뷰 | 021-design-review-{llm}-{n}.md |
| apply | `[dd]` | development | 리뷰 내용 반영 | 010-design.md |
| test | `[im]` | development | TDD/E2E 테스트 실행 | 070-test-results.md |
| audit | `[im]`, `[fx]` | 전체 | LLM 코드 리뷰 | 031-code-review-{llm}-{n}.md |
| patch | `[im]`, `[fx]` | 전체 | 리뷰 내용 반영 | 030-implementation.md |

### 3.4 카테고리별 흐름도

```
development:     [ ] → [dd] → [ap] → [im] → [xx]
                  │     │      │      │      │
칸반 컬럼:       Todo Design Approve Impl  Done
                  │     ╳      ╳      │      │
defect:          [ ] ──────→ [an] → [fx] → [vf] → [xx]
                  │     ╳      │      ╳      ╳      │
infrastructure:  [ ] ──────→ [dd]? ─────→ [im] ──→ [xx]
```

### 3.5 테스트 결과 관리

완료(`[xx]`)로 전환하기 위한 조건:

| 카테고리 | 조건 |
|----------|------|
| development | test-result: pass 필요 |
| defect | 회귀 테스트 통과 필요 |
| infrastructure | 조건 없음 |

**test-result 필드:**
- `none`: 테스트 미실행
- `pass`: 테스트 통과
- `fail`: 테스트 실패

---

## 4. 문서 관리

### 4.1 문서 저장 구조

```
.jjiban/
├── settings/              # 전역 설정
├── templates/             # 문서 템플릿
└── projects/              # 프로젝트 폴더
    └── [project-id]/
        ├── project.json   # 프로젝트 메타데이터
        ├── team.json      # 팀원 목록
        ├── wbs.md         # WBS 통합 파일
        └── tasks/         # Task 문서 폴더
            └── {TSK-ID}/
                ├── 010-design.md
                ├── 011-ui-design.md
                ├── 030-implementation.md
                └── ...
```

### 4.2 통합 설계 문서 구성

기존 기본설계 + 상세설계를 통합한 단일 설계 문서입니다.

```
010-design.md
├── 섹션 1: 목적 및 범위
├── 섹션 2: 요구사항 분석 (FR/NFR)
├── 섹션 3: 아키텍처 개요 (컴포넌트 구조)
├── 섹션 4: 데이터 모델 (ERD, 스키마)
├── 섹션 5: 인터페이스 계약 (API 명세)
├── 섹션 6: UI 설계 (화면 레이아웃, 상태)
├── 섹션 7: 프로세스 흐름 (시퀀스 다이어그램)
├── 섹션 8: 에러 처리 전략
├── 섹션 9: 테스트 시나리오
└── 섹션 10: 체크리스트
```

**코드 금지 원칙:**
- ❌ TypeScript/JavaScript 구현 코드
- ❌ Dart/Flutter 구현 코드
- ✅ 인터페이스 시그니처 (타입만)
- ✅ 표, 다이어그램, 유즈케이스

### 4.3 문서 번호 체계

| 카테고리 | 단계 | 파일명 |
|---------|------|--------|
| **development** | | |
| | 설계 | `010-design.md` |
| | 설계 리뷰 | `021-design-review-{llm}-{n}.md` |
| | 추적성 매트릭스 | `025-traceability-matrix.md` |
| | 테스트 명세 | `026-test-specification.md` |
| | 구현 | `030-implementation.md` |
| | 코드 리뷰 | `031-code-review-{llm}-{n}.md` |
| | 테스트 결과 | `070-test-results.md` |
| | 매뉴얼 | `080-manual.md` |
| **defect** | | |
| | 분석 | `010-defect-analysis.md` |
| | 구현 | `030-implementation.md` |
| | 코드 리뷰 | `031-code-review-{llm}-{n}.md` |
| | 테스트 | `070-test-results.md` |
| **infrastructure** | | |
| | 설계 | `010-tech-design.md` |
| | 구현 | `030-implementation.md` |
| | 코드 리뷰 | `031-code-review-{llm}-{n}.md` |

### 4.4 문서 뷰어 요구사항

**Markdown 렌더링**
- GitHub Flavored Markdown 지원
- 체크리스트 인터랙티브 지원

**코드 하이라이팅**
- 다중 언어 지원
- 라인 번호 표시
- 복사 버튼

**다이어그램 렌더링**
- Mermaid 다이어그램 지원
- 실시간 미리보기

---

## 6. 화면 기능

### 6.1 메인 화면

| 화면 | 설명 | 주요 기능 |
|------|------|-----------|
| 대시보드 | 전체 현황 | 프로젝트 요약, 내 할 일, 최근 활동 |

### 6.2 작업 관리 화면

| 화면 | 설명 | 주요 기능 |
|------|------|-----------|
| 칸반 보드 | 메인 작업 화면 | 칸반, 필터, 검색, 드래그 앤 드롭 |
| WBS 트리 | 계층 구조 | 트리 뷰, 펼침/접힘 |
| Gantt 차트 | 일정 시각화 | 타임라인, 드래그 일정 조정 |

### 6.3 WBS 트리 뷰

**헤더 영역**
| 요소 | 설명 |
|------|------|
| 아이콘 + 제목 | 📁 WBS 트리 |
| 검색 박스 | Task ID 또는 제목으로 필터링 |
| 펼치기/접기 | 전체 트리 확장/축소 |
| 요약 카드 | WP/ACT/TSK 수, 전체 진행률 |

**트리 노드 표시**
```
[펼침] [아이콘] [제목] [진행률] [Task수] [상태태그]
```

| 요소 | 설명 |
|------|------|
| 펼침 아이콘 | ▼ 펼침 / ▶ 접힘 |
| 레벨 아이콘 | P(보라) / WP(파랑) / A(초록) / T(주황) |
| 제목 | ID + 이름 |
| 진행률 | 프로그레스 바 (%) |
| Task 수 | 하위 Task 개수 |
| 상태 태그 | 카테고리(dev/infra), 상태([dd]) |

**상호작용**
- **클릭**: 노드 선택 → 상세 패널 표시
- **더블클릭**: 펼침/접힘 토글
- **키보드**: 화살표 탐색, Enter 선택

### 6.4 Task 상세 화면

**기본 정보 패널**
- Task ID, 제목, 카테고리
- 우선순위, 담당자
- 일정 (schedule): 시작일 ~ 종료일
- 태그 (tags): 복수 태그 표시
- 의존성 (depends): 선행 Task 링크
- 참조 문서 (ref): PRD, TRD 등 참조 문서 표시

**워크플로우 Stepper**
- 카테고리별 워크플로우 단계를 수평 Stepper로 시각화
- 각 단계는 클릭 가능한 노드로 표시
- 현재 단계 강조 (확대, 그림자 효과)
- 완료된 단계는 체크 아이콘 표시
- 미완료 단계는 비활성화 스타일 적용

**단계 클릭 시 Popover**
1. 완료일 표시 (최상단)
2. Auto 버튼: 현재 상태에서 완료까지 자동 실행
3. 상태 전이 액션: start, approve, build, done, fix, skip
4. 상태 내 액션: ui, review, apply, test, audit, patch
5. 롤백 액션 (선택적)

**버튼 활성화 규칙**
| 단계 상태 | 활성화 버튼 |
|----------|------------|
| 현재 단계 | 모든 관련 액션 |
| 완료된 단계 | 롤백만 (선택적) |
| 미완료 단계 | 모든 버튼 비활성화 |

### 6.5 칸반 보드

**보드 구성**
- 워크플로우 상태별 컬럼
- 컬럼 커스터마이징

**카드 기능**
- 드래그 앤 드롭 상태 변경
- 빠른 편집
- 컨텍스트 메뉴 (LLM 명령어, 문서, 이동)
- 담당자, 우선순위, 라벨 표시

**필터링 및 검색**
- 담당자별 필터
- 카테고리별 필터
- 라벨별 필터
- 제목/설명 검색

### 6.6 Gantt 차트

**차트 구성**
- 계층 구조 표시
- 타임라인 시각화

**기능**
- 드래그로 일정 조정
- 의존성 표시
- 진행률 표시

**확대/축소**
- 일/주/월/분기 뷰

### 6.7 의존관계 그래프

**핵심 기능**
| 기능 | 설명 |
|------|------|
| Hierarchical Layout | 왼쪽(독립) → 오른쪽(의존) 방향 |
| 인터랙티브 | 노드 드래그, 줌, 팬, 클릭 |
| 모달 형태 | 버튼 클릭 시 전체화면 모달 |
| 전체 프로젝트 | 모든 Task 의존관계 표시 |

**노드 스타일**
| 카테고리 | 색상 |
|----------|------|
| development | 파랑 |
| defect | 빨강 |
| infrastructure | 녹색 |

### 6.8 문서 화면

| 화면 | 설명 | 주요 기능 |
|------|------|-----------|
| 문서 뷰어 | 문서 보기 | Markdown 렌더링, 다이어그램 |
| 문서 편집기 | 문서 편집 | Markdown 편집, 실시간 미리보기 |

### 6.9 설정 화면

| 화면 | 설명 | 주요 기능 |
|------|------|-----------|
| 카테고리 관리 | 카테고리 설정 | 카테고리 목록, 추가/수정/삭제, 사용 현황 |
| 워크플로우 관리 | 워크플로우 설정 | 칸반 컬럼 관리, 규칙 관리, 플로우차트 시각화 |

**카테고리 관리 화면 기능**
- 카테고리 목록 표시 (테이블/카드 뷰)
- 카테고리 추가 (ID, 이름, 설명, 아이콘, 색상)
- 카테고리 수정/삭제 (사용 중인 Task 없을 때만 삭제 가능)
- 해당 카테고리를 사용하는 Task 수 표시

**워크플로우 관리 화면 기능**
- 칸반 컬럼 관리 (추가/수정/순서변경/삭제)
- 워크플로우 규칙 시각화 (플로우차트)
- 규칙 추가/수정 (현재상태 → 명령어 → 다음상태 매핑)
- 액션 관리 (반복 가능 여부 포함)
- 규칙 검증 (순환 참조, 도달 불가능 상태 등)

---

## 7. 데이터 구조

### 7.1 디렉토리 구조

```
.jjiban/
├── settings/                      # 전역 설정 (모든 프로젝트 공통)
│   ├── projects.json              # 프로젝트 목록
│   ├── columns.json               # 칸반 컬럼 정의
│   ├── categories.json            # 카테고리 정의
│   ├── workflows.json             # 워크플로우 규칙
│   └── actions.json               # 상태 내 액션 정의
│
├── templates/                     # 문서 템플릿
│   ├── 010-design.md
│   ├── 011-ui-design.md
│   ├── 030-implementation.md
│   ├── 070-test-results.md
│   └── 080-manual.md
│
└── projects/                      # 프로젝트 폴더
    └── [project-id]/              # 개별 프로젝트
        ├── project.json           # 프로젝트 메타데이터
        ├── team.json              # 팀원 목록
        ├── wbs.md                 # WBS 통합 파일 (유일한 소스)
        │
        └── tasks/                 # Task 문서 폴더
            ├── TSK-01-01/         # 3단계: WP-ACT 없이 직접
            │   ├── 010-design.md
            │   └── 030-implementation.md
            └── TSK-01-01-01/      # 4단계: WP-ACT-TSK
                ├── 010-design.md
                └── 030-implementation.md
```

### 7.2 wbs.md 형식

```markdown
# WBS - JJIBAN Project Manager

> version: 1.0
> depth: 4
> updated: 2025-12-26

---

## WP-01: 플랫폼 기반 구축
- status: in_progress
- priority: high
- schedule: 2025-01-15 ~ 2025-02-14
- progress: 25%

### ACT-01-01: 프로젝트 관리
- status: in_progress
- schedule: 2025-01-15 ~ 2025-01-22

#### TSK-01-01-01: 프로젝트 CRUD API 구현
- category: development
- status: implement [im]
- priority: high
- assignee: hong
- schedule: 2025-01-15 ~ 2025-01-21
- tags: api, backend, crud
- depends: -
- blocked-by: -
- test-result: pass

#### TSK-01-01-02: 프로젝트 목록 UI 구현
- category: development
- status: todo [ ]
- priority: high
- assignee: hong
- schedule: 2025-01-22 ~ 2025-01-25
- tags: frontend, ui
- depends: TSK-01-01-01
- test-result: none

---

## WP-02: 칸반 보드
- status: planned
- priority: high
- schedule: 2025-02-15 ~ 2025-03-15

### TSK-02-01: 칸반 컴포넌트 구현
- category: development
- status: todo [ ]
- priority: high
- note: 3단계 구조 예시 (ACT 없이 WP 아래 직접 TSK)
```

### 7.3 wbs.md 문법 규칙

| 레벨 | 마크다운 | ID 패턴 | 예시 |
|------|----------|---------|------|
| WP | `## WP-XX:` | `WP-{2자리}` | `## WP-01: 플랫폼 기반` |
| ACT (4단계) | `### ACT-XX-XX:` | `ACT-{WP}-{순번}` | `### ACT-01-01: 프로젝트 관리` |
| TSK (4단계) | `#### TSK-XX-XX-XX:` | `TSK-{WP}-{ACT}-{순번}` | `#### TSK-01-01-01: API 구현` |
| TSK (3단계) | `### TSK-XX-XX:` | `TSK-{WP}-{순번}` | `### TSK-02-01: 칸반 구현` |

### 7.4 Task 속성

| 속성 | 필수 | 설명 | 예시 |
|------|------|------|------|
| category | O | 작업 유형 | `development`, `defect`, `infrastructure` |
| status | O | 상태 + 기호 | `todo [ ]`, `implement [im]`, `done [xx]` |
| priority | O | 우선순위 | `critical`, `high`, `medium`, `low` |
| assignee | - | 담당자 ID | `hong`, `-` (미지정) |
| schedule | - | 일정 | `2025-01-15 ~ 2025-01-21` |
| tags | - | 태그 목록 | `api, backend, crud` |
| depends | - | 선행 Task | `TSK-01-01-01` |
| blocked-by | - | 차단 Task | `TSK-01-01-01` |
| test-result | - | 테스트 결과 | `none`, `pass`, `fail` |
| note | - | 비고 | 자유 텍스트 |
| completed | - | 단계별 완료시각 | 아래 형식 참조 |

### 7.5 completed 필드 형식

각 워크플로우 단계 완료 시 자동 기록되는 타임스탬프입니다.

```markdown
- completed:
  - dd: 2025-12-15 10:30
  - ap: 2025-12-15 14:20
  - im: 2025-12-16 09:15
  - xx: 2025-12-17 16:00
```

**카테고리별 기록 항목:**

| 카테고리 | 기록 단계 |
|---------|----------|
| development | `dd`, `ap`, `im`, `xx` |
| defect | `an`, `fx`, `vf`, `xx` |
| infrastructure | `dd`, `im`, `xx` |

### 7.6 defect 카테고리 전용 필드

| 필드 | 설명 | 값 |
|------|------|-----|
| severity | 심각도 | critical, major, minor, trivial |
| reproducibility | 재현성 | always, sometimes, rare, unable |
| affectedVersion | 발생 버전 | 버전 문자열 |

---

## 8. 상태 기호 요약

### 8.1 칸반 통합 상태

| 칸반 컬럼 | 통합 상태 | 의미 |
|-----------|-----------|------|
| Todo | `[ ]` | 대기 |
| Design | `[dd]` | 설계 |
| Approve | `[ap]` | 승인 |
| Implement | `[im]` | 구현/수정 |
| Verify | `[vf]` | 검증 |
| Done | `[xx]` | 완료 |

### 8.2 카테고리별 세부 상태

| 기호 | 의미 | 사용 워크플로우 | 칸반 매핑 |
|------|------|----------------|-----------|
| `[ ]` | Todo (대기) | 공통 | Todo |
| `[dd]` | 설계 | development, infrastructure | Design |
| `[an]` | 분석 | defect | Design |
| `[ap]` | 승인 | development | Approve |
| `[im]` | 구현 | development, infrastructure | Implement |
| `[fx]` | 수정 | defect | Implement |
| `[vf]` | 검증 | defect | Verify |
| `[xx]` | 완료 | 공통 | Done |

---

## 9. 명령어 요약

### 9.1 development 카테고리 명령어

**상태 전환 명령어**

| 명령어 | 설명 | 상태 전환 |
|--------|------|----------|
| `design` | 설계 시작 | Todo → 설계 |
| `approve` | 설계 승인 | 설계 → 승인 |
| `build` | 구현 시작 | 승인 → 구현 |
| `done` | 작업 완료 | 구현 → 완료 |

**상태 내 액션 (상태 변경 없음)**

| 명령어 | 사용 가능 상태 | 설명 |
|--------|---------------|------|
| `ui` | 설계 | 화면설계 작성 |
| `review` | 설계 | LLM 설계 리뷰 실행 |
| `apply` | 설계 | 리뷰 내용을 설계서에 반영 |
| `test` | 구현 | TDD/E2E 테스트 실행 |
| `audit` | 구현 | LLM 코드 리뷰 실행 |
| `patch` | 구현 | 리뷰 내용을 코드에 반영 |

### 9.2 defect 카테고리 명령어

**상태 전환 명령어**

| 명령어 | 설명 | 상태 전환 |
|--------|------|----------|
| `start` | 결함 분석 시작 | Todo → 분석 |
| `fix` | 수정 시작 | 분석 → 수정 |
| `verify` | 회귀 테스트 시작 | 수정 → 검증 |
| `done` | 수정 완료 | 검증 → 완료 |

### 9.3 infrastructure 카테고리 명령어

**상태 전환 명령어**

| 명령어 | 설명 | 상태 전환 |
|--------|------|----------|
| `start` | 기술 설계 시작 | Todo → 설계 |
| `skip` | 설계 생략, 바로 구현 | Todo → 구현 |
| `build` | 구현 시작 | 설계 → 구현 |
| `done` | 작업 완료 | 구현 → 완료 |

### 9.4 자동 실행 명령어

| 명령어 | 설명 | 옵션 |
|--------|------|------|
| `run` | 병렬 자동 실행 | `--max N`, `--parallel N` |
| `auto` | 순차 자동 실행 | `--until <target>` |

### 9.5 orchay 스케줄러

→ [orchay-prd.md](./orchay-prd.md) 참조

---

## 10. 테마 시스템

### 10.1 기본 테마 (Dark Blue)

**색상 팔레트**

| 용도 | Hex |
|------|-----|
| 배경 (Background) | `#1a1a2e` |
| 헤더 (Header) | `#16213e` |
| 사이드바 (Sidebar) | `#0f0f23` |
| 카드 배경 (Cards) | `#1e1e38` |
| 프라이머리 (Primary) | `#3b82f6` |
| 성공 (Success) | `#22c55e` |
| 경고 (Warning) | `#f59e0b` |
| 위험 (Danger) | `#ef4444` |
| 텍스트 (Primary) | `#e8e8e8` |
| 텍스트 (Secondary) | `#888888` |
| 보더 (Border) | `#3d3d5c` |

**계층 아이콘 색상**

| 계층 | 색상 | Hex |
|------|------|-----|
| Project | 퍼플 | `#8b5cf6` |
| Work Package | 블루 | `#3b82f6` |
| Activity | 그린 | `#22c55e` |
| Task | 앰버 | `#f59e0b` |

### 10.2 지원 테마 목록

| 테마 ID | 테마명 | 설명 |
|---------|--------|------|
| `dark-blue` | Dark Blue | 기본 다크 테마 |
| `light` | Light | 밝은 테마 |
| `dark` | Dark | 순수 다크 테마 |
| `system` | System | 시스템 설정 따름 |

### 10.3 테마 중앙 관리 시스템

테마는 앱 전체에서 일관되게 적용되도록 중앙 관리 시스템으로 구현합니다.

**중앙 관리 원칙**
| 원칙 | 설명 |
|------|------|
| 단일 소스 | 모든 테마 설정은 하나의 테마 서비스에서 관리 |
| 전역 적용 | 테마 변경 시 모든 화면에 즉시 반영 |
| 상속 구조 | 기본 테마 → 사용자 커스텀 → 컴포넌트별 오버라이드 |
| 반응형 갱신 | 테마 변경 시 실시간으로 UI 업데이트 |

**테마 설정 구조**
```
.jjiban/settings/theme.json
├── activeTheme: "dark-blue"      # 현재 활성 테마 ID
├── customColors: { ... }         # 사용자 커스텀 색상
├── fontSize: "medium"            # 폰트 크기 (small/medium/large)
├── sidebarWidth: 280             # 사이드바 너비 (px)
└── preferences: { ... }          # 기타 UI 설정
```

**테마 토큰 시스템**
| 토큰 유형 | 예시 | 설명 |
|----------|------|------|
| 시맨틱 컬러 | `--color-primary`, `--color-success` | 의미 기반 색상 |
| 표면 컬러 | `--surface-ground`, `--surface-card` | 배경/표면 색상 |
| 텍스트 컬러 | `--text-primary`, `--text-secondary` | 텍스트 색상 |
| 상태 컬러 | `--state-hover`, `--state-focus` | 상태별 색상 |
| 간격 | `--spacing-sm`, `--spacing-md` | 여백/간격 |
| 반경 | `--radius-sm`, `--radius-lg` | 모서리 둥글기 |

**테마 관리 기능**
- **헤더 메뉴**: 테마 선택 드롭다운
- **설정 페이지**: 상세 테마 설정
- **로컬 저장**: 사용자 선택 저장 (theme.json)
- **프라이머리 색상 변경**: 커스터마이징 가능
- **폰트 크기 조절**: 소/중/대
- **사이드바 너비 조절**
- **테마 미리보기**: 적용 전 미리보기 지원
- **테마 초기화**: 기본 테마로 복원

**테마 적용 우선순위**
1. 컴포넌트별 오버라이드 (최우선)
2. 사용자 커스텀 설정
3. 선택된 테마 프리셋
4. 시스템 기본값 (폴백)

---

## 11. 비기능 요구사항

### 11.1 성능

| 항목 | 기준 |
|------|------|
| 앱 시작 시간 | 3초 이내 |
| 페이지 전환 | 500ms 이내 |
| 파일 로딩 (1,000 태스크) | 300ms 이내 |
| 트리 렌더링 (1,000 노드) | 500ms 이내 |
| 검색 반응 | 100ms 이내 |

### 11.2 호환성

| 플랫폼 | 요구사항 |
|--------|----------|
| Windows | Windows 10 이상 |
| macOS | macOS 10.15 (Catalina) 이상 |
| Linux | Ubuntu 20.04 LTS 이상 |

### 11.3 접근성

- 키보드 네비게이션 지원
- 스크린 리더 호환
- 고대비 모드 지원

### 11.4 안정성

| 시나리오 | 처리 |
|---------|------|
| 파일 읽기 실패 | 에러 메시지 + 재시도 |
| 파일 쓰기 실패 | 자동 백업 + 알림 |
| 앱 크래시 | 자동 복구 + 로그 저장 |

### 11.5 보안

- 로컬 파일만 접근 (외부 네트워크 불필요)
- 민감 정보 암호화 저장 (설정)
- XSS/인젝션 방지

---

## 12. Git 동기화 워크플로우

### 12.1 분산 파일의 장점

```bash
# 홍길동 (집): TSK-001 수정
# 김철수 (회사): TSK-002 수정

# 분산 파일 → 자동 병합 성공!
# 단일 파일 → 충돌 발생!
```

| 상황 | 단일 파일 | 분산 파일 |
|------|----------|-----------|
| 다른 태스크 동시 수정 | ❌ 충돌 | ✅ 자동 병합 |
| 같은 태스크 동시 수정 | ❌ 충돌 | ❌ 충돌 (불가피) |
| 충돌 해결 난이도 | 어려움 | 쉬움 |
| PR 리뷰 | 어려움 | 명확함 |

### 12.2 권장 워크플로우

```bash
# 1. 작업 시작 전 (필수!)
git pull

# 2. 작업 중
jjiban  # 로컬에서 태스크 관리

# 3. 작업 완료 후
git add .jjiban
git commit -m "TSK-001 완료"
git pull --rebase  # 충돌 확인
git push
```

### 12.3 충돌 최소화 규칙

1. **작업 전 항상 pull** - 최신 상태 유지
2. **작업 후 바로 push** - 변경사항 빨리 공유
3. **태스크 분배 명확히** - 같은 태스크 동시 작업 피함

---

## 변경 이력

| 버전 | 날짜 | 변경 내용 |
|------|------|-----------|
| 1.0 | 2025-12-26 | 통합 PRD 작성 (Flutter 기반, Option A 워크플로우 적용) |
| 1.1 | 2025-12-27 | 외부 멀티플렉서 연동 섹션 추가 |
| 1.2 | 2025-12-27 | LLM/터미널 섹션 분리 → orchay-prd.md |
