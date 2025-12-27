# orchay

> **orch**estration + ok**ay** - WezTerm 기반 Task 스케줄러

wbs.md를 모니터링하여 실행 가능한 Task를 추출하고, 여러 Claude Code Worker pane에 작업을 자동 분배합니다.

## 설치

### 요구사항

- Python >= 3.10
- WezTerm 터미널 (PATH에 `wezterm` 명령어 등록 필요)
- uv (권장) 또는 pip

### 설치 방법

```bash
cd orchay

# uv 사용 (권장)
uv venv
uv pip install -e ".[dev]"

# 또는 pip 사용
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac
pip install -e ".[dev]"
```

## 실행

```bash
# uv 사용 (권장)
cd orchay
uv run python -m orchay [WBS_PATH] [OPTIONS]

# 또는 venv 활성화 후
.venv\Scripts\activate      # Windows
# source .venv/bin/activate  # Linux/Mac
python -m orchay [WBS_PATH] [OPTIONS]
```

### CLI 옵션

```
usage: orchay [-h] [-w WORKERS] [-i INTERVAL]
              [-m {design,quick,develop,force}] [--dry-run] [-v]
              [wbs]

positional arguments:
  wbs                   WBS 파일 경로 (기본: .jjiban/projects/orchay/wbs.md)

options:
  -w, --workers N       Worker 수 (기본: 3)
  -i, --interval SEC    모니터링 간격 초 (기본: 5)
  -m, --mode MODE       실행 모드: design, quick, develop, force (기본: quick)
  --dry-run             분배 없이 상태만 표시
  -v, --verbose         상세 로그 출력
```

### 사용 예시

```bash
# 기본 실행 (quick 모드, 3 workers)
uv run python -m orchay .jjiban/projects/myproject/wbs.md

# develop 모드로 실행
uv run python -m orchay wbs.md -m develop

# 5개 Worker로 실행
uv run python -m orchay wbs.md -w 5

# 상태만 확인 (분배 없음)
uv run python -m orchay wbs.md --dry-run

# 모니터링 간격 10초
uv run python -m orchay wbs.md -i 10
```

### 실행 화면

```
orchay - Task Scheduler v0.1.0

WBS: C:\project\wbs.md
Mode: quick
Workers: 3개
Tasks: 9개

스케줄러 시작 (Ctrl+C로 종료)

                    Worker Status
┌──────┬────────┬────────────┬──────────────────────┐
│ ID   │ Pane   │ State      │ Task                 │
├──────┼────────┼────────────┼──────────────────────┤
│ 1    │ 0      │ busy       │ TSK-02-01            │
│ 2    │ 2      │ idle       │ -                    │
│ 3    │ 1      │ idle       │ -                    │
└──────┴────────┴────────────┴──────────────────────┘

Queue: 5 pending, 1 running, 3 done
```

## 아키텍처

```
orchay/
├── src/orchay/
│   ├── main.py          # 진입점
│   ├── scheduler.py     # 스케줄러 코어 (Task 필터링, 분배 로직)
│   ├── wbs_parser.py    # WBS 파일 파싱 및 감시
│   ├── worker.py        # Worker 상태 감지
│   ├── models/
│   │   ├── task.py      # Task 모델
│   │   ├── worker.py    # Worker 모델
│   │   └── config.py    # 설정 모델
│   └── utils/
│       └── wezterm.py   # WezTerm CLI 래퍼
└── tests/               # 테스트 코드
```

## 핵심 기능

### 1. WBS 파싱 (`wbs_parser.py`)

wbs.md 파일을 파싱하여 Task 객체 리스트로 변환합니다.

```python
from orchay.wbs_parser import parse_wbs, watch_wbs

# 단일 파싱
tasks = await parse_wbs(".jjiban/projects/orchay/wbs.md")
for task in tasks:
    print(f"{task.id}: {task.status}")

# 파일 변경 감시
async def on_change(tasks):
    print(f"Tasks updated: {len(tasks)}")

watcher = watch_wbs("wbs.md", on_change, debounce=0.5)
watcher.start()
# ... 작업 ...
await watcher.stop()
```

**WBS 파일 형식:**

```markdown
### TSK-01-01: Task 제목
- category: development
- domain: backend
- status: todo [ ]
- priority: high
- assignee: -
- schedule:
- tags: api, auth
- depends: TSK-01-00
- blocked-by: -
```

### 2. Task 모델 (`models/task.py`)

