# TSK-01-03 테스트 명세서

## 문서 정보

| 항목 | 내용 |
|------|------|
| Task ID | TSK-01-03 |
| 문서 버전 | 1.0 |
| 작성일 | 2025-12-28 |

---

## 1. 단위 테스트

### TC-01: --web 옵션 파싱

| 항목 | 내용 |
|------|------|
| 테스트 ID | TC-01 |
| 목적 | --web 옵션이 정상 파싱되는지 확인 |
| 사전 조건 | CLI 모듈 로드됨 |
| 입력 | `["jjiban", "--web"]` |
| 예상 결과 | `args.web == True`, `args.web_only == False` |
| 우선순위 | 높음 |

```python
def test_web_option_parsing():
    args = parse_args(["jjiban", "--web"])
    assert args.web is True
    assert args.web_only is False
    assert args.port == 8080
```

### TC-02: --web-only 옵션 파싱

| 항목 | 내용 |
|------|------|
| 테스트 ID | TC-02 |
| 목적 | --web-only 옵션이 정상 파싱되는지 확인 |
| 입력 | `["jjiban", "--web-only"]` |
| 예상 결과 | `args.web_only == True`, `args.web == False` |
| 우선순위 | 높음 |

```python
def test_web_only_option_parsing():
    args = parse_args(["jjiban", "--web-only"])
    assert args.web_only is True
    assert args.web is False
```

### TC-03: --port 옵션 파싱

| 항목 | 내용 |
|------|------|
| 테스트 ID | TC-03 |
| 목적 | --port 옵션이 정상 파싱되는지 확인 |
| 입력 | `["jjiban", "--web", "--port", "3000"]` |
| 예상 결과 | `args.port == 3000` |
| 우선순위 | 중간 |

```python
def test_port_option_parsing():
    args = parse_args(["jjiban", "--web", "--port", "3000"])
    assert args.port == 3000
```

### TC-04: 옵션 충돌 테스트

| 항목 | 내용 |
|------|------|
| 테스트 ID | TC-04 |
| 목적 | --web과 --web-only 동시 사용 시 에러 발생 확인 |
| 입력 | `["jjiban", "--web", "--web-only"]` |
| 예상 결과 | `SystemExit` 또는 에러 메시지 |
| 우선순위 | 높음 |

```python
def test_web_options_mutually_exclusive():
    with pytest.raises(SystemExit):
        parse_args(["jjiban", "--web", "--web-only"])
```

### TC-05: 무효 포트 테스트

| 항목 | 내용 |
|------|------|
| 테스트 ID | TC-05 |
| 목적 | 유효 범위 외 포트에서 에러 발생 확인 |
| 입력 | `["jjiban", "--web", "--port", "99999"]` |
| 예상 결과 | 에러 메시지 또는 `SystemExit` |
| 우선순위 | 중간 |

```python
def test_invalid_port():
    with pytest.raises(SystemExit):
        parse_args(["jjiban", "--web", "--port", "99999"])
```

---

## 2. 통합 테스트

### TC-06: 웹서버 시작 테스트

| 항목 | 내용 |
|------|------|
| 테스트 ID | TC-06 |
| 목적 | --web 옵션으로 웹서버가 실제로 시작되는지 확인 |
| 사전 조건 | FastAPI, uvicorn 설치됨 |
| 절차 | 1. --web 옵션으로 실행<br>2. localhost:8080 요청<br>3. 응답 확인 |
| 예상 결과 | HTTP 200 응답 |
| 우선순위 | 높음 |

```python
@pytest.mark.asyncio
async def test_web_server_starts():
    async with start_orchay_with_web() as server:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://127.0.0.1:8080/")
            assert response.status_code == 200
```

### TC-07: 병렬 실행 테스트

| 항목 | 내용 |
|------|------|
| 테스트 ID | TC-07 |
| 목적 | Orchestrator와 웹서버가 동시에 동작하는지 확인 |
| 절차 | 1. --web 옵션으로 실행<br>2. Orchestrator 동작 확인<br>3. 웹서버 응답 확인 |
| 예상 결과 | 둘 다 정상 동작 |
| 우선순위 | 높음 |

---

## 3. E2E 테스트

### TC-08: 전체 워크플로우

| 항목 | 내용 |
|------|------|
| 테스트 ID | TC-08 |
| 목적 | CLI에서 웹서버까지 전체 흐름 확인 |
| 절차 | 1. `orchay jjiban --web` 실행<br>2. 브라우저에서 localhost:8080 접속<br>3. WBS 트리 표시 확인<br>4. Ctrl+C로 종료 |
| 예상 결과 | 모든 단계 정상 동작 |
| 우선순위 | 높음 |

---

## 4. 테스트 환경

| 항목 | 요구사항 |
|------|----------|
| Python | >= 3.10 |
| 테스트 프레임워크 | pytest, pytest-asyncio |
| HTTP 클라이언트 | httpx |
| 포트 | 8080 (기본), 3000 (대안) |

---

## 변경 이력

| 버전 | 일자 | 변경 내용 |
|------|------|-----------|
| 1.0 | 2025-12-28 | 최초 작성 |
