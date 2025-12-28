# WBS - orchay_web (웹 모니터링 UI)

> version: 1.0
> depth: 3
> updated: 2025-12-28
> project-root: orchay
> strategy: 기존 orchay에 web/ 모듈 추가

---

## WP-01: 웹서버 기본 구조
- status: planned
- priority: critical
- schedule: 2025-12-29 ~ 2025-12-30
- progress: 0%
- note: FastAPI + Jinja2 + HTMX 기본 구조 구축

### TSK-01-01: FastAPI 앱 및 라우트 정의
- category: development
- domain: backend
- status: done [xx]
- priority: critical
- assignee: -
- schedule: 2025-12-29 ~ 2025-12-29
- tags: fastapi, routing, api
- depends: -

#### PRD 요구사항
- prd-ref: PRD 3.4 CLI 옵션
- requirements:
  - FastAPI 앱 생성 (create_app 함수)
  - Orchestrator 참조 주입
  - 기본 라우트 정의 (/, /api/tree, /api/detail, /api/workers)
  - 정적 파일 서빙 설정
- acceptance:
  - uvicorn으로 서버 실행 가능
  - GET / 요청 시 HTML 응답
  - Orchestrator 데이터 접근 가능

#### 기술 스펙 (TRD)
- tech-spec:
  - FastAPI ^0.115, uvicorn[standard]
  - Starlette StaticFiles, Jinja2Templates
- api-spec:
  - GET / → index.html
  - GET /api/tree → tree.html (partial)
  - GET /api/detail/{task_id} → detail.html (partial)
  - GET /api/workers → workers.html (partial)

---

### TSK-01-02: Jinja2 템플릿 기본 구조
- category: development
- domain: frontend
- status: approved [ap]
- priority: critical
- assignee: -
- schedule: 2025-12-29 ~ 2025-12-29
- tags: jinja2, template, html
- depends: TSK-01-01

#### PRD 요구사항
- prd-ref: PRD 2.1 레이아웃
- requirements:
  - base.html 레이아웃 (헤더, 메인, 푸터)
  - index.html 메인 페이지 (2열 레이아웃)
  - HTMX CDN 포함
  - Tailwind CSS CDN 포함
- acceptance:
  - 다크테마 적용된 페이지 렌더링
  - 2열 레이아웃 (트리 | 상세)
  - 반응형 기본 지원

#### 기술 스펙 (TRD)
- tech-spec:
  - Jinja2 ^3.0 템플릿 엔진
  - HTMX 2.0 CDN
  - Tailwind CSS 3.x CDN
- ui-spec:
  - 레이아웃: flex h-screen
  - 좌측 50%: WBS 트리
  - 우측 50%: Task 상세

---

### TSK-01-03: CLI 옵션 및 서버 통합
- category: development
- domain: backend
- status: approved [ap]
- priority: high
- assignee: -
- schedule: 2025-12-30 ~ 2025-12-30
- tags: cli, argparse, integration
- depends: TSK-01-01

#### PRD 요구사항
- prd-ref: PRD 3.4 CLI 옵션
- requirements:
  - --web 옵션 추가 (웹서버 포함 실행)
  - --web-only 옵션 추가 (웹서버만 실행)
  - --port 옵션 추가 (기본 8080)
  - Orchestrator와 웹서버 병렬 실행
- acceptance:
  - `orchay --web` 실행 시 TUI + 웹서버 동시 실행
  - `orchay --web-only` 실행 시 웹서버만 실행
  - 지정 포트로 서버 바인딩

#### 기술 스펙 (TRD)
- tech-spec:
  - argparse CLI 옵션 확장
  - asyncio.gather로 병렬 실행
  - uvicorn.Server 비동기 실행

---

## WP-02: WBS 트리 UI
- status: planned
- priority: high
- schedule: 2025-12-31 ~ 2026-01-01
- progress: 0%
- note: WBS 계층 구조 시각화 및 인터랙션

### TSK-02-01: 트리 데이터 API
- category: development
- domain: backend
- status: approved [ap]
- priority: high
- assignee: -
- schedule: 2025-12-31 ~ 2025-12-31
- tags: api, tree, data
- depends: TSK-01-01

#### PRD 요구사항
- prd-ref: PRD 3.1 WBS 트리
- requirements:
  - WBS 트리 구조 API 엔드포인트
  - Task를 WP/ACT 계층으로 그룹화
  - 각 노드의 진행률 계산
  - 확장/축소 상태 관리
- acceptance:
  - /api/tree 요청 시 전체 트리 반환
  - /api/tree/{wp_id} 요청 시 하위 노드만 반환
  - 진행률 정확히 계산