| 필드 | 타입 | 설명 |
|------|------|------|
| id | string | Task ID (예: TSK-01-01) |
| title | string | Task 제목 |
| category | enum | development, defect, infrastructure, simple-dev |
| domain | string | 기술 도메인 (backend, frontend 등) |
| status | enum | 현재 상태 (아래 표 참조) |
| priority | enum | critical, high, medium, low |
| depends | list | 의존 Task ID 목록 |
| blocked_by | string? | 블로킹 사유 |

**Task 상태 (status):**

| 코드 | 의미 | 설명 |
|------|------|------|
| `[ ]` | TODO | 미시작 |
| `[bd]` | BASIC_DESIGN | 기본 설계 |
| `[dd]` | DETAIL_DESIGN | 상세 설계 |
| `[an]` | ANALYSIS | 분석 |
| `[ds]` | DESIGN | 설계 완료 |
| `[ap]` | APPROVED | 승인됨 |
| `[im]` | IMPLEMENT | 구현됨 |
| `[fx]` | FIX | 수정 중 |
| `[vf]` | VERIFY | 검증 중 |
| `[xx]` | DONE | 완료 |

### 3. 실행 모드 (`scheduler.py`)

| 모드 | 워크플로우 단계 | 설명 |
|------|-----------------|------|
| **design** | start | 설계만 수행 |
| **quick** | start → approve → build → done | 빠른 구현 |
| **develop** | start → review → apply → approve → build → audit → patch → test → done | 전체 워크플로우 |
| **force** | start → approve → build → done | 의존성 무시하고 강제 실행 |

**비즈니스 규칙:**

- BR-01: 완료 Task(`[xx]`)는 항상 제외
- BR-02: `blocked-by` 설정된 Task 제외
- BR-03: 실행 중 Task 중복 분배 금지
- BR-04: design 모드: `[ ]` 상태만 표시
- BR-05: develop/quick: 구현 단계에서 의존성 검사
- BR-06: force 모드: 의존성 무시
- BR-07: 우선순위 정렬: critical > high > medium > low

### 4. Worker 관리 (`worker.py`)

Worker pane의 출력을 분석하여 상태를 감지합니다.

**Worker 상태:**

| 상태 | 우선순위 | 설명 |
|------|----------|------|
| dead | 1 | pane이 존재하지 않음 |
| done | 2 | ORCHAY_DONE 신호 수신 |
| paused | 3 | rate limit, capacity 등 |
| error | 4 | Error, Failed, Exception 등 |
| blocked | 5 | 사용자 입력 대기 중 |
| idle | 6 | 프롬프트 대기 상태 |
| busy | 7 | 작업 실행 중 |

**완료 신호 형식:**

```
ORCHAY_DONE:{task-id}:{action}:{status}[:{message}]

예:
ORCHAY_DONE:TSK-01-01:build:success
ORCHAY_DONE:TSK-01-02:test:error:테스트 실패
```

### 5. WezTerm 통합 (`utils/wezterm.py`)

WezTerm CLI를 통한 pane 관리 기능:

```python
from orchay.utils.wezterm import (
    wezterm_list_panes,
    wezterm_get_text,
    wezterm_send_text,
    pane_exists,
)

# pane 목록 조회
panes = await wezterm_list_panes()
for p in panes:
    print(f"Pane {p.pane_id}: {p.title} @ {p.cwd}")

# pane 출력 조회 (최근 50줄)
text = await wezterm_get_text(pane_id=1, lines=50)

# pane에 텍스트 전송
await wezterm_send_text(pane_id=1, text="/wf:build TSK-01-01\n")

# pane 존재 확인
if await pane_exists(pane_id=1):
    print("Pane 1 exists")
```

## 개발

### 테스트 실행

```bash
# 전체 테스트
pytest

# 특정 모듈 테스트
pytest tests/test_wbs_parser.py
pytest tests/test_scheduler.py
pytest tests/test_worker.py
pytest tests/test_wezterm.py

# 커버리지 포함
pytest --cov=orchay
```

### 린트 및 타입 검사

```bash
# Ruff 린터
ruff check src tests

# Ruff 포매터
ruff format src tests

# Pyright 타입 검사
pyright src tests
```

## 의존성

| 패키지 | 버전 | 용도 |
|--------|------|------|
| textual | >=1.0 | TUI 프레임워크 |
| rich | >=14.0 | 터미널 출력 포매팅 |
| watchdog | >=4.0 | 파일 변경 감시 |
| pydantic | >=2.0 | 데이터 모델 검증 |

### 개발 의존성

| 패키지 | 버전 | 용도 |
|--------|------|------|
| pytest | >=8.0 | 테스트 프레임워크 |
| pytest-asyncio | >=0.23 | 비동기 테스트 지원 |
| ruff | >=0.5 | 린터/포매터 |
| pyright | >=1.1 | 타입 검사 |

## 라이선스

MIT
