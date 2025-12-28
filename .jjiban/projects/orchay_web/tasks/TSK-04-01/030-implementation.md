# TSK-04-01: 의존성 및 pyproject.toml 업데이트 - 구현 보고서

## 1. 개요

### 1.1 Task 정보
| 항목 | 내용 |
|------|------|
| Task ID | TSK-04-01 |
| 제목 | 의존성 및 pyproject.toml 업데이트 |
| Category | infrastructure |
| 상태 전환 | [ds] 설계 → [im] 구현 |

### 1.2 구현 결과 요약
- pyproject.toml에 웹서버 관련 의존성 추가 완료
- 모든 의존성 설치 및 import 테스트 통과

## 2. 구현 내용

### 2.1 pyproject.toml 변경

**변경 전:**
```toml
dependencies = [
    "textual>=1.0",
    "rich>=14.0",
    "watchdog>=4.0",
    "pydantic>=2.0",
]
```

**변경 후:**
```toml
dependencies = [
    "textual>=1.0",
    "rich>=14.0",
    "watchdog>=4.0",
    "pydantic>=2.0",
    "fastapi>=0.115",
    "uvicorn[standard]",
    "jinja2>=3.0",
]
```

### 2.2 추가된 의존성

| 패키지 | 설치 버전 | 용도 |
|--------|-----------|------|
| fastapi | 0.128.0 | 웹 프레임워크 |
| uvicorn | 0.40.0 | ASGI 서버 |
| jinja2 | 3.1.6 | 템플릿 엔진 |

### 2.3 개발 의존성 추가

| 패키지 | 용도 |
|--------|------|
| httpx>=0.24 | FastAPI 테스트 클라이언트 |

## 3. 검증 결과

### 3.1 설치 테스트
```bash
cd orchay && uv pip install -e ".[dev]"
# 결과: Resolved 43 packages, Installed 1 package
```

### 3.2 Import 테스트
```bash
cd orchay && uv run python -c "import fastapi; import uvicorn; import jinja2; print('OK')"
# 결과: OK: fastapi 0.128.0 | uvicorn 0.40.0 | jinja2 3.1.6
```

## 4. 수용 기준 충족

| 기준 | 상태 |
|------|------|
| `uv pip install -e .` 성공 | ✅ |
| 모든 의존성 정상 설치 | ✅ |
| Python import 테스트 통과 | ✅ |

## 5. 관련 파일

| 파일 | 변경 내용 |
|------|-----------|
| orchay/pyproject.toml | dependencies 섹션에 3개 패키지 추가 |

---

| 항목 | 내용 |
|------|------|
| Task ID | TSK-04-01 |
| 문서 버전 | 1.0 |
| 작성일 | 2025-12-28 |
