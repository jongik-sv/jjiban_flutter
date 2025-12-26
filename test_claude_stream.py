import sys
import os
import platform
import time
import threading

# 크로스 플랫폼 PTY
if platform.system() == 'Windows':
    from winpty import PtyProcess

    def spawn_process(cmd):
        return PtyProcess.spawn(cmd)

    def read_output(proc):
        try:
            return proc.read(1024)
        except:
            return None

    def write_input(proc, text):
        proc.write(text)

    def is_alive(proc):
        return proc.isalive()

else:
    import pty
    import os
    import select
    import subprocess

    class UnixPty:
        def __init__(self, cmd):
            self.master, slave = pty.openpty()
            self.proc = subprocess.Popen(
                cmd,
                stdin=slave,
                stdout=slave,
                stderr=slave,
                shell=True,
                close_fds=True
            )
            os.close(slave)

        def read(self, size=1024):
            if select.select([self.master], [], [], 0.1)[0]:
                return os.read(self.master, size).decode('utf-8', errors='replace')
            return None

        def write(self, text):
            os.write(self.master, text.encode('utf-8'))

        def isalive(self):
            return self.proc.poll() is None

        def close(self):
            os.close(self.master)
            self.proc.wait()

    def spawn_process(cmd):
        return UnixPty(cmd)

    def read_output(proc):
        return proc.read()

    def write_input(proc, text):
        proc.write(text)

    def is_alive(proc):
        return proc.isalive()


# 프로세스 시작
cmd = 'claude --dangerously-skip-permissions'
print(f"[Starting: {cmd}]")
print("[Type your input and press Enter to send. Type '/quit' to exit.]")
proc = spawn_process(cmd)

prompt = "./hello 폴더에 간단한 hello world html 페이지 하나만 만들어줘"

# 상태 변수
prompt_sent = False
running = True

# 사용자 입력 스레드
def user_input_thread():
    global running
    while running:
        try:
            user_input = input()
            if user_input == '/quit':
                print("[Quitting...]")
                write_input(proc, "/exit\r")
                running = False
                break
            write_input(proc, user_input + "\r")
        except EOFError:
            break
        except Exception as e:
            print(f"[Input error: {e}]")
            break

input_thread = threading.Thread(target=user_input_thread, daemon=True)
input_thread.start()

try:
    while running and is_alive(proc):
        output = read_output(proc)

        if output:
            # sys.stdout.write 사용 (print보다 빠르고 한글 지원)
            sys.stdout.write(output)
            sys.stdout.flush()

            # "Welcome" 감지 후 프롬프트 전송 (별도 스레드에서 처리 - 출력 읽기 블록 방지)
            if not prompt_sent and "Welcome" in output:
                prompt_sent = True
                def send_prompt():
                    print("\n[Welcome detected, waiting 10 seconds...]")
                    time.sleep(10)
                    print(f"[Sending prompt...]")
                    write_input(proc, prompt + "\r")
                    time.sleep(5)
                    print("[Sending extra Enter...]")
                    write_input(proc, "\r")
                threading.Thread(target=send_prompt, daemon=True).start()

            # 작업 완료 감지 시 자동 종료
            if "===CLAUDE_TASK_COMPLETE==" in output:
                print("\n[Task complete detected, exiting...]")
                write_input(proc, "/exit\r")
                running = False

        time.sleep(0.01)  # 100ms → 10ms로 줄임

except KeyboardInterrupt:
    print("\n[Ctrl+C detected, exiting...]")
    running = False
finally:
    # 프로세스 강제 종료
    try:
        if platform.system() == 'Windows':
            import os
            os.system('taskkill //F //IM claude.exe 2>nul')
        else:
            proc.close()
    except:
        pass

print("\n[Process finished]")
