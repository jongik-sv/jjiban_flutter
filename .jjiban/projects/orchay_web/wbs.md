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
- status: done [xx]
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
- status: done [xx]
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
- status: done [xx]
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
- status: done [xx]
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
- status: done [xx]
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
- status: done [xx]
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
- status: done [xx]
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
- status: done [xx]
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
  - hx-swap="morph:innerHTML" (DOM morphing으로 깜빡임 없는 갱신)
  - htmx-ext-morph 2.0 확장 필수

#### 버그 수정 이력
- **2025-12-28**: idiomorph CDN 경로 수정 (HTMX 2.0 호환)
  - 원인: `idiomorph@0.3.0/dist/idiomorph-ext.min.js`가 HTMX 2.0과 호환되지 않음
  - 수정: `htmx-ext-morph@2.0.0/morph.js`로 변경
  - 결과: morph 확장 정상 작동, 깜빡임 해소

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
- status: done [xx]
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
- status: done [xx]
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
- status: done [xx]
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

## WP-05: Document Viewer
- status: planned
- priority: high
- schedule: 2026-01-06 ~ 2026-01-07
- progress: 0%
- note: 문서 및 이미지 뷰어 모달

### TSK-05-01: Document Viewer 구현
- category: development
- domain: fullstack
- status: done [xx]
- priority: high
- assignee: -
- schedule: 2026-01-06 ~ 2026-01-07
- tags: viewer, markdown, mermaid, modal
- depends: TSK-03-01

#### PRD 요구사항
- prd-ref: PRD 3.5 Document Viewer
- requirements:
  - 문서 API 엔드포인트 (/api/document/{task_id}/{doc_name})
  - MD 파일 렌더링 (marked.js)
  - Mermaid 다이어그램 지원
  - 이미지 파일 표시 (png, jpg, gif, webp)
  - 모달 팝업 UI
  - ESC 키로 닫기
- acceptance:
  - 문서 클릭 시 모달에 내용 표시
  - Mermaid 코드블록 다이어그램 렌더링
  - 이미지 정상 표시
  - Path traversal 공격 차단

#### 기술 스펙 (TRD)
- tech-spec:
  - marked.js (CDN) - 마크다운 렌더링
  - mermaid.js (CDN) - 다이어그램 (다크 테마)
  - FastAPI FileResponse/PlainTextResponse
- api-spec:
  - GET /api/document/{task_id}/{doc_name}
    - .md → PlainTextResponse (클라이언트 렌더링)
    - 이미지 → FileResponse
- security-spec:
  - Path traversal 방지: is_relative_to() 검증
  - 허용 확장자: .md, .png, .jpg, .jpeg, .gif, .webp

---

## WP-06: UI 개선 (Vue 스타일)
- status: planned
- priority: high
- schedule: 2026-01-08 ~ 2026-01-10
- progress: 0%
- note: Vue WBS 페이지 스타일 적용

### TSK-06-01: 트리 패널 개선
- category: development
- domain: frontend
- status: done [xx]
- priority: high
- assignee: -
- schedule: 2026-01-08 ~ 2026-01-08
- tags: tree, stats, search, ui
- depends: TSK-02-02

#### PRD 요구사항
- prd-ref: PRD 3.6.2 트리 패널 개선, PRD 3.6.3 트리 노드 인터랙션
- requirements:
  - 통계 배지 (WP/ACT/TSK 개수, 전체 진행률)
  - 검색창 (Task ID/제목 필터링)
  - 전체 펼치기/접기 버튼
  - WP/ACT 텍스트 클릭 → Detail 패널에 설명 표시
  - 앞 아이콘 클릭 → 트리 열기/닫기
- acceptance:
  - 통계 배지에 정확한 수치 표시
  - 검색 시 실시간 필터링
  - 펼치기/접기 일괄 동작
  - WP/ACT 클릭 시 Detail 패널 업데이트

#### 기술 스펙 (TRD)
- tech-spec:
  - 통계 계산: server.py에서 WP/ACT/TSK 집계
  - 검색: 클라이언트 사이드 JavaScript 필터
  - 펼치기/접기: expandAll(), collapseAll() 함수