#### 기술 스펙 (TRD)
- tech-spec:
  - Orchestrator.tasks에서 트리 구조 생성
  - Task.id 파싱으로 계층 구분
- api-spec:
  - GET /api/tree → 전체 트리 HTML
  - GET /api/tree/{wp_id} → WP 하위 노드 HTML

---

### TSK-02-02: 트리 템플릿 구현
- category: development
- domain: frontend
- status: approved [ap]
- priority: high
- assignee: -
- schedule: 2025-12-31 ~ 2025-12-31
- tags: template, tree, ui
- depends: TSK-02-01

#### PRD 요구사항
- prd-ref: PRD 3.1 WBS 트리
- requirements:
  - tree.html 파셜 템플릿
  - 계층별 들여쓰기 (pl-0, pl-4, pl-8)
  - 상태 기호별 색상 표시
  - 확장/축소 아이콘 (▶/▼)
- acceptance:
  - 트리 노드 정확히 렌더링
  - 상태별 색상 구분 명확
  - 클릭 가능한 노드 표시

#### 기술 스펙 (TRD)
- tech-spec:
  - Jinja2 재귀 매크로 또는 반복문
  - Tailwind 유틸리티 클래스
- ui-spec:
  - WP: font-bold, 아이콘 WP
  - ACT: font-medium, 아이콘 A
  - TSK: font-normal, 아이콘 T

---

### TSK-02-03: 트리 인터랙션 구현
- category: development
- domain: frontend
- status: detail-design [dd]
- priority: medium
- assignee: -
- schedule: 2026-01-01 ~ 2026-01-01
- tags: htmx, interaction, toggle
- depends: TSK-02-02

#### PRD 요구사항
- prd-ref: PRD 3.1 WBS 트리
- requirements:
  - 노드 클릭 시 확장/축소
  - Task 클릭 시 상세 패널 로드
  - 부드러운 애니메이션 전환
  - 5초마다 자동 갱신
- acceptance:
  - 클릭으로 하위 노드 토글
  - Task 선택 시 우측 패널 업데이트
  - 애니메이션 0.3초

#### 기술 스펙 (TRD)
- tech-spec:
  - HTMX hx-get, hx-trigger, hx-target, hx-swap
  - CSS transition max-height
- ui-spec:
  - hx-trigger="click" (토글)
  - hx-trigger="every 5s" (자동 갱신)

---

## WP-03: Task 상세 및 Worker 상태
- status: planned
- priority: high
- schedule: 2026-01-02 ~ 2026-01-03
- progress: 0%
- note: Task 상세 패널 및 Worker 상태 바

### TSK-03-01: Task 상세 API 및 템플릿
- category: development
- domain: fullstack
- status: approved [ap]
- priority: high
- assignee: -
- schedule: 2026-01-02 ~ 2026-01-02
- tags: api, detail, template
- depends: TSK-02-02

#### PRD 요구사항
- prd-ref: PRD 3.2 Task 상세 패널
- requirements:
  - Task 상세 정보 API
  - detail.html 파셜 템플릿
  - 모든 Task 속성 표시 (ID, 제목, 상태, 카테고리 등)
  - 관련 문서 링크 목록
- acceptance:
  - /api/detail/{task_id} 요청 시 상세 정보 반환
  - 모든 필드 정확히 렌더링
  - 문서 링크 클릭 가능

#### 기술 스펙 (TRD)
- tech-spec:
  - Task 모델에서 직접 데이터 추출
  - 문서 경로: .jjiban/projects/{project}/tasks/{task_id}/
- ui-spec:
  - 레이아웃: 세로 정렬, 섹션 구분
  - 상태 배지: 색상 + 아이콘

---

### TSK-03-02: Worker 상태 바 구현
- category: development
- domain: fullstack
- status: approved [ap]
- priority: high
- assignee: -
- schedule: 2026-01-02 ~ 2026-01-02
- tags: worker, status, bar
- depends: TSK-01-02

#### PRD 요구사항
- prd-ref: PRD 3.3 Worker 상태 표시
- requirements:
  - Worker 상태 바 API
  - workers.html 파셜 템플릿
  - 상태별 아이콘 및 색상 표시
  - 현재 작업 중인 Task 표시
- acceptance:
  - /api/workers 요청 시 상태 바 반환
  - 각 Worker 상태 정확히 표시
  - 실시간 갱신 동작

#### 기술 스펙 (TRD)
- tech-spec:
  - Orchestrator.workers에서 데이터 추출
  - WorkerState enum 매핑
