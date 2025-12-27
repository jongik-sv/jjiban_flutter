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


def get_active_tasks_path() -> Path:
    """상태 파일 경로 반환."""
    # 현재 작업 디렉토리 기준 .jjiban/logs/
    return Path.cwd() / ".jjiban" / "logs" / "orchay-active.json"


def load_active_tasks() -> ActiveTasksData:
    """상태 파일 로드."""
    path = get_active_tasks_path()
    if not path.exists():
        return {"activeTasks": {}}

    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {"activeTasks": {}}


def save_active_tasks(data: ActiveTasksData) -> None:
    """상태 파일 저장."""
    path = get_active_tasks_path()
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def clear_active_tasks() -> None:
    """상태 파일 초기화 (스케줄러 시작 시)."""
    save_active_tasks({"activeTasks": {}})


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
    """Task 완료(ORCHAY_DONE) 시 작업 중 상태 해제."""
    data = load_active_tasks()
    if task_id in data["activeTasks"]:
        del data["activeTasks"][task_id]
        save_active_tasks(data)


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
