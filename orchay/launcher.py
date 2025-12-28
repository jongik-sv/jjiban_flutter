#!/usr/bin/env python3
"""WezTerm 레이아웃으로 orchay 스케줄러 실행.

사용법:
    python launcher.py [OPTIONS]
    python launcher.py --help                    # 도움말 표시
    python launcher.py -w 5                      # Worker 5개로 실행
    python launcher.py --scheduler-cols 100      # 스케줄러 100 columns
    python launcher.py --worker-cols 120         # Worker 120 columns
    python launcher.py --font-size 10            # 폰트 크기 10pt
    python launcher.py -w 5 -m quick             # 조합 사용

Launcher 옵션:
    -w, --workers N       Worker pane 개수 (기본: 3)
    --scheduler-cols N    스케줄러 너비 columns (기본: 100)
    --worker-cols N       Worker 너비 columns (기본: 120)
    --font-size F         폰트 크기 (기본: 11.0)

나머지 옵션은 orchay에 전달됩니다 (-m, --dry-run 등)
"""

from __future__ import annotations

import argparse
import os
import platform
import subprocess
import sys
import time


def get_venv_python() -> str:
    """가상환경 Python 경로 반환."""
    launcher_dir = os.path.dirname(os.path.abspath(__file__))
    if platform.system() == "Windows":
        return os.path.join(launcher_dir, ".venv", "Scripts", "python.exe")
    return os.path.join(launcher_dir, ".venv", "bin", "python")


def show_orchay_help() -> int:
    """orchay --help 실행."""
    venv_python = get_venv_python()
    result = subprocess.run([venv_python, "-m", "orchay", "--help"])
    return result.returncode


def kill_mux_server() -> None:
    """기존 mux-server 종료 및 완전히 종료될 때까지 대기."""
    if platform.system() == "Windows":
        # mux-server 종료
        subprocess.run(
            ["taskkill", "/f", "/im", "wezterm-mux-server.exe"],
            capture_output=True,
        )
        # wezterm-gui도 종료 (connect 모드로 인해 같이 종료해야 함)
        subprocess.run(
            ["taskkill", "/f", "/im", "wezterm-gui.exe"],
            capture_output=True,
        )
    else:
        subprocess.run(["pkill", "-f", "wezterm-mux-server"], capture_output=True)
        subprocess.run(["pkill", "-f", "wezterm-gui"], capture_output=True)

    # 프로세스 완전 종료 대기
    time.sleep(1)


def parse_args() -> tuple[argparse.Namespace, list[str]]:
    """launcher 전용 인자 파싱.

    launcher 전용 옵션만 파싱하고, 나머지는 orchay에 그대로 전달합니다.

    launcher 전용: --scheduler-cols, --worker-cols, --font-size
    orchay 전달: project, -w, -m, --web, --port, --dry-run 등
    """
    parser = argparse.ArgumentParser(add_help=False)
    # launcher 전용 옵션 (WezTerm 레이아웃 관련)
    parser.add_argument(
        "--scheduler-cols",
        type=int,
        default=100,
        help="스케줄러 pane 너비 columns (기본: 100)",
    )
    parser.add_argument(
        "--worker-cols",
        type=int,
        default=120,
        help="Worker pane 너비 columns (기본: 120)",
    )
    parser.add_argument(
        "--font-size",
        type=float,
        default=11.0,
        help="폰트 크기 (기본: 11.0)",
    )
    return parser.parse_known_args()


def main() -> int:
    """메인 함수."""
    # --help 또는 -h 처리 (orchay 도움말 표시)
    if "-h" in sys.argv or "--help" in sys.argv:
        print("Launcher 전용 옵션 (WezTerm 레이아웃):")
        print("  --scheduler-cols N    스케줄러 너비 columns (기본: 100)")
        print("  --worker-cols N       Worker 너비 columns (기본: 120)")
        print("  --font-size F         폰트 크기 (기본: 11.0)")
        print()
        print("나머지 옵션은 orchay에 그대로 전달됩니다:")
        print()
        return show_orchay_help()

    # launcher 전용 인자와 나머지 분리
    launcher_args, orchay_args = parse_args()

    # 가상환경 Python 경로
    venv_python = get_venv_python()

    # 현재 작업 디렉토리 (실행 위치)
    cwd = os.getcwd()

    # orchay_args에서 -w 값 추출 (WezTerm 레이아웃용)
    workers = 3  # 기본값
    for i, arg in enumerate(orchay_args):
        if arg in ("-w", "--workers") and i + 1 < len(orchay_args):
            try:
                workers = int(orchay_args[i + 1])
            except ValueError:
                pass
            break

    # 0번 pane에서 실행할 명령 구성
    # orchay run + 모든 orchay 옵션 전달
    cmd = f'"{venv_python}" -m orchay run'
    if orchay_args:
        args_str = " ".join(orchay_args)
        cmd = f"{cmd} {args_str}"

    # 웹 서버 기본 활성화 (사용자가 명시하지 않은 경우)
    if "--web" not in orchay_args and "--web-only" not in orchay_args:
        cmd = f"{cmd} --web"
    if "--port" not in orchay_args:
        cmd = f"{cmd} --port 9000"

    # 환경변수 설정
    os.environ["WEZTERM_SHELL_CMD"] = cmd
    os.environ["WEZTERM_CWD"] = cwd
    os.environ["WEZTERM_WORKERS"] = str(workers)
    os.environ["WEZTERM_SCHEDULER_COLS"] = str(launcher_args.scheduler_cols)
    os.environ["WEZTERM_WORKER_COLS"] = str(launcher_args.worker_cols)
    os.environ["WEZTERM_FONT_SIZE"] = str(launcher_args.font_size)

    # orchay 전용 WezTerm 설정 파일 사용
    orchay_config = os.path.expanduser("~/.wezterm-orchay.lua")
    if os.path.exists(orchay_config):
        os.environ["WEZTERM_CONFIG_FILE"] = orchay_config

    print("[launcher] Killing existing WezTerm processes...")

    # 기존 mux-server 종료 (새 환경변수 적용을 위해)
    kill_mux_server()

    # 웹 포트 추출 (로그 출력용)
    web_port = 9000
    if "--port" in orchay_args:
        try:
            port_idx = orchay_args.index("--port")
            if port_idx + 1 < len(orchay_args):
                web_port = int(orchay_args[port_idx + 1])
        except (ValueError, IndexError):
            pass

    print("[launcher] Starting WezTerm with:")
    print(f"           Layout: {launcher_args.scheduler_cols} + {workers} x {launcher_args.worker_cols} cols")
    print(f"           Font: {launcher_args.font_size}pt")
    print(f"           Web: http://localhost:{web_port}")
    print(f"           Command: {cmd}")

    # wezterm 실행
    subprocess.Popen(["wezterm"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