- ui-spec:
  - 가로 배열 (flex gap-4)
  - 상태: idle 🟢, busy 🟡, error 🔴

---

### TSK-03-03: 실시간 자동 갱신
- category: development
- domain: frontend
- status: detail-design [dd]
- priority: medium
- assignee: -
- schedule: 2026-01-03 ~ 2026-01-03
- tags: htmx, polling, realtime
- depends: TSK-03-01, TSK-03-02

#### PRD 요구사항
- prd-ref: PRD 2.3 실시간 갱신
- requirements:
  - Worker 상태 5초마다 갱신
  - 전체 진행률 5초마다 갱신
  - 선택된 Task 상세 자동 갱신
- acceptance:
  - 상태 변경 시 5초 내 UI 반영
  - 네트워크 오류 시 graceful 처리
  - 갱신 중 깜빡임 최소화

#### 기술 스펙 (TRD)
- tech-spec:
  - HTMX hx-trigger="every 5s"
  - hx-swap="innerHTML" (부분 교체)

---

## WP-04: 마무리 및 테스트
- status: planned
- priority: medium
- schedule: 2026-01-04 ~ 2026-01-05
- progress: 0%
- note: 테스트, 문서화, 스타일 정리

### TSK-04-01: 의존성 및 pyproject.toml 업데이트
- category: infrastructure
- domain: infra
- status: approved [ap]
- priority: high
- assignee: -
- schedule: 2026-01-04 ~ 2026-01-04
- tags: deps, config
- depends: -

#### PRD 요구사항
- prd-ref: TRD 의존성 추가
- requirements:
  - fastapi, uvicorn, jinja2 의존성 추가
  - pyproject.toml 업데이트
- acceptance:
  - `uv pip install -e .` 성공
  - 모든 의존성 정상 설치

#### 기술 스펙 (TRD)
- tech-spec:
  - fastapi>=0.115
  - uvicorn[standard]
  - jinja2>=3.0

---

### TSK-04-02: 통합 테스트
- category: development
- domain: test
- status: detail-design [dd]
- priority: medium
- assignee: -
- schedule: 2026-01-04 ~ 2026-01-05
- tags: test, integration
- depends: TSK-03-03

#### PRD 요구사항
- prd-ref: PRD 4 비기능 요구사항
- requirements:
  - 웹서버 시작/종료 테스트
  - API 엔드포인트 응답 테스트
  - HTMX 인터랙션 테스트
- acceptance:
  - 모든 테스트 통과
  - 페이지 로드 < 1초

#### 기술 스펙 (TRD)
- tech-spec:
  - pytest, pytest-asyncio
  - httpx (FastAPI 테스트 클라이언트)

---

### TSK-04-03: 문서화
- category: development
- domain: docs
- status: detail-design [dd]
- priority: low
- assignee: -
- schedule: 2026-01-05 ~ 2026-01-05
- tags: docs, readme
- depends: TSK-04-02

#### PRD 요구사항
- prd-ref: -
- requirements:
  - README.md 웹 UI 섹션 추가
  - CLI 옵션 문서화
  - 스크린샷 추가 (선택)
- acceptance:
  - 사용법 명확히 설명
  - 옵션 목록 완전

---

## 요약

| 단계 | Task 수 | 개발 방식 | 예상 기간 |
|------|---------|----------|----------|
| WP-01 (기본 구조) | 3개 | 순차 | 2일 |
| WP-02 (트리 UI) | 3개 | 순차 | 2일 |
| WP-03 (상세/상태) | 3개 | 순차 | 2일 |
| WP-04 (마무리) | 3개 | 순차 | 2일 |
| **총합** | **12개** | - | **8일** |

### 의존성 그래프

```
TSK-01-01 (FastAPI 앱)
    │
    ├──────────┬──────────┐
    ▼          ▼          ▼
TSK-01-02  TSK-01-03  TSK-02-01
(템플릿)    (CLI)      (트리 API)
    │                     │
    │                     ▼
    │               TSK-02-02
    │               (트리 템플릿)
    │                     │
    ├─────────────────────┤
    ▼                     ▼
TSK-03-02           TSK-02-03
(Worker 상태)       (트리 인터랙션)
    │                     │
    └──────────┬──────────┘
               ▼
         TSK-03-01
         (Task 상세)
               │
               ▼
         TSK-03-03
         (실시간 갱신)
               │
               ▼
         TSK-04-01 → TSK-04-02 → TSK-04-03
         (의존성)    (테스트)    (문서화)
```
