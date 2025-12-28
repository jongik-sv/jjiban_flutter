# Worker 상태 바 사용 매뉴얼

## 문서 정보

| 항목 | 내용 |
|------|------|
| Task ID | TSK-03-02 |
| 기능명 | Worker 상태 바 |
| 문서 버전 | 1.0 |
| 작성일 | 2025-12-28 |

---

## 1. 개요

### 1.1 기능 소개

Worker 상태 바는 orchay 웹 모니터링 UI의 핵심 기능으로, 모든 Worker의 현재 상태를 한눈에 파악할 수 있도록 시각적으로 표시합니다.

**주요 특징**:
- 실시간 상태 모니터링 (5초마다 자동 갱신)
- 상태별 이모지 아이콘으로 직관적 표시
- 현재 작업 중인 Task ID 표시
- 다크 테마 UI 적용

### 1.2 대상 사용자

- orchay 스케줄러를 사용하는 개발자
- 프로젝트 진행 상황을 모니터링하는 관리자
- 다중 Worker 환경에서 작업 분배 상태를 확인하려는 사용자

---

## 2. 시작하기

### 2.1 사전 요구사항

- orchay 스케줄러 설치 완료
- Python 3.12 이상
- WezTerm 터미널 환경 (Worker 패널 생성 필요)

### 2.2 접근 방법

**웹서버 시작**:
```bash
# 프로젝트 루트에서 실행
cd orchay
uv run python -m orchay --web <project-name>
# 또는 웹서버만 실행
uv run python -m orchay --web-only <project-name> --port 8080
```

**브라우저 접속**:
```
http://localhost:8080
```

페이지 상단 헤더 영역에 Worker 상태 바가 표시됩니다.

---

## 3. 사용 방법

### 3.1 기본 사용법

Worker 상태 바는 페이지 로드 시 자동으로 표시되며, 5초마다 최신 상태로 갱신됩니다.

**화면 구성**:
```
┌─────────────────────────────────────────────────────────────────┐
│  Workers:  🟢 W1       🟡 W2 (TSK-01-01)    🔴 W3 (error)       │
│           idle        busy                  error               │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 상태 아이콘 및 색상

| 상태 | 아이콘 | 배경색 | 설명 |
|------|--------|--------|------|
| idle | 🟢 | 초록 | 대기 중, 작업 가능 |
| busy | 🟡 | 노랑 | 작업 처리 중 |
| paused | ⏸️ | 보라 | 일시 정지 (rate limit 등) |
| error | 🔴 | 빨강 | 오류 발생, 주의 필요 |
| blocked | ⊘ | 회색 | 입력 대기 중 (y/n 등) |
| dead | 💀 | 진회색 | 패널 종료됨 |
| done | ✅ | 에메랄드 | 작업 완료 |

### 3.3 상세 기능

#### 3.3.1 현재 작업 Task 표시

Worker가 `busy` 상태일 때, 현재 처리 중인 Task ID가 괄호 안에 표시됩니다.

**예시**:
- `🟡 W2 (TSK-01-01)` - Worker 2가 TSK-01-01을 처리 중

#### 3.3.2 자동 갱신

- 페이지 로드 시 즉시 상태 표시
- 이후 5초마다 자동으로 최신 상태 갱신
- 네트워크 오류 시 마지막 상태 유지

#### 3.3.3 에러 상태 강조

에러 상태의 Worker는 빨간색 배경으로 강조되어 즉시 주의를 끌 수 있습니다.

---

## 4. FAQ

### Q1: Worker 상태가 갱신되지 않습니다

**A**: 다음을 확인하세요:
1. 브라우저 개발자 도구에서 네트워크 탭 확인 (5초마다 `/api/workers` 요청)
2. 서버가 정상 실행 중인지 확인
3. 페이지 새로고침 시도

### Q2: "No workers available" 메시지가 표시됩니다

**A**: Orchestrator가 초기화되었으나 Worker 패널이 감지되지 않은 상태입니다:
1. WezTerm에서 Worker 패널이 생성되었는지 확인
2. orchay 스케줄러가 정상 실행 중인지 확인

### Q3: Worker 상태가 계속 "busy"로 표시됩니다

**A**: Task 처리가 진행 중이거나, Worker 상태 감지에 문제가 있을 수 있습니다:
1. 해당 Worker 패널에서 실제 작업 진행 상태 확인
2. 터미널 출력에 완료 패턴 (`ORCHAY_DONE:...`) 확인

---

## 5. 문제 해결

### 5.1 화면에 Worker가 표시되지 않음

**원인**: Orchestrator가 Worker 목록을 가져오지 못함

**해결 방법**:
1. orchay 스케줄러 재시작
2. WezTerm 패널 확인 및 재설정
3. 서버 로그 확인 (`/api/workers` 응답)

### 5.2 상태 아이콘이 올바르지 않음

**원인**: 상태 감지 패턴 불일치

**해결 방법**:
1. `orchay/src/orchay/worker.py`의 상태 패턴 확인
2. Worker 패널의 실제 출력과 비교

### 5.3 자동 갱신이 동작하지 않음

**원인**: HTMX 스크립트 로드 실패

**해결 방법**:
1. 브라우저 콘솔에서 HTMX 오류 확인
2. CDN 연결 상태 확인
3. 페이지 새로고침

---

## 6. 참고 자료

### 6.1 관련 문서

| 문서 | 경로 |
|------|------|
| 설계 문서 | `.jjiban/projects/orchay_web/tasks/TSK-03-02/010-design.md` |
| 추적 매트릭스 | `.jjiban/projects/orchay_web/tasks/TSK-03-02/025-traceability-matrix.md` |
| 테스트 명세 | `.jjiban/projects/orchay_web/tasks/TSK-03-02/026-test-specification.md` |
| 구현 보고서 | `.jjiban/projects/orchay_web/tasks/TSK-03-02/030-implementation.md` |

### 6.2 API 엔드포인트

| Method | Endpoint | 설명 |
|--------|----------|------|
| GET | `/api/workers` | Worker 상태 HTML 파셜 반환 |

### 6.3 구현 파일

| 파일 | 설명 |
|------|------|
| `orchay/src/orchay/web/filters.py` | Jinja2 필터 (status_icon, status_bg) |
| `orchay/src/orchay/web/templates/partials/workers.html` | Worker 상태 바 템플릿 |
| `orchay/src/orchay/web/server.py` | API 라우트 정의 |

---

## 변경 이력

| 버전 | 일자 | 작성자 | 변경 내용 |
|------|------|--------|----------|
| 1.0 | 2025-12-28 | Claude | 최초 작성 |
