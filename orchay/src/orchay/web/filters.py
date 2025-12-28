"""Jinja2 템플릿 필터 모듈.

TSK-03-02: Worker 상태 바 구현
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from orchay.models.worker import WorkerState


def status_icon(state: WorkerState) -> str:
    """WorkerState를 이모지 아이콘으로 변환.

    Args:
        state: Worker 상태

    Returns:
        상태별 이모지 문자열
    """
    from orchay.models.worker import WorkerState

    icons: dict[WorkerState, str] = {
        WorkerState.IDLE: "🟢",
        WorkerState.BUSY: "🟡",
        WorkerState.PAUSED: "⏸️",
        WorkerState.ERROR: "🔴",
        WorkerState.BLOCKED: "⊘",
        WorkerState.DEAD: "💀",
        WorkerState.DONE: "✅",
    }
    return icons.get(state, "❓")


def status_bg(state: WorkerState) -> str:
    """WorkerState를 Tailwind 배경색 클래스로 변환.

    Args:
        state: Worker 상태

    Returns:
        Tailwind CSS 배경색 클래스
    """
    from orchay.models.worker import WorkerState

    colors: dict[WorkerState, str] = {
        WorkerState.IDLE: "bg-green-500/20",
        WorkerState.BUSY: "bg-yellow-500/20",
        WorkerState.PAUSED: "bg-purple-500/20",
        WorkerState.ERROR: "bg-red-500/20",
        WorkerState.BLOCKED: "bg-gray-500/20",
        WorkerState.DEAD: "bg-gray-700/20",
        WorkerState.DONE: "bg-emerald-500/20",
    }
    return colors.get(state, "bg-gray-500/20")
