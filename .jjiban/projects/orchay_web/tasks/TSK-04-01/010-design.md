# TSK-04-01: 의존성 및 pyproject.toml 업데이트 - 기술 설계

## 1. 개요

### 1.1 목적
orchay 프로젝트에 웹 모니터링 UI 기능을 위한 Python 패키지 의존성을 추가합니다.

### 1.2 범위
- pyproject.toml에 웹서버 관련 의존성 추가
- 기존 의존성과의 호환성 유지

## 2. 현재 상태

### 2.1 현재 의존성
```toml
dependencies = [
    "textual>=1.0",
    "rich>=14.0",
    "watchdog>=4.0",
    "pydantic>=2.0",
]
```

### 2.2 현재 개발 의존성
```toml
dev = [
    "pytest>=8.0",
    "pytest-asyncio>=0.23",
    "ruff>=0.5",
    "pyright>=1.1",
]
```

## 3. 목표 상태

### 3.1 추가할 의존성

| 패키지 | 버전 | 용도 |
|--------|------|------|
| fastapi | >=0.115 | 웹 프레임워크 |
| uvicorn[standard] | - | ASGI 서버 |
| jinja2 | >=3.0 | 템플릿 엔진 |

### 3.2 변경 후 dependencies 섹션
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

## 4. 구현 계획

### 4.1 pyproject.toml 수정
1. dependencies 배열에 3개 패키지 추가
2. 버전 명시: TRD 스펙 기준

### 4.2 검증 방법
```bash
# 설치 확인
cd orchay
uv pip install -e .

# import 테스트
python -c "import fastapi; import uvicorn; import jinja2; print('OK')"
```

## 5. 의존성 분석

### 5.1 호환성 확인

| 패키지 | Python 요구사항 | 기존 의존성 충돌 |
|--------|-----------------|------------------|
| fastapi | >=3.8 | 없음 (pydantic 호환) |
| uvicorn | >=3.8 | 없음 |
| jinja2 | >=3.7 | 없음 |

### 5.2 주요 특성

- **fastapi**: pydantic 기반이므로 기존 pydantic>=2.0과 호환
- **uvicorn[standard]**: 비동기 서버로 asyncio와 자연스럽게 통합
- **jinja2**: 독립적 템플릿 엔진, 충돌 요소 없음

## 6. 수용 기준

- [ ] `uv pip install -e .` 또는 `pip install -e .` 성공
- [ ] 모든 의존성 정상 설치
- [ ] Python import 테스트 통과

---

| 항목 | 내용 |
|------|------|
| Task ID | TSK-04-01 |
| Category | infrastructure |
| 문서 버전 | 1.0 |
| 작성일 | 2025-12-28 |
