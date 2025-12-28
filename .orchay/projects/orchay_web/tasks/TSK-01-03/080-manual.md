# CLI 옵션 및 서버 통합 매뉴얼

## 1. 개요

### 1.1 기능 소개
orchay의 CLI 옵션을 확장하여 웹 모니터링 UI를 TUI와 함께 또는 단독으로 실행할 수 있는 기능입니다.

- **`--web`**: TUI/스케줄러와 웹서버를 동시에 실행
- **`--web-only`**: 웹서버만 단독 실행 (스케줄링 비활성화)
- **`--port`**: 웹서버 포트 지정 (기본값: 8080)

### 1.2 대상 사용자
- orchay를 사용하여 WBS 기반 Task 스케줄링을 수행하는 개발자
- 웹 브라우저를 통해 Task 진행 상황을 모니터링하고자 하는 팀원

---

## 2. 시작하기

### 2.1 사전 요구사항
- Python 3.10 이상
- orchay 패키지 설치 (`uv pip install -e ".[dev]"`)
- WezTerm (TUI 모드 사용 시)

### 2.2 설치 확인
```bash
# orchay 명령어 확인
orchay --help

# 웹 옵션 확인
orchay --help | grep -E "(--web|--port)"
```

---

## 3. 사용 방법

### 3.1 기본 사용법

#### 웹서버 포함 실행 (TUI + 웹)
```bash
orchay <project> --web
```
- TUI 화면과 웹서버가 동시에 실행됩니다.
- 웹 브라우저에서 `http://127.0.0.1:8080` 접속

#### 웹서버만 실행
```bash
orchay <project> --web-only
```
- WezTerm 터미널 없이 웹서버만 실행됩니다.
- 스케줄링은 비활성화되고 모니터링만 가능

#### 포트 지정
```bash
orchay <project> --web --port 3000
orchay <project> --web-only --port 9000
```
- 포트 범위: 1-65535

### 3.2 상세 기능

#### 3.2.1 옵션 상호 배타성
`--web`과 `--web-only`는 동시에 사용할 수 없습니다.

```bash
# 오류 발생
orchay orchay --web --web-only
# error: argument --web-only: not allowed with argument --web
```

#### 3.2.2 포트 검증
유효하지 않은 포트 입력 시 오류 메시지가 표시됩니다.

```bash
# 범위 초과
orchay orchay --web --port 70000
# error: Port must be between 1 and 65535

# 숫자 아님
orchay orchay --web --port abc
# error: invalid _validate_port value: 'abc'
```

#### 3.2.3 보안 설정
- 웹서버는 기본적으로 `127.0.0.1` (localhost)에만 바인딩됩니다.
- 외부 접근을 허용하려면 코드 수정이 필요합니다.

### 3.3 조합 예시

| 명령어 | 동작 |
|--------|------|
| `orchay orchay` | 기존 TUI 모드 |
| `orchay orchay --web` | TUI + 웹서버 (포트 8080) |
| `orchay orchay --web --port 3000` | TUI + 웹서버 (포트 3000) |
| `orchay orchay --web-only` | 웹서버만 (포트 8080) |
| `orchay orchay --web-only --port 9000` | 웹서버만 (포트 9000) |
| `orchay orchay --dry-run --web` | 드라이런 + 웹서버 |

---

## 4. FAQ

### Q1: 웹서버만 실행하면 스케줄링이 되지 않나요?
A: 네, `--web-only` 모드에서는 스케줄링이 비활성화됩니다. Task 상태 모니터링만 가능하며, 실제 Task 디스패치는 TUI 모드나 `--web` 모드에서만 동작합니다.

### Q2: 외부 네트워크에서 접근하려면 어떻게 하나요?
A: 현재 보안상 localhost만 바인딩됩니다. 외부 접근이 필요한 경우 `WebConfig.host` 값을 `0.0.0.0`으로 변경하거나, 리버스 프록시를 사용하세요.

### Q3: 포트가 이미 사용 중이면 어떻게 되나요?
A: uvicorn이 "Address already in use" 오류를 출력합니다. `--port` 옵션으로 다른 포트를 지정하세요.

### Q4: 여러 프로젝트를 동시에 모니터링할 수 있나요?
A: 현재는 단일 프로젝트만 지원합니다. 여러 프로젝트를 모니터링하려면 각각 다른 포트로 별도 인스턴스를 실행하세요.

---

## 5. 문제 해결

### 오류: Port must be between 1 and 65535
**원인**: 유효하지 않은 포트 번호 입력
**해결**: 1-65535 범위의 정수를 입력하세요.

### 오류: Address already in use
**원인**: 지정한 포트가 다른 프로세스에서 사용 중
**해결**:
1. 다른 포트 사용: `--port 9000`
2. 사용 중인 프로세스 확인: `netstat -an | grep 8080`

### 오류: argument --web-only: not allowed with argument --web
**원인**: `--web`과 `--web-only` 동시 사용
**해결**: 둘 중 하나만 선택하세요.

### 웹페이지가 로드되지 않음
**원인**:
1. 서버가 실행되지 않았거나 오류 발생
2. 방화벽 차단

**해결**:
1. 터미널에서 서버 로그 확인
2. `curl http://127.0.0.1:8080` 으로 연결 테스트
3. 방화벽 설정 확인

---

## 6. 참고 자료

### 관련 문서
- [010-design.md](./010-design.md) - 통합설계 문서
- [025-traceability-matrix.md](./025-traceability-matrix.md) - 추적성 매트릭스
- [026-test-specification.md](./026-test-specification.md) - 테스트 명세
- [030-implementation.md](./030-implementation.md) - 구현 보고서

### 관련 Task
- TSK-01-01: FastAPI 앱 및 라우트 정의
- TSK-01-02: Jinja2 템플릿 기본 구조

### 소스 코드
- `orchay/src/orchay/main.py` - CLI 옵션 및 웹서버 통합
- `orchay/src/orchay/models/config.py` - WebConfig 데이터클래스

---

## 변경 이력

| 버전 | 날짜 | 작성자 | 변경 내용 |
|------|------|--------|----------|
| 1.0 | 2025-12-28 | Claude | 최초 작성 |
