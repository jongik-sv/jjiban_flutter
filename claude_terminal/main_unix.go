//go:build !windows

package main

import (
	"bufio"
	"flag"
	"fmt"
	"io"
	"os"
	"os/exec"
	"regexp"
	"strings"
	"sync"
	"time"

	"github.com/creack/pty"
)

// ANSI escape 코드 제거
var ansiRegex = regexp.MustCompile(`\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])`)

func stripAnsi(s string) string {
	return ansiRegex.ReplaceAllString(s, "")
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
	cmd := exec.Command("claude", "--dangerously-skip-permissions")
	ptmx, err := pty.Start(cmd)
	if err != nil {
		fmt.Printf("[ERROR] %v\n", err)
		os.Exit(1)
	}
	defer ptmx.Close()

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
				io.WriteString(ptmx, "/exit\r")
				mu.Lock()
				running = false
				mu.Unlock()
				break
			}

			io.WriteString(ptmx, input+"\r")
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

		n, err := ptmx.Read(buf)
		if err != nil {
			break
		}

		output := string(buf[:n])

		// ANSI 코드 제거 후 출력
		clean := stripAnsi(output)
		if clean != "" {
			fmt.Print(clean)
		}

		// "Welcome" 감지 후 프롬프트 전송
		if !promptSent && strings.Contains(output, "Welcome") {
			promptSent = true
			go func() {
				fmt.Printf("\n[BRIDGE:WAIT:%ds]\n", waitTime)
				time.Sleep(time.Duration(waitTime) * time.Second)
				fmt.Println("[BRIDGE:SENDING]")
				io.WriteString(ptmx, prompt+"\r")
			}()
		}

		// 완료 감지
		if strings.Contains(output, "===CLAUDE_TASK_COMPLETE==") {
			fmt.Println("\n[BRIDGE:COMPLETE]")
			io.WriteString(ptmx, "/exit\r")
			mu.Lock()
			running = false
			mu.Unlock()
		}
	}

	cmd.Wait()
	fmt.Println("[BRIDGE:END]")
}
