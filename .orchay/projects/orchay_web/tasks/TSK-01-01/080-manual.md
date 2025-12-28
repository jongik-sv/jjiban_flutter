# 사용자 매뉴얼 - FastAPI 앱 및 라우트 정의

## 0. 문서 메타데이터

| 항목 | 내용 |
|------|------|
| Task ID | TSK-01-01 |
| Task 명 | FastAPI 앱 및 라우트 정의 |
| 문서 버전 | 1.0 |
| 작성일 | 2025-12-28 |
| 대상 사용자 | orchay 개발자, 시스템 통합 담당자 |

---

## 1. 개요

### 1.1 기능 소개

**orchay 웹 서버 모듈**은 FastAPI 기반의 내장 웹 서버로, WBS 트리와 Task 진행 상황을 브라우저에서 모니터링할 수 있는 HTTP API를 제공합니다.

**주요 기능:**
- FastAPI 애플리케이션 생성 (`create_app` 함수)
- Orchestrator 참조 주입을 통한 실시간 데이터 접근
- HTMX 기반 부분 렌더링을 위한 HTML 조각 API
- Jinja2 템플릿 렌더링 및 정적 파일 서빙

### 1.2 대상 사용자

| 사용자 유형 | 역할 | 주요 활용 |
|------------|------|----------|
| 개발자 | orchay 확장 개발 | 웹 모듈 통합, API 확장 |
| 시스템 관리자 | 서버 운영 | CLI 옵션으로 웹 서버 실행 |

---

## 2. 시작하기

### 2.1 사전 요구사항

- Python 3.10 이상
- orchay 패키지 설치
- 의존성: `fastapi>=0.115`, `uvicorn[standard]`, `jinja2>=3.0`

### 2.2 설치 확인

```bash
cd orchay
uv pip install -e ".[dev]"

# 의존성 확인
python -c "from orchay.web.server import create_app; print('OK')"
```

### 2.3 기본 사용법

```python
from orchay.main import Orchestrator
from orchay.web.server import create_app
import uvicorn

# Orchestrator 인스턴스 생성
orchestrator = Orchestrator(project="my_project")

# FastAPI 앱 생성
app = create_app(orchestrator)

# 서버 실행
uvicorn.run(app, host="127.0.0.1", port=8080)
```

---

## 3. 사용 방법

### 3.1 API 엔드포인트

| HTTP 메서드 | 경로 | 설명 | 응답 타입 |
|------------|------|------|----------|
| GET | `/` | 메인 페이지 | HTML |
| GET | `/api/tree` | WBS 트리 조각 | HTML 조각 |
| GET | `/api/detail/{task_id}` | Task 상세 조각 | HTML 조각 |
| GET | `/api/workers` | Worker 상태 조각 | HTML 조각 |

### 3.2 메인 페이지 (/)

브라우저에서 루트 URL에 접속하면 `index.html` 템플릿이 렌더링됩니다.

**요청 예시:**
```bash
curl http://localhost:8080/
```

**템플릿 컨텍스트:**
| 변수 | 설명 | 예시 |
|------|------|------|
| `project` | 프로젝트명 | `"orchay_web"` |
| `mode` | 실행 모드 | `"quick"` |

### 3.3 WBS 트리 API (/api/tree)

WBS 계층 구조를 HTML 조각으로 반환합니다. HTMX의 `hx-get` 속성으로 동적 로드에 사용됩니다.

**요청 예시:**
```bash
curl http://localhost:8080/api/tree
```

**응답 구조:**
- WP(Work Package) → ACT(Activity) → Task 계층으로 그룹화
- 각 Task의 상태 코드별 색상 표시

**템플릿 컨텍스트:**
| 변수 | 타입 | 설명 |
|------|------|------|
| `tree` | `dict[str, dict[str, list[Task]]]` | WP → ACT → Task 계층 |

### 3.4 Task 상세 API (/api/detail/{task_id})

특정 Task의 상세 정보를 HTML 조각으로 반환합니다.

**요청 예시:**
```bash
curl http://localhost:8080/api/detail/TSK-01-01
```

**성공 응답 (200):**
- Task 속성: ID, 제목, 상태, 카테고리, 우선순위, 의존성
- 관련 문서 링크 목록

**에러 응답 (404):**
```html
<div class="error">Task 'TSK-99-99'를 찾을 수 없습니다</div>
```

**템플릿 컨텍스트:**
| 변수 | 타입 | 설명 |
|------|------|------|
| `task` | `Task` | Task 객체 (성공 시) |
| `message` | `str` | 에러 메시지 (실패 시) |

