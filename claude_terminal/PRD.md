# Claude Terminal PRD

## 개요
Go 언어로 구현된 Claude CLI 터미널 래퍼 프로그램. ConPTY를 사용하여 Claude CLI와 상호작용하고 자동으로 프롬프트를 전송할 수 있음.

## 핵심 발견사항

### Enter 키 전송 방식
**중요**: Claude CLI에 명령어를 전송할 때 `\r\n`이 아닌 **`\r`만 사용해야 함**.

```go
// 올바른 방식
io.WriteString(cpty, prompt+"\r")

// 잘못된 방식 (작동 안 함)
io.WriteString(cpty, prompt+"\r\n")
```

### ConPTY 사용 시 Claude CLI 경로
Windows에서 ConPTY로 Claude CLI를 실행할 때 전체 경로를 사용해야 함:

```go
cpty, err := conpty.Start(`C:\Users\sviso\AppData\Roaming\npm\claude.cmd --dangerously-skip-permissions`)
```

### Welcome 메시지 감지
Claude CLI가 준비되면 "Welcome" 문자열이 출력됨. 이를 감지한 후 프롬프트를 전송해야 함.

```go
if strings.Contains(output, "Welcome") {
    // 10초 대기 후 프롬프트 전송
    time.Sleep(10 * time.Second)
    io.WriteString(cpty, prompt+"\r")
}
```

### 출력 읽기와 프롬프트 전송 병렬 처리
프롬프트 전송 시 `time.Sleep()`을 사용하면 출력 읽기가 블록됨. 별도 고루틴에서 처리해야 함:

```go
go func() {
    time.Sleep(10 * time.Second)
    io.WriteString(cpty, prompt+"\r")
}()
```

### 작업 완료 감지 (Hook 기반)
**중요**: Claude CLI의 `Stop` hook을 사용하여 작업 완료를 정확하게 감지할 수 있음.

#### 1. Hook 설정 (`.claude/settings.json`)
```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "echo ===CLAUDE_TASK_COMPLETE==="
          }
        ]
      }
    ]
  }
}
```

#### 2. Go 프로그램에서 마커 감지
```go
const COMPLETION_MARKER = "===CLAUDE_TASK_COMPLETE==="

// 출력 읽기 루프에서
if strings.Contains(output, COMPLETION_MARKER) {
    fmt.Println("[✅ Task completed detected via hook!]")
    // 완료 처리 로직
}
```

#### 장점
| 방법 | 신뢰성 | 복잡도 |
|------|--------|--------|
| Idle timeout | 낮음 | 낮음 |
| stream-json result 이벤트 | 중간 (버그 있음) | 높음 |
| **Stop hook** | **높음** | **낮음** |

## 의존성

- `github.com/UserExistsError/conpty` - Windows ConPTY 지원
- `github.com/creack/pty` - Unix PTY 지원 (Mac/Linux)

## 빌드 방법

```bash
cd claude_terminal
go mod tidy
go build -o claude_terminal.exe .
```

## 실행 방법

```bash
.\claude_terminal.exe
```

- 입력 후 Enter로 명령어 전송
- `/quit` 입력으로 종료
- `Ctrl+C`로 강제 종료

## 파일 구조

```
claude_terminal/
├── go.mod
├── main_windows.go  # Windows용 (ConPTY)
├── main_unix.go     # Mac/Linux용 (PTY)
└── PRD.md           # 이 문서
```
