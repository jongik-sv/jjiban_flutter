# 사용자 매뉴얼 - orchay_web 통합 테스트

## 0. 문서 메타데이터

* **문서명**: `080-manual.md`
* **Task ID**: TSK-04-02
* **Task 명**: 통합 테스트
* **작성일**: 2025-12-28
* **작성자**: Claude AI Agent
* **버전**: 1.0.0

---

## 1. 개요

### 1.1 기능 소개
orchay_web 통합 테스트는 웹 모니터링 UI의 품질을 자동으로 검증하는 테스트 스위트입니다. 웹서버 라이프사이클, API 엔드포인트, HTMX 인터랙션, 성능을 포괄적으로 테스트합니다.

### 1.2 대상 사용자
- **개발자**: 코드 변경 후 회귀 테스트 수행
- **CI/CD 시스템**: 자동화된 품질 게이트
- **QA 엔지니어**: 기능 검증 수행

---

## 2. 시작하기

### 2.1 사전 요구사항
- Python 3.10 이상
- uv 패키지 매니저
- orchay 프로젝트 설치

### 2.2 의존성 설치
```bash
cd orchay
uv pip install -e ".[dev]"
```

### 2.3 테스트 위치
```
orchay/tests/test_web_server.py
```

---

## 3. 사용 방법

### 3.1 전체 테스트 실행
```bash
cd orchay
uv run pytest tests/test_web_server.py -v
```

### 3.2 특정 테스트 실행
```bash
# 서버 라이프사이클 테스트만
uv run pytest tests/test_web_server.py -k "server" -v

# API 엔드포인트 테스트만
uv run pytest tests/test_web_server.py -k "api" -v

# HTMX 테스트만
uv run pytest tests/test_web_server.py -k "htmx" -v

# 성능 테스트만
uv run pytest tests/test_web_server.py -k "time" -v
```

### 3.3 커버리지 포함 실행
```bash
uv run pytest tests/test_web_server.py --cov=src/orchay/web -v
```

### 3.4 빠른 실행 (출력 최소화)
```bash
uv run pytest tests/test_web_server.py -q
```

---

## 4. 테스트 케이스 상세

### 4.1 테스트 카테고리

| 카테고리 | 테스트 수 | 설명 |
|---------|----------|------|
| 서버 라이프사이클 | 4 | 시작, 종료, 앱 생성 |
| API 엔드포인트 | 12 | /, /api/tree, /api/detail, /api/workers |
| HTMX 인터랙션 | 16 | 자동 갱신, 토글, 에러 처리 |
| Worker 상태 | 10 | 아이콘, 색상, Task 표시 |
| 진행률 | 5 | 계산, 표시 |
| 성능 | 6 | 응답 시간 < 1초 |

### 4.2 주요 테스트 케이스

| 테스트 함수 | 검증 내용 |
|------------|----------|
| `test_create_app` | FastAPI 앱 정상 생성 |
| `test_index_page` | 메인 페이지 200 응답 |
| `test_tree_api` | WBS 트리 API 정상 응답 |
| `test_detail_api` | Task 상세 API 정상 응답 |
| `test_workers_api` | Worker 상태 API 정상 응답 |
| `test_page_load_time` | 페이지 로드 < 1초 |
| `test_htmx_auto_refresh_attributes` | HTMX 속성 검증 |

---

## 5. FAQ

### Q: 테스트 실패 시 어떻게 하나요?
A: 먼저 `uv run pytest tests/test_web_server.py -v --tb=long`으로 상세 오류를 확인하세요.

### Q: 테스트 속도가 느린 경우?
A: `pytest-xdist`로 병렬 실행: `uv run pytest tests/test_web_server.py -n auto`

### Q: 특정 테스트만 디버깅하려면?
A: `uv run pytest tests/test_web_server.py::test_함수명 -v --tb=short`

---

## 6. 문제 해결

### 6.1 일반적인 오류

| 오류 | 원인 | 해결책 |
|-----|------|--------|
| `ModuleNotFoundError` | 의존성 미설치 | `uv pip install -e ".[dev]"` |
| `ImportError: httpx` | httpx 미설치 | `uv pip install httpx` |
| `TestClient timeout` | 서버 응답 지연 | timeout 값 증가 |

### 6.2 테스트 격리 문제
테스트 간 상태 공유가 의심되면 `--forked` 옵션 사용:
```bash
uv run pytest tests/test_web_server.py --forked
```

---

## 7. 참고 자료

- [pytest 공식 문서](https://docs.pytest.org/)
- [FastAPI TestClient 가이드](https://fastapi.tiangolo.com/tutorial/testing/)
- [HTMX 테스팅 가이드](https://htmx.org/docs/#testing)

---

## 부록: 테스트 실행 결과 예시

```
============================= test session starts =============================
platform win32 -- Python 3.12.11, pytest-9.0.2
plugins: anyio-4.12.0, asyncio-1.3.0, cov-7.0.0

tests/test_web_server.py::test_create_app PASSED
tests/test_web_server.py::test_orchestrator_reference PASSED
tests/test_web_server.py::test_index_page PASSED
... (50 more tests)

============================= 53 passed in 0.70s ==============================
```

---

<!--
TSK-04-02: 통합 테스트 사용자 매뉴얼
Version: 1.0.0
-->
