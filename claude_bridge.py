#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Claude CLI Bridge for Flutter
-p --output-format stream-json --include-partial-messages 사용
"""
import sys
import os
import platform
import threading
import argparse
import subprocess

# Windows UTF-8 강제 설정
if platform.system() == 'Windows':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


def main():
    parser = argparse.ArgumentParser(description='Claude CLI Bridge')
    parser.add_argument('--prompt', '-p', type=str, required=True, help='Prompt to send')
    args = parser.parse_args()

    prompt = args.prompt
    print(f"[BRIDGE:START]", flush=True)
    print(f"[BRIDGE:PROMPT:{prompt}]", flush=True)

    # Claude CLI 실행 (-p 모드 + text)
    claude_cmd = r'C:\Users\sviso\AppData\Roaming\npm\claude.cmd'
    cmd = [
        claude_cmd, '-p',
        '--dangerously-skip-permissions',
        '--output-format', 'text',
        '--verbose',
        prompt
    ]

    # subprocess 실행 (shell=True로 cmd.exe 통해 실행)
    cmd_str = f'"{claude_cmd}" -p --dangerously-skip-permissions --output-format stream-json --verbose "{prompt}"'
    proc = subprocess.Popen(
        cmd_str,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
    )

    # stderr 스레드
    def read_stderr():
        for line in proc.stderr:
            try:
                text = line.decode('utf-8', errors='replace').strip()
                if text:
                    print(f"[STDERR] {text}", flush=True)
            except:
                pass

    threading.Thread(target=read_stderr, daemon=True).start()

    try:
        # stdout에서 줄 단위로 읽기 (plain text)
        for line in iter(proc.stdout.readline, b''):
            text = line.decode('utf-8', errors='replace')
            if text:
                print(text, end='', flush=True)

        proc.wait()
        print(f"\n[BRIDGE:EXIT:{proc.returncode}]", flush=True)

    except KeyboardInterrupt:
        print("\n[BRIDGE:INTERRUPTED]", flush=True)
        proc.terminate()

    print("[BRIDGE:END]", flush=True)


if __name__ == '__main__':
    main()
