"""orchay CLI 모듈.

서브커맨드 기반 CLI 인터페이스를 제공합니다.

사용법:
    orchay                      # 스케줄러 실행 (기본)
    orchay run [options]        # 스케줄러 실행
    orchay exec start <task> <step>  # Task 실행 시작 등록
    orchay exec stop <task>     # Task 실행 완료 해제
    orchay exec list            # 실행 중인 Task 목록
    orchay exec clear           # 모든 실행 상태 초기화
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime

from rich.console import Console
from rich.table import Table

from orchay.utils.active_tasks import (
    clear_active_tasks,
    load_active_tasks,
    register_active_task,
    unregister_active_task,
    update_active_task_step,
)

console = Console()


def create_parser() -> argparse.ArgumentParser:
    """CLI 파서 생성."""
    parser = argparse.ArgumentParser(
        prog="orchay",
        description="WezTerm 기반 Task 스케줄러",
    )
    subparsers = parser.add_subparsers(dest="command", help="사용 가능한 명령어")

    # run 서브커맨드 (스케줄러 실행)
    run_parser = subparsers.add_parser("run", help="스케줄러 실행")
    run_parser.add_argument(
        "wbs",
        nargs="?",
        default=".jjiban/projects/orchay/wbs.md",
        help="WBS 파일 경로 (기본: .jjiban/projects/orchay/wbs.md)",
    )
    run_parser.add_argument(
        "-w", "--workers",
        type=int,
        default=3,
        help="Worker 수 (기본: 3)",
    )
    run_parser.add_argument(
        "-i", "--interval",
        type=int,
        default=5,
        help="모니터링 간격 초 (기본: 5)",
    )
    run_parser.add_argument(
        "-m", "--mode",
        choices=["design", "quick", "develop", "force"],
        default="quick",
        help="실행 모드 (기본: quick)",
    )
    run_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="분배 없이 상태만 표시",
    )
    run_parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="상세 로그 출력",
    )

    # exec 서브커맨드 (실행 상태 관리)
    exec_parser = subparsers.add_parser(
        "exec",
        help="Task 실행 상태 관리 (워크플로우 훅용)",
    )
    exec_subparsers = exec_parser.add_subparsers(dest="exec_command", help="exec 명령어")

    # exec start
    start_parser = exec_subparsers.add_parser("start", help="Task 실행 시작 등록")
    start_parser.add_argument("task_id", help="Task ID (예: TSK-01-01)")
    start_parser.add_argument("step", help="워크플로우 단계 (예: design, build, done)")
    start_parser.add_argument(
        "-w", "--worker",
        type=int,
        default=0,
        help="Worker ID (기본: 0)",
    )
    start_parser.add_argument(
        "-p", "--pane",
        type=int,
        default=0,
        help="Pane ID (기본: 0)",
    )

    # exec stop
    stop_parser = exec_subparsers.add_parser("stop", help="Task 실행 완료 해제")
    stop_parser.add_argument("task_id", help="Task ID (예: TSK-01-01)")

    # exec update
    update_parser = exec_subparsers.add_parser("update", help="Task 단계 갱신")
    update_parser.add_argument("task_id", help="Task ID")
    update_parser.add_argument("step", help="새 단계")

    # exec list
    exec_subparsers.add_parser("list", help="실행 중인 Task 목록")

    # exec clear
    exec_subparsers.add_parser("clear", help="모든 실행 상태 초기화")

    return parser


def exec_start(args: argparse.Namespace) -> int:
    """Task 실행 시작 등록."""
    try:
        register_active_task(
            task_id=args.task_id,
            worker_id=args.worker,
            pane_id=args.pane,
            step=args.step,
        )
        console.print(f"[green]✓[/] {args.task_id} 실행 시작 등록 (step: {args.step})")
        return 0
    except Exception as e:
        console.print(f"[red]✗[/] 등록 실패: {e}")
        return 1


def exec_stop(args: argparse.Namespace) -> int:
    """Task 실행 완료 해제."""
    try:
        unregister_active_task(args.task_id)
        console.print(f"[green]✓[/] {args.task_id} 실행 완료 해제")
        return 0
    except Exception as e:
        console.print(f"[red]✗[/] 해제 실패: {e}")
        return 1


def exec_update(args: argparse.Namespace) -> int:
    """Task 단계 갱신."""
    try:
        update_active_task_step(args.task_id, args.step)
        console.print(f"[green]✓[/] {args.task_id} 단계 갱신 → {args.step}")
        return 0
    except Exception as e:
        console.print(f"[red]✗[/] 갱신 실패: {e}")
        return 1


def exec_list(_args: argparse.Namespace) -> int:
    """실행 중인 Task 목록 출력."""
    data = load_active_tasks()
    active = data.get("activeTasks", {})

    if not active:
        console.print("[dim]실행 중인 Task가 없습니다.[/]")
        return 0

    table = Table(title="실행 중인 Task", show_header=True)
    table.add_column("Task ID", style="cyan")
    table.add_column("Worker", justify="center")
    table.add_column("Pane", justify="center")
    table.add_column("Step", style="yellow")
    table.add_column("Started At", style="dim")

    for task_id, info in active.items():
        started = info.get("startedAt", "-")
        if started != "-":
            try:
                dt = datetime.fromisoformat(started)
                started = dt.strftime("%H:%M:%S")
            except ValueError:
                pass

        table.add_row(
            task_id,
            str(info.get("worker", "-")),
            str(info.get("paneId", "-")),
            info.get("currentStep", "-"),
            started,
        )

    console.print(table)
    return 0


def exec_clear(_args: argparse.Namespace) -> int:
    """모든 실행 상태 초기화."""
    try:
        clear_active_tasks()
        console.print("[green]✓[/] 모든 실행 상태 초기화 완료")
        return 0
    except Exception as e:
        console.print(f"[red]✗[/] 초기화 실패: {e}")
        return 1


def handle_exec(args: argparse.Namespace) -> int:
    """exec 서브커맨드 처리."""
    if args.exec_command == "start":
        return exec_start(args)
    elif args.exec_command == "stop":
        return exec_stop(args)
    elif args.exec_command == "update":
        return exec_update(args)
    elif args.exec_command == "list":
        return exec_list(args)
    elif args.exec_command == "clear":
        return exec_clear(args)
    else:
        console.print("[yellow]사용법:[/] orchay exec {start|stop|update|list|clear}")
        return 1


def cli_main() -> int:
    """CLI 메인 함수."""
    parser = create_parser()

    # 인자가 없으면 기본적으로 run 실행
    if len(sys.argv) == 1:
        # 스케줄러 실행
        from orchay.main import main as run_scheduler
        run_scheduler()
        return 0

    args = parser.parse_args()

    if args.command == "exec":
        return handle_exec(args)
    elif args.command == "run":
        # 스케줄러 실행
        from orchay.main import async_main
        import asyncio
        return asyncio.run(async_main(args))
    elif args.command is None:
        # 서브커맨드 없이 인자가 있는 경우 (기존 호환성)
        # 기존 main.py 방식으로 처리
        from orchay.main import main as run_scheduler
        run_scheduler()
        return 0
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(cli_main())