### 3.5 Worker 상태 API (/api/workers)

Worker 상태 바를 HTML 조각으로 반환합니다. 5초마다 자동 갱신됩니다.

**요청 예시:**
```bash
curl http://localhost:8080/api/workers
```

**템플릿 컨텍스트:**
| 변수 | 타입 | 설명 |
|------|------|------|
| `workers` | `list[Worker]` | Worker 목록 |

---

## 4. FAQ

### Q1. Orchestrator 없이 앱을 생성할 수 있나요?

**A:** 아니요. `create_app(orchestrator)` 함수는 반드시 Orchestrator 인스턴스를 인자로 받아야 합니다. Orchestrator는 Task와 Worker 데이터의 소스입니다.

### Q2. 정적 파일은 어디에 저장하나요?

**A:** `orchay/src/orchay/web/static/` 디렉토리에 저장합니다. 이 디렉토리가 존재하면 `/static` 경로로 마운트됩니다.

### Q3. 템플릿 파일은 어디에 있나요?

**A:** `orchay/src/orchay/web/templates/` 디렉토리에 있습니다.
- `index.html`: 메인 페이지
- `partials/tree.html`: WBS 트리 조각
- `partials/detail.html`: Task 상세 조각
- `partials/workers.html`: Worker 상태 조각
- `partials/error.html`: 에러 메시지 조각

### Q4. 포트를 변경할 수 있나요?

**A:** 예. uvicorn 실행 시 `port` 인자를 변경하거나, CLI에서 `--port` 옵션을 사용합니다 (TSK-01-03에서 구현 예정).

---

## 5. 문제 해결

### 문제 1: "TemplateNotFound" 에러

**증상:**
```
jinja2.exceptions.TemplateNotFound: index.html
```

**원인:** 템플릿 디렉토리가 없거나 템플릿 파일이 누락됨

**해결:**
1. `orchay/src/orchay/web/templates/` 디렉토리 존재 확인
2. 필요한 템플릿 파일 확인:
   - `index.html`
   - `partials/tree.html`
   - `partials/detail.html`
   - `partials/workers.html`
   - `partials/error.html`

### 문제 2: "ModuleNotFoundError: No module named 'fastapi'"

**증상:**
```
ModuleNotFoundError: No module named 'fastapi'
```

**원인:** 의존성 미설치

**해결:**
```bash
cd orchay
uv pip install fastapi uvicorn[standard] jinja2
# 또는
uv pip install -e ".[dev]"
```

### 문제 3: Task 상세 조회 시 404 에러

**증상:**
```
Task 'TSK-XX-XX'를 찾을 수 없습니다
```

**원인:** 해당 Task ID가 Orchestrator.tasks에 없음

**해결:**
1. WBS 파일에 해당 Task가 정의되어 있는지 확인
2. Task ID 형식이 올바른지 확인 (`TSK-XX-XX` 또는 `TSK-XX-XX-XX`)
3. Orchestrator가 WBS를 정상적으로 파싱했는지 확인

---

## 6. 참고 자료

### 6.1 관련 문서

| 문서 | 경로 | 설명 |
|------|------|------|
| 설계 문서 | `010-design.md` | 상세 설계 및 유즈케이스 |
| 추적성 매트릭스 | `025-traceability-matrix.md` | 요구사항 추적 |
| 테스트 명세 | `026-test-specification.md` | 테스트 케이스 |
| 구현 보고서 | `030-implementation.md` | 구현 결과 및 커버리지 |

### 6.2 외부 참조

| 리소스 | URL | 설명 |
|--------|-----|------|
| FastAPI 공식 문서 | https://fastapi.tiangolo.com | FastAPI 프레임워크 |
| Jinja2 문서 | https://jinja.palletsprojects.com | 템플릿 엔진 |
| HTMX 문서 | https://htmx.org | HTML 확장 |

### 6.3 코드 구조

```
orchay/src/orchay/web/
├── __init__.py          # 모듈 초기화, create_app 내보내기
├── server.py            # FastAPI 앱, 라우트 정의
├── templates/           # Jinja2 템플릿
│   ├── index.html       # 메인 페이지
│   └── partials/        # HTML 조각
│       ├── tree.html    # WBS 트리
│       ├── detail.html  # Task 상세
│       ├── workers.html # Worker 상태
│       └── error.html   # 에러 메시지
└── static/              # 정적 파일
    └── .gitkeep
```

---

## 변경 이력

| 버전 | 날짜 | 작성자 | 변경 내용 |
|------|------|--------|----------|
| 1.0 | 2025-12-28 | Claude | 최초 작성 |