- ui-spec:
  - 통계 배지: flex gap-4, 둥근 카드 형태
  - 검색창: w-full, bg-gray-800, border rounded

---

### TSK-06-02: Task Detail 패널 개선
- category: development
- domain: frontend
- status: done [xx]
- priority: high
- assignee: -
- schedule: 2026-01-09 ~ 2026-01-09
- tags: detail, card, stepper, ui
- depends: TSK-03-01

#### PRD 요구사항
- prd-ref: PRD 3.6.4 Task Detail 패널 개선
- requirements:
  - 카드 기반 섹션 분리 (기본 정보, 진행 상태, 요구사항, 기술 스펙)
  - Task ID 배지 형태 (프로젝트 + 카테고리 + ID)
  - 워크플로우 스테퍼 (시작 전 → 설계 → 구현 → 완료)
  - 진행률 바 표시
  - PRD 요구사항 표시 섹션
  - 기술 스펙 표시 섹션
  - 각 섹션 접기/펼치기 기능
- acceptance:
  - 각 섹션이 카드로 분리되어 표시
  - 워크플로우 스테퍼에서 현재 단계 하이라이트
  - 요구사항/기술 스펙 정확히 표시

#### 기술 스펙 (TRD)
- tech-spec:
  - 카드 스타일: bg-gray-800 rounded-lg p-4 mb-4
  - 스테퍼: flex items-center, 원형 아이콘 + 연결선
  - 접기/펼치기: CSS max-height transition
- ui-spec:
  - 배지: px-2 py-1 rounded text-sm
  - 진행률 바: bg-gray-700 h-2 rounded-full

---

### TSK-06-03: 문서 테이블
- category: development
- domain: frontend
- status: done [xx]
- priority: medium
- assignee: -
- schedule: 2026-01-10 ~ 2026-01-10
- tags: document, table, ui
- depends: TSK-05-01, TSK-06-02

#### PRD 요구사항
- prd-ref: PRD 3.6.4 관련 문서 섹션
- requirements:
  - 문서 테이블 형태 표시 (문서명, 타입, 크기, 수정일)
  - 클릭 시 TSK-05-01 Document Viewer 호출
  - 접기/펼치기 기능
- acceptance:
  - 문서 목록이 테이블로 표시
  - 파일 메타정보 (타입, 크기, 수정일) 정확히 표시
  - 클릭 시 Document Viewer 모달 열림

#### 기술 스펙 (TRD)
- tech-spec:
  - 문서 메타정보: server.py에서 파일 stat 조회
  - 테이블: w-full text-sm, hover:bg-gray-700
  - Document Viewer 호출: openDocument(taskId, docName)
- api-spec:
  - 기존 /api/detail/{task_id} 응답에 documents 메타정보 포함

---

## 요약

| 단계 | Task 수 | 개발 방식 | 예상 기간 |
|------|---------|----------|----------|
| WP-01 (기본 구조) | 3개 | 순차 | 2일 |
| WP-02 (트리 UI) | 3개 | 순차 | 2일 |
| WP-03 (상세/상태) | 3개 | 순차 | 2일 |
| WP-04 (마무리) | 3개 | 순차 | 2일 |
| WP-05 (Document Viewer) | 1개 | 순차 | 2일 |
| WP-06 (UI 개선) | 3개 | 순차 | 3일 |
| **총합** | **16개** | - | **13일** |

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
    ├─────────────────────┼─────────────────┐
    ▼                     ▼                 ▼
TSK-03-02           TSK-02-03          TSK-06-01
(Worker 상태)       (트리 인터랙션)    (트리 패널 개선)
    │                     │
    └──────────┬──────────┘
               ▼
         TSK-03-01
         (Task 상세)
               │
    ┌──────────┼──────────┐
    ▼          ▼          ▼
TSK-03-03  TSK-05-01  TSK-06-02
(실시간)   (Doc Viewer) (Detail 개선)
               │          │
               └────┬─────┘
                    ▼
              TSK-06-03
              (문서 테이블)
                    │
                    ▼
   TSK-04-01 → TSK-04-02 → TSK-04-03
   (의존성)    (테스트)    (문서화)
```
