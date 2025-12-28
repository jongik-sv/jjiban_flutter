"""작업 중 상태 파일 관리 모듈.

`.jjiban/logs/orchay-active.json` 파일로 Worker 작업 상태를 추적합니다.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import TypedDict


class ActiveTaskInfo(TypedDict):
    """작업 중인 Task 정보."""

    worker: int
    paneId: int
    startedAt: str
    currentStep: str


class ActiveTasksData(TypedDict):
    """orchay-active.json 파일 구조."""

    activeTasks: dict[str, ActiveTaskInfo]
    pausedWorkers: list[int]  # 수동 일시정지된 Worker ID 목록
    schedulerState: str  # running, paused, stopped


def get_active_tasks_path() -> Path:
    """상태 파일 경로 반환."""
    # 현재 작업 디렉토리 기준 .jjiban/logs/
    return Path.cwd() / ".jjiban" / "logs" / "orchay-active.json"


def _get_default_data() -> ActiveTasksData:
    """기본 데이터 반환."""
    return {
        "activeTasks": {},
        "pausedWorkers": [],
        "schedulerState": "running",
    }


def load_active_tasks() -> ActiveTasksData:
    """상태 파일 로드."""
    path = get_active_tasks_path()
    if not path.exists():
        return _get_default_data()

    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
            # 기본값 보장
            if "activeTasks" not in data:
                data["activeTasks"] = {}
            if "pausedWorkers" not in data:
                data["pausedWorkers"] = []
            if "schedulerState" not in data:
                data["schedulerState"] = "running"
            return data
    except (json.JSONDecodeError, OSError):
        return _get_default_data()


def save_active_tasks(data: ActiveTasksData) -> None:
    """상태 파일 저장."""
    path = get_active_tasks_path()
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def clear_active_tasks() -> None:
    """상태 파일 초기화 (스케줄러 시작 시).

    pausedWorkers와 schedulerState는 유지합니다.
    """
    data = load_active_tasks()
    data["activeTasks"] = {}
    save_active_tasks(data)


def register_active_task(
    task_id: str,
    worker_id: int,
    pane_id: int,
    step: str = "start",
) -> None:
    """Task 분배 시 작업 중 상태 등록."""
    data = load_active_tasks()
    data["activeTasks"][task_id] = {
        "worker": worker_id,
        "paneId": pane_id,
        "startedAt": datetime.now().isoformat(),
        "currentStep": step,
    }
    save_active_tasks(data)


def update_active_task_step(task_id: str, step: str) -> None:
    """Task 단계 갱신."""
    data = load_active_tasks()
    if task_id in data["activeTasks"]:
        data["activeTasks"][task_id]["currentStep"] = step
        save_active_tasks(data)


def unregister_active_task(task_id: str) -> None:
    """Task 완료(ORCHAY_DONE) 시 작업 중 상태 해제.

    Args:
        task_id: Task ID (project/TSK-XX-XX 또는 TSK-XX-XX 형식 모두 지원)
    """
    data = load_active_tasks()

    # 정확한 ID로 먼저 찾기
    if task_id in data["activeTasks"]:
        del data["activeTasks"][task_id]
        save_active_tasks(data)
        return

    # project prefix 제거 후 찾기 (orchay_web/TSK-01-03 → TSK-01-03)
    if "/" in task_id:
        pure_id = task_id.split("/")[-1]
        if pure_id in data["activeTasks"]:
            del data["activeTasks"][pure_id]
            save_active_tasks(data)
            return

    # prefix 붙은 형태로도 찾기 (TSK-01-03 → */TSK-01-03)
    for key in list(data["activeTasks"].keys()):
        if key.endswith(f"/{task_id}") or key == task_id:
            del data["activeTasks"][key]
            save_active_tasks(data)
            return


def is_pane_active(pane_id: int) -> bool:
    """해당 pane이 작업 중인지 확인."""
    data = load_active_tasks()
    return any(task_info["paneId"] == pane_id for task_info in data["activeTasks"].values())


def get_task_by_pane(pane_id: int) -> str | None:
    """pane에 할당된 Task ID 반환."""
    data = load_active_tasks()
    for task_id, task_info in data["activeTasks"].items():
        if task_info["paneId"] == pane_id:
            return task_id
    return None


# === Worker Pause/Resume 관리 ===


def pause_worker(worker_id: int) -> None:
    """Worker 수동 일시정지.

    Args:
        worker_id: Worker ID (1, 2, 3...)
    """
    data = load_active_tasks()
    paused = data.get("pausedWorkers", [])
    if worker_id not in paused:
        paused.append(worker_id)
        data["pausedWorkers"] = paused
        save_active_tasks(data)


def resume_worker(worker_id: int) -> None:
    """Worker 수동 일시정지 해제.

    Args:
        worker_id: Worker ID (1, 2, 3...)
    """
    data = load_active_tasks()
    paused = data.get("pausedWorkers", [])
    if worker_id in paused:
        paused.remove(worker_id)
        data["pausedWorkers"] = paused
        save_active_tasks(data)


def is_worker_paused(worker_id: int) -> bool:
    """Worker가 수동 일시정지 상태인지 확인.

    Args:
        worker_id: Worker ID

    Returns:
        일시정지 상태 여부
    """
    data = load_active_tasks()
    return worker_id in data.get("pausedWorkers", [])


def get_paused_workers() -> list[int]:
    """수동 일시정지된 Worker ID 목록 반환."""
    data = load_active_tasks()
    return data.get("pausedWorkers", [])


# === Scheduler State 관리 ===


def set_scheduler_state(state: str) -> None:
    """스케줄러 상태 설정.

    Args:
        state: running, paused, stopped 중 하나
    """
    data = load_active_tasks()
    data["schedulerState"] = state
    save_active_tasks(data)


def get_scheduler_state() -> str:
    """스케줄러 상태 반환.

    Returns:
        running, paused, stopped 중 하나
    """
    data = load_active_tasks()
    return data.get("schedulerState", "running")
