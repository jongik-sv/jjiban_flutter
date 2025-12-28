# TSK-02-01 매뉴얼

## 1. 개요

### 1.1 기능 소개

WBS 트리 데이터 API는 orchay 웹 UI에서 Task 계층 구조를 시각화하기 위한 백엔드 API입니다.
Task 목록을 WP(Work Package) → ACT(Activity) → TSK(Task) 계층 구조로 변환하여 제공합니다.

### 1.2 대상 사용자

- orchay 웹 UI 사용자
- orchay 웹 개발자 (API 연동)

---

## 2. 시작하기

### 2.1 사전 요구사항

- Python >= 3.10
- uv (권장) 또는 pip
- orchay 프로젝트 설치

### 2.2 설치

```bash
cd orchay
uv pip install -e ".[dev]"
```

### 2.3 서버 실행

```bash
# 웹서버만 실행
python -m orchay orchay --web-only

# TUI + 웹서버 동시 실행
python -m orchay orchay --web

# 포트 지정
python -m orchay orchay --web --port 8080
```

---

## 3. 사용 방법

### 3.1 기본 사용법

브라우저에서 `http://localhost:8080` 접속 시 좌측에 WBS 트리가 표시됩니다.

### 3.2 API 엔드포인트

| 엔드포인트 | 메서드 | 설명 | 응답 |
|-----------|--------|------|------|
| `/api/tree` | GET | 전체 트리 조회 | HTML (tree.html) |
| `/api/tree/{wp_id}` | GET | WP 하위 노드 조회 | HTML (wp_children.html) |

### 3.3 트리 구조

```
WP-01 (진행률 50%)
├── ACT-01-01 (진행률 100%)
│   ├── TSK-01-01 [xx] 완료
│   └── TSK-01-02 [xx] 완료
└── ACT-01-02 (진행률 0%)
    └── TSK-01-03 [ ] 대기
```

### 3.4 상세 기능

#### 진행률 계산

- 각 노드(WP, ACT)의 진행률은 하위 Task 완료 비율로 계산
- 완료 상태: `[xx]`
- 진행률 = (완료 Task 수 / 전체 Task 수) × 100

#### HTMX 연동

트리는 HTMX를 통해 5초마다 자동 갱신됩니다:
```html
<div hx-get="/api/tree" hx-trigger="every 5s" hx-swap="innerHTML">
```

---

## 4. FAQ

### Q1. 트리가 표시되지 않습니다

A: Orchestrator에 WBS 파일이 올바르게 로드되었는지 확인하세요.
```bash
python -m orchay orchay --dry-run
```

### Q2. 진행률이 0%로 표시됩니다

A: Task가 없거나 모든 Task가 미완료 상태입니다. WBS 파일의 Task 상태를 확인하세요.

### Q3. 특정 WP가 404로 응답합니다

A: 요청한 WP ID가 WBS에 존재하지 않습니다. `/api/tree`로 전체 트리를 확인하세요.

---

## 5. 문제 해결

| 증상 | 원인 | 해결 방법 |
|------|------|----------|
| 404 Not Found | WP ID 오류 | `/api/tree`로 전체 조회 후 확인 |
| 500 Internal Server Error | Orchestrator 초기화 실패 | 로그 확인, WBS 파일 경로 검증 |
| 빈 트리 | Task 없음 | WBS 파일에 Task 추가 |
| 갱신 안됨 | HTMX 미로드 | CDN 연결 확인 |

---

## 6. 참고 자료

- [설계 문서](./010-design.md)
- [추적성 매트릭스](./025-traceability-matrix.md)
- [테스트 명세](./026-test-specification.md)
- [구현 보고서](./030-implementation.md)

### 관련 파일

| 파일 | 경로 |
|------|------|
| 트리 변환 모듈 | `orchay/src/orchay/web/tree.py` |
| 서버 라우트 | `orchay/src/orchay/web/server.py` |
| 트리 템플릿 | `orchay/src/orchay/web/templates/partials/tree.html` |
| WP 하위 템플릿 | `orchay/src/orchay/web/templates/partials/wp_children.html` |

---

## 변경 이력

| 버전 | 일자 | 변경 내용 |
|------|------|----------|
| 1.0 | 2025-12-28 | 최초 작성 |
