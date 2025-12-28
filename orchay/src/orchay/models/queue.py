"""Task Queue 모듈.

메모리 기반 Task 할당 관리를 제공합니다.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Assignment:
    """Task 할당 정보."""

    worker_id: int
    assigned_at: datetime
    current_step: str = "start"


class TaskQueue:
    """메모리 기반 Task 할당 큐.

    파일 I/O 없이 즉시 할당 상태를 확인하고 관리합니다.
    """

    def __init__(self) -> None:
        self._assignments: dict[str, Assignment] = {}

    def try_assign(self, task_id: str, worker_id: int, step: str = "start") -> bool:
        """Task를 Worker에 할당 시도.

        Args:
            task_id: Task ID
            worker_id: Worker ID
            step: 현재 워크플로우 단계

        Returns:
            할당 성공 여부 (이미 할당된 경우 False)
        """
        if task_id in self._assignments:
            return False

        self._assignments[task_id] = Assignment(
            worker_id=worker_id,
            assigned_at=datetime.now(),
            current_step=step,
        )
        return True

    def release(self, task_id: str) -> bool:
        """Task 할당 해제.

        Args:
            task_id: Task ID

        Returns:
            해제 성공 여부 (할당되지 않은 경우 False)
        """
        if task_id not in self._assignments:
            return False

        del self._assignments[task_id]
        return True

    def is_assigned(self, task_id: str) -> bool:
        """Task가 할당되어 있는지 확인."""
        return task_id in self._assignments

    def get_assignment(self, task_id: str) -> Assignment | None:
        """Task의 할당 정보 반환."""
        return self._assignments.get(task_id)

    def get_worker_task(self, worker_id: int) -> str | None:
        """Worker에 할당된 Task ID 반환."""
        for task_id, assignment in self._assignments.items():
            if assignment.worker_id == worker_id:
                return task_id
        return None

    def update_step(self, task_id: str, step: str) -> bool:
        """Task의 현재 단계 업데이트.

        Args:
            task_id: Task ID
            step: 새로운 워크플로우 단계

        Returns:
            업데이트 성공 여부
        """
        if task_id not in self._assignments:
            return False

        self._assignments[task_id].current_step = step
        return True

    def get_assigned_task_ids(self) -> set[str]:
        """할당된 모든 Task ID 집합 반환."""
        return set(self._assignments.keys())

    def clear(self) -> None:
        """모든 할당 초기화."""
        self._assignments.clear()

    def __len__(self) -> int:
        return len(self._assignments)

    def __contains__(self, task_id: str) -> bool:
        return task_id in self._assignments
