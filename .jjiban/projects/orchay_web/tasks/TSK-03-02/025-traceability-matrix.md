# TSK-03-02 - 요구사항 추적 매트릭스

## 문서 정보

| 항목 | 내용 |
|------|------|
| Task ID | TSK-03-02 |
| 문서 버전 | 1.0 |
| 작성일 | 2025-12-28 |
| 설계 문서 | `010-design.md` |

---

## 1. PRD → 설계 추적

### 1.1 PRD 요구사항 매핑

| PRD 섹션 | 요구사항 | 설계 섹션 | 구현 항목 |
|----------|----------|----------|----------|
| 3.3 Worker 상태 표시 | 상태별 아이콘 표시 | 5.2 화면별 상세 | status_icon 필터 |
| 3.3 Worker 상태 표시 | 상태별 색상 표시 | 5.2 화면별 상세 | status_bg 필터 |
| 3.3 Worker 상태 표시 | 현재 작업 중인 Task 표시 | 11.4 템플릿 구조 | current_task 표시 |
| 2.3 실시간 갱신 | 5초마다 자동 갱신 | 6.3 HTMX 자동 갱신 | hx-trigger="every 5s" |

### 1.2 TRD 기술 요구사항 매핑

| TRD 섹션 | 기술 요구사항 | 설계 섹션 | 구현 방법 |
|----------|-------------|----------|----------|
| API 설계 | GET /api/workers | 11.3 API 엔드포인트 | FastAPI 라우트 |
| HTMX 패턴 | hx-trigger, hx-swap | 6.3 HTMX 자동 갱신 | innerHTML 교체 |
| UI 스타일링 | Tailwind + 다크테마 | 5.2 상태별 표시 | bg-*-500/20 클래스 |

---

## 2. 설계 → 테스트 추적

### 2.1 유즈케이스 → 테스트 케이스

| 유즈케이스 | 테스트 케이스 ID | 테스트 유형 | 테스트 명세 참조 |
|-----------|----------------|------------|----------------|
| UC-01: Worker 상태 조회 | TC-01-01 | API 테스트 | 026-test-specification.md |
| UC-01: Worker 상태 조회 | TC-01-02 | 렌더링 테스트 | 026-test-specification.md |
| UC-02: 실시간 상태 갱신 | TC-02-01 | E2E 테스트 | 026-test-specification.md |

### 2.2 비즈니스 규칙 → 테스트 케이스

| 규칙 ID | 규칙 설명 | 테스트 케이스 ID | 검증 방법 |
|---------|----------|----------------|----------|
| BR-01 | busy 상태 Worker는 current_task 표시 필수 | TC-03-01 | 템플릿 검증 |
| BR-02 | error 상태는 빨간색 강조 | TC-03-02 | CSS 클래스 검증 |
| BR-03 | 5초마다 자동 갱신 | TC-02-01 | HTMX 속성 검증 |

---

## 3. 구현 컴포넌트 매핑

### 3.1 파일 → 요구사항

| 파일 | 구현 내용 | 관련 요구사항 |
|------|----------|--------------|
| `orchay/web/server.py` | `/api/workers` 라우트 | PRD 3.3, TRD API 설계 |
| `orchay/web/templates/partials/workers.html` | Worker 상태 바 템플릿 | PRD 3.3, TRD UI 스타일링 |
| `orchay/web/templates/index.html` | 상태 바 영역 배치 | PRD 2.1 레이아웃 |

### 3.2 Jinja2 필터 매핑

| 필터 함수 | 입력 | 출력 | 관련 요구사항 |
|----------|------|------|--------------|
| `status_icon` | WorkerState | 이모지 문자열 | PRD 3.3 상태 아이콘 |
| `status_bg` | WorkerState | Tailwind 클래스 | PRD 3.3 상태 색상 |

---

## 4. 상태 아이콘/색상 매핑

### 4.1 WorkerState → 표시 요소

| WorkerState | 아이콘 | 배경색 (Tailwind) | PRD 정의 색상 |
|-------------|--------|------------------|--------------|
| IDLE | 🟢 | bg-green-500/20 | #22c55e |
| BUSY | 🟡 | bg-yellow-500/20 | #f59e0b |
| PAUSED | ⏸️ | bg-purple-500/20 | #8b5cf6 |
| ERROR | 🔴 | bg-red-500/20 | #ef4444 |
| BLOCKED | ⊘ | bg-gray-500/20 | #6b7280 |
| DEAD | 💀 | bg-gray-700/20 | - |
| DONE | ✅ | bg-emerald-500/20 | - |

---

## 5. 의존성 추적

### 5.1 Task 의존성

| 의존 Task | 의존 내용 | 필요 산출물 | 상태 |
|----------|----------|------------|------|
| TSK-01-02 | Jinja2 템플릿 기본 구조 | base.html, index.html | [dd] |

### 5.2 데이터 의존성

| 데이터 소스 | 데이터 | 인터페이스 | 상태 |
|------------|--------|----------|------|
| Orchestrator | workers 리스트 | orchestrator.workers | 완료 |
| Worker 모델 | id, state, current_task | Worker 클래스 | 완료 |
| WorkerState | 상태 enum | models/worker.py | 완료 |

---

## 변경 이력

| 버전 | 일자 | 작성자 | 변경 내용 |
|------|------|--------|----------|
| 1.0 | 2025-12-28 | Claude | 최초 작성 |
