  | 라이브러리 | 플랫폼   | 설명                              |
  |------------|----------|-----------------------------------|
  | pexpect    | Unix/Mac | PTY 기반 프로세스 제어, 가장 유명 |
  | wexpect    | Windows  | pexpect의 Windows 포트            |
  | pywinpty   | Windows  | winpty Python 바인딩              |
  | pyte       | 모두     | 순수 Python 터미널 에뮬레이터     |
  | ptyprocess | Unix/Mac | pexpect 하위 라이브러리           |



파워쉘 업그레이드 https://dong-it-engineer.tistory.com/39
파워쉘 7버전에서 가능함
PS C:\bin\wezterm> ./wezterm.exe cli send-text --no-paste --pane-id 1 안녕
PS C:\bin\wezterm> ./wezterm.exe cli send-text --no-paste --pane-id 1 `r
