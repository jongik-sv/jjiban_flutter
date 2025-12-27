"""Worker 모델 정의."""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class WorkerState(str, Enum):
    """Worker 상태."""

    IDLE = "idle"
    BUSY = "busy"
    PAUSED = "paused"
    ERROR = "error"
    BLOCKED = "blocked"
    DEAD = "dead"
    DONE = "done"


class Worker(BaseModel):
    """Claude Code Worker 모델."""

    id: int = Field(description="Worker 번호 (1, 2, 3...)")
    pane_id: int = Field(description="WezTerm pane ID")
    state: WorkerState = Field(default=WorkerState.IDLE, description="현재 상태")
    current_task: str | None = Field(default=None, description="현재 작업 중인 Task ID")
    current_step: str | None = Field(default=None, description="현재 workflow 단계")
    dispatch_time: datetime | None = Field(default=None, description="Task 분배 시간")
    retry_count: int = Field(default=0, description="재시도 횟수")

    def is_available(self) -> bool:
        """작업 할당 가능 여부."""
        return self.state == WorkerState.IDLE

    def reset(self) -> None:
        """Worker 상태 초기화."""
        self.state = WorkerState.IDLE
        self.current_task = None
        self.current_step = None
        self.dispatch_time = None
        self.retry_count = 0
