# TRD: orchay_web - 기술 요구사항 정의서

## 문서 정보

| 항목 | 내용 |
|------|------|
| 문서 버전 | 1.0 |
| 작성일 | 2025-12-28 |
| PRD 버전 | 1.0 |
| 상태 | Draft |

---

## 기술 스택

### 핵심 기술

| 계층 | 기술 | 버전 | 선정 근거 |
|-----|------|------|----------|
| 웹 프레임워크 | FastAPI | ^0.115 | 비동기, 경량, Starlette 기반 |
| 템플릿 | Jinja2 | ^3.0 | FastAPI 네이티브 지원 |
| 동적 UI | HTMX | 2.0 (CDN) | 빌드 불필요, HTML 속성만으로 동적 UI |
| 스타일링 | Tailwind CSS | 3.x (CDN) | 빌드 불필요, 다크테마 쉬움 |

### 선정 근거

| 결정 | 이유 |
|------|------|
| **HTMX > React** | 빌드 도구 불필요, Python 단일 스택 유지 |
| **Tailwind CDN** | 별도 CSS 빌드 없이 다크테마 + 반응형 |
| **FastAPI** | orchay가 이미 asyncio 기반, 자연스러운 통합 |
| **SSE > WebSocket** | 단방향 업데이트만 필요, 구현 단순 |

---

## 아키텍처

### 파일 구조

```
orchay/src/orchay/
├── web/
│   ├── __init__.py
│   ├── server.py         # FastAPI 앱, 라우트
│   ├── templates/
│   │   ├── base.html     # 기본 레이아웃
│   │   ├── index.html    # 메인 페이지
│   │   └── partials/
│   │       ├── tree.html      # WBS 트리 조각
│   │       ├── detail.html    # Task 상세 조각
│   │       └── workers.html   # Worker 상태 조각
│   └── static/
│       └── style.css     # 추가 스타일 (선택)
└── main.py               # --web 옵션 추가
```

### 데이터 흐름

```
┌─────────────────────────────────────────────────────────────┐
│                      Orchestrator                           │
│  self.tasks, self.workers, self.mode (메모리)              │
└─────────────────────┬───────────────────────────────────────┘
                      │ 참조
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Server                           │
│  GET /              → index.html (전체 페이지)             │
│  GET /api/tree      → tree.html (HTMX 조각)                │
│  GET /api/detail/ID → detail.html (HTMX 조각)              │
│  GET /api/workers   → workers.html (HTMX 조각)             │
└─────────────────────┬───────────────────────────────────────┘
                      │ HTTP
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                     Browser (HTMX)                          │
│  hx-get="/api/tree" hx-trigger="every 5s"                  │
│  hx-get="/api/workers" hx-trigger="every 5s"               │
└─────────────────────────────────────────────────────────────┘
```

---

## API 설계

### 라우트

| 메서드 | 경로 | 응답 | 설명 |
|--------|------|------|------|
| GET | `/` | HTML | 메인 페이지 (전체) |
| GET | `/api/tree` | HTML 조각 | WBS 트리 |
| GET | `/api/tree/{wp_id}` | HTML 조각 | WP 하위 노드 (확장) |
| GET | `/api/detail/{task_id}` | HTML 조각 | Task 상세 |
| GET | `/api/workers` | HTML 조각 | Worker 상태 바 |
| GET | `/api/progress` | HTML 조각 | 전체 진행률 |

### HTMX 패턴

```html
<!-- 5초마다 자동 갱신 -->
<div id="workers"
     hx-get="/api/workers"
     hx-trigger="every 5s"
     hx-swap="innerHTML">
  ...
</div>

<!-- 트리 노드 확장/축소 -->
<div class="tree-node"
     hx-get="/api/tree/WP-08"
     hx-trigger="click"
     hx-target="next .children"
     hx-swap="innerHTML">
  ▶ WP-08
</div>
<div class="children"></div>

<!-- Task 클릭 시 상세 패널 로드 -->
<div class="task"
     hx-get="/api/detail/TSK-08-01"
     hx-trigger="click"
     hx-target="#detail-panel">
  TSK-08-01
</div>
```

---

## UI 스타일링

### Tailwind + 다크테마

```html
<body class="bg-gray-900 text-gray-100">
  <div class="flex h-screen">
    <!-- 좌측: 트리 -->
    <div class="w-1/2 border-r border-gray-700 overflow-auto">
      ...
    </div>
    <!-- 우측: 상세 -->
    <div class="w-1/2 p-4">
      ...
    </div>
  </div>
</body>
```

### 상태 색상 (workflows.json 연동)

```python
STATUS_COLORS = {
    "[ ]": "bg-gray-500",
    "[bd]": "bg-blue-500",
    "[dd]": "bg-purple-500",
    "[ap]": "bg-green-500",
    "[im]": "bg-yellow-500",
    "[xx]": "bg-emerald-500",
}
```

---

## 트리 UI 구현

### CSS 애니메이션

```css
.children {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s ease;
}
.children.open {
  max-height: 2000px;
}

.tree-node:hover {
  background: rgba(59, 130, 246, 0.1);
}
```

### 계층 들여쓰기

```html
<!-- 레벨별 padding-left -->
<div class="pl-0">WP-01</div>
<div class="pl-4">ACT-01-01</div>
<div class="pl-8">TSK-01-01-01</div>
```

---

## 의존성 추가

### pyproject.toml 수정

```toml
dependencies = [
    "textual>=1.0",
    "rich>=14.0",
    "watchdog>=4.0",
    "pydantic>=2.0",
    "fastapi>=0.115",      # 추가
    "uvicorn[standard]",   # 추가
    "jinja2>=3.0",         # 추가
]
```

---

## 통합 방법

### main.py 수정

```python
# 기존 Orchestrator에 웹서버 추가
if args.web or args.web_only:
    from orchay.web.server import create_app
    app = create_app(orchestrator)

    # 백그라운드에서 웹서버 실행
    config = uvicorn.Config(app, host="127.0.0.1", port=args.port)
    server = uvicorn.Server(config)

    if args.web_only:
        # 웹서버만 실행
        await server.serve()
    else:
        # 스케줄러 + 웹서버 병렬 실행
        await asyncio.gather(
            orchestrator.run(),
            server.serve()
        )
```

---

## AI 코딩 가이드라인

### 권장 사항

- FastAPI 라우트는 async 함수 사용
- Jinja2 템플릿에서 HTMX 속성 활용
- Tailwind 유틸리티 클래스 사용 (커스텀 CSS 최소화)
- workflows.json 상태/색상 연동
- Type hints 필수

### 금지 사항

- JavaScript 프레임워크 (React, Vue 등) 사용 금지
- npm/빌드 도구 사용 금지
- 동기 블로킹 I/O 금지
- 하드코딩된 색상/상태 금지

---

## 변경 이력

| 버전 | 날짜 | 변경 내용 |
|------|------|-----------|
| 1.0 | 2025-12-28 | 초기 TRD 작성 |
