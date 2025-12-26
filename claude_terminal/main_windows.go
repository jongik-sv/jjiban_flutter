//go:build windows

package main

import (
	"bufio"
	"flag"
	"fmt"
	"io"
	"os"
	"regexp"
	"strings"
	"sync"
	"time"

	"github.com/UserExistsError/conpty"
)

// ANSI escape 코드 제거 (더 강력한 패턴)
var ansiRegex = regexp.MustCompile(`\x1B\[[0-9;]*[a-zA-Z]|\x1B\].*?\x07|\x1B[@-Z\\-_]`)

func stripAnsi(s string) string {
	// ANSI 코드 제거
	s = ansiRegex.ReplaceAllString(s, "")
	// 제어 문자 제거
	s = strings.ReplaceAll(s, "\r", "")
	return s
}

// 유용한 라인만 필터링
func isUsefulLine(line string) bool {
	line = strings.TrimSpace(line)
	if line == "" {
		return false
	}
	// UI 요소 필터링
	skipPatterns := []string{
		"───", "╭", "╮", "╰", "╯", "│",
		"bypass permissions", "ctrl+g", "alt+m",
		"⏵", "▐", "▛", "▜", "▝", "▘",
		"invalid settings", "/doctor",
	}
	for _, p := range skipPatterns {
		if strings.Contains(line, p) {
			return false
		}
	}
	return true
}

func main() {
	// 명령줄 인자
	promptPtr := flag.String("p", "", "Prompt to send")
	waitPtr := flag.Int("w", 3, "Wait seconds after Welcome")
	flag.Parse()

	prompt := *promptPtr
	waitTime := *waitPtr

	if prompt == "" {
		fmt.Println("[ERROR] No prompt provided. Use -p \"your prompt\"")
		os.Exit(1)
	}

	fmt.Println("[BRIDGE:START]")
	fmt.Printf("[BRIDGE:PROMPT:%s]\n", prompt)

	// Claude CLI 실행
	cpty, err := conpty.Start(`C:\Users\sviso\AppData\Roaming\npm\claude.cmd --dangerously-skip-permissions`)
	if err != nil {
		fmt.Printf("[ERROR] %v\n", err)
		os.Exit(1)
	}
	defer cpty.Close()

	var (
		promptSent bool
		running    = true
		mu         sync.Mutex
	)

	// stdin 입력 고루틴
	go func() {
		reader := bufio.NewReader(os.Stdin)
		for {
			mu.Lock()
			if !running {
				mu.Unlock()
				break
			}
			mu.Unlock()

			input, err := reader.ReadString('\n')
			if err != nil {
				break
			}

			input = strings.TrimSpace(input)
			if input == "/quit" {
				fmt.Println("[BRIDGE:QUIT]")
				io.WriteString(cpty, "/exit\r")
				mu.Lock()
				running = false
				mu.Unlock()
				break
			}

			io.WriteString(cpty, input+"\r")
		}
	}()

	// 출력 읽기
	buf := make([]byte, 4096)
	for {
		mu.Lock()
		if !running {
			mu.Unlock()
			break
		}
		mu.Unlock()

		n, err := cpty.Read(buf)
		if err != nil {
			break
		}

		output := string(buf[:n])

		// ANSI 코드 제거
		clean := stripAnsi(output)

		// 줄 단위로 필터링하여 출력
		lines := strings.Split(clean, "\n")
		for _, line := range lines {
			if isUsefulLine(line) {
				fmt.Println(strings.TrimSpace(line))
			}
		}

		// "Welcome" 감지 후 프롬프트 전송
		if !promptSent && strings.Contains(output, "Welcome") {
			promptSent = true
			go func() {
				fmt.Printf("\n[BRIDGE:WAIT:%ds]\n", waitTime)
				time.Sleep(time.Duration(waitTime) * time.Second)
				fmt.Println("[BRIDGE:SENDING]")
				io.WriteString(cpty, prompt+"\r")
			}()
		}

		// 완료 감지
		if strings.Contains(output, "===CLAUDE_TASK_COMPLETE==") {
			fmt.Println("\n[BRIDGE:COMPLETE]")
			io.WriteString(cpty, "/exit\r")
			mu.Lock()
			running = false
			mu.Unlock()
		}
	}

	fmt.Println("[BRIDGE:END]")
}
