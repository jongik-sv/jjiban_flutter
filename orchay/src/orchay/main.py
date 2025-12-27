"""orchay 메인 모듈.

WezTerm 기반 Task 스케줄러의 진입점입니다.
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import signal
import sys
from pathlib import Path

from rich.console import Console
from rich.table import Table

from orchay.models import Config, ExecutionConfig, Task, Worker, WorkerState
from orchay.scheduler import ExecutionMode, dispatch_task, filter_executable_tasks
from orchay.utils.wezterm import (
    WezTermNotFoundError,
    wezterm_list_panes,
    wezterm_send_text,
)
from orchay.wbs_parser import WbsParser
from orchay.worker import detect_worker_state

logger = logging.getLogger(__name__)
console = Console()


class Orchestrator:
    """Task 오케스트레이터.

    WBS 파일을 모니터링하고 Worker에 Task를 분배합니다.
    """

    def __init__(self, config: Config, wbs_path: Path) -> None:
        self.config = config
        self.wbs_path = wbs_path
        self.parser = WbsParser(wbs_path)
        self.workers: list[Worker] = []
        self.tasks: list[Task] = []
        self.running_tasks: set[str] = set()
        self.mode = ExecutionMode(config.execution.mode)
        self._running = False

    async def initialize(self) -> bool:
        """오케스트레이터 초기화.

        Returns:
            성공 여부
        """
        console.print("[bold cyan]orchay[/] - Task Scheduler v0.1.0\n")

        # WBS 파일 확인
        if not self.wbs_path.exists():
            console.print(f"[red]Error:[/] WBS 파일을 찾을 수 없습니다: {self.wbs_path}")
            return False

        # WezTerm pane 목록 조회
        try:
            panes = await wezterm_list_panes()
        except WezTermNotFoundError as e:
            console.print(f"[red]Error:[/] {e}")
            return False

        if not panes:
            console.print("[red]Error:[/] WezTerm pane을 찾을 수 없습니다.")
            return False

        # Worker 초기화 (현재 pane 제외, 최대 config.workers 개)
        # 현재 pane은 orchay가 실행 중인 pane
        worker_count = 0
        for pane in panes:
            if worker_count >= self.config.workers:
                break
            # Worker pane으로 등록
            self.workers.append(
                Worker(
                    id=worker_count + 1,
                    pane_id=pane.pane_id,
                    state=WorkerState.IDLE,
                )
            )
            worker_count += 1

        if not self.workers:
            console.print("[red]Error:[/] 사용 가능한 Worker pane이 없습니다.")
            return False

        # 초기 WBS 파싱
        self.tasks = await self.parser.parse()

        console.print(f"[green]WBS:[/] {self.wbs_path}")
        console.print(f"[green]Mode:[/] {self.mode.value}")
        console.print(f"[green]Workers:[/] {len(self.workers)}개")
        console.print(f"[green]Tasks:[/] {len(self.tasks)}개\n")

        return True

    async def run(self) -> None:
        """메인 스케줄링 루프 실행."""
        self._running = True
        console.print("[bold green]스케줄러 시작[/] (Ctrl+C로 종료)\n")

        while self._running:
            try:
                await self._tick()
                await asyncio.sleep(self.config.interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.exception(f"스케줄링 오류: {e}")
                await asyncio.sleep(self.config.interval)

        console.print("\n[yellow]스케줄러 종료[/]")

    async def _tick(self) -> None:
        """단일 스케줄링 사이클."""
        # 1. WBS 재파싱
        self.tasks = await self.parser.parse()

        # 2. Worker 상태 업데이트
        await self._update_worker_states()

        # 3. 실행 가능 Task 필터링
        executable = await filter_executable_tasks(
            self.tasks,
            self.mode,
            self.running_tasks,
        )

        # 4. idle Worker에 Task 분배
        for worker in self.workers:
            if not executable:
                break
            if worker.state == WorkerState.IDLE:
                task = executable.pop(0)
                await self._dispatch_to_worker(worker, task)

        # 5. 상태 출력
        self.print_status()

    async def _update_worker_states(self) -> None:
        """모든 Worker의 상태를 업데이트."""
        for worker in self.workers:
            state, _done_info = await detect_worker_state(worker.pane_id)

            # 상태 매핑
            state_map = {
                "dead": WorkerState.DEAD,
                "done": WorkerState.DONE,
                "paused": WorkerState.PAUSED,
                "error": WorkerState.ERROR,
                "blocked": WorkerState.BLOCKED,
                "idle": WorkerState.IDLE,
                "busy": WorkerState.BUSY,
            }
            new_state = state_map.get(state, WorkerState.BUSY)

            # done 상태 처리
            if new_state == WorkerState.DONE and worker.current_task:
                self.running_tasks.discard(worker.current_task)
                worker.reset()
            elif new_state == WorkerState.IDLE and worker.state == WorkerState.BUSY:
                # busy → idle 전환: Task 완료로 간주
                if worker.current_task:
                    self.running_tasks.discard(worker.current_task)
                worker.reset()
            else:
                worker.state = new_state

    async def _dispatch_to_worker(self, worker: Worker, task: Task) -> None:
        """Worker에 Task를 분배."""
        # Worker 상태 업데이트
        await dispatch_task(worker, task, self.mode)
        self.running_tasks.add(task.id)

        # /clear 전송 (옵션)
        if self.config.dispatch.clear_before_dispatch:
            try:
                await wezterm_send_text(worker.pane_id, "/clear\n")
                await asyncio.sleep(self.config.dispatch.clear_wait_time)
            except Exception as e:
                logger.warning(f"Worker {worker.id} /clear 실패: {e}")

        # 워크플로우 명령 전송
        command = f"/wf:run {task.id}\n"
        try:
            await wezterm_send_text(worker.pane_id, command)
            console.print(
                f"[cyan]Dispatch:[/] {task.id} → Worker {worker.id} ({self.mode.value})"
            )
        except Exception as e:
            logger.error(f"Worker {worker.id} 명령 전송 실패: {e}")
            worker.reset()
            self.running_tasks.discard(task.id)

    def print_status(self) -> None:
        """현재 상태 출력."""
        # Worker 상태 테이블
        table = Table(title="Worker Status", show_header=True)
        table.add_column("ID", style="cyan", width=4)
        table.add_column("Pane", width=6)
        table.add_column("State", width=10)
        table.add_column("Task", width=20)

        state_colors = {
            WorkerState.IDLE: "green",
            WorkerState.BUSY: "yellow",
            WorkerState.PAUSED: "magenta",
            WorkerState.ERROR: "red",
            WorkerState.BLOCKED: "orange3",
            WorkerState.DEAD: "dim",
            WorkerState.DONE: "blue",
        }

        for w in self.workers:
            color = state_colors.get(w.state, "white")
            table.add_row(
                str(w.id),
                str(w.pane_id),
                f"[{color}]{w.state.value}[/]",
                w.current_task or "-",
            )

        console.print(table)

        # 큐 상태
        pending = sum(1 for t in self.tasks if t.status.value == "[ ]")
        running = len(self.running_tasks)
        done = sum(1 for t in self.tasks if t.status.value == "[xx]")
        console.print(
            f"\n[dim]Queue:[/] {pending} pending, {running} running, {done} done\n"
        )

    def stop(self) -> None:
        """스케줄러 중지."""
        self._running = False


def parse_args() -> argparse.Namespace:
    """CLI 인자 파싱."""
    parser = argparse.ArgumentParser(
        prog="orchay",
        description="WezTerm 기반 Task 스케줄러",
    )
    parser.add_argument(
        "wbs",
        nargs="?",
        default=".jjiban/projects/orchay/wbs.md",
        help="WBS 파일 경로 (기본: .jjiban/projects/orchay/wbs.md)",
    )
    parser.add_argument(
        "-w", "--workers",
        type=int,
        default=3,
        help="Worker 수 (기본: 3)",
    )
    parser.add_argument(
        "-i", "--interval",
        type=int,
        default=5,
        help="모니터링 간격 초 (기본: 5)",
    )
    parser.add_argument(
        "-m", "--mode",
        choices=["design", "quick", "develop", "force"],
        default="quick",
        help="실행 모드 (기본: quick)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="분배 없이 상태만 표시",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="상세 로그 출력",
    )
    return parser.parse_args()


async def async_main() -> int:
    """비동기 메인 함수."""
    args = parse_args()

    # 로깅 설정
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    # Config 생성
    config = Config(
        workers=args.workers,
        interval=args.interval,
        execution=ExecutionConfig(mode=args.mode),
    )

    # WBS 경로
    wbs_path = Path(args.wbs)
    if not wbs_path.is_absolute():
        wbs_path = Path.cwd() / wbs_path

    # 오케스트레이터 생성 및 초기화
    orchestrator = Orchestrator(config, wbs_path)

    if not await orchestrator.initialize():
        return 1

    # dry-run 모드
    if args.dry_run:
        console.print("[yellow]--dry-run 모드: 분배 없이 상태만 표시[/]\n")
        orchestrator.print_status()
        return 0

    # 시그널 핸들러 설정
    def signal_handler() -> None:
        orchestrator.stop()

    loop = asyncio.get_event_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, signal_handler)
        except NotImplementedError:
            # Windows에서는 add_signal_handler가 지원되지 않음
            pass

    # 메인 루프 실행
    try:
        await orchestrator.run()
    except KeyboardInterrupt:
        orchestrator.stop()

    return 0


def main() -> None:
    """orchay 스케줄러 진입점."""
    try:
        exit_code = asyncio.run(async_main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        console.print("\n[yellow]중단됨[/]")
        sys.exit(0)


if __name__ == "__main__":
    main()
