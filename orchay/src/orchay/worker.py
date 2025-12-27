"""Worker 상태 감지 모듈.

Worker pane의 출력을 분석하여 상태를 감지합니다.
"""

import re
from dataclasses import dataclass
from typing import Literal

from orchay.utils.wezterm import pane_exists, wezterm_get_text

# ORCHAY_DONE 패턴: ORCHAY_DONE:{task-id}:{action}:{status}[:{message}]
DONE_PATTERN = re.compile(r"ORCHAY_DONE:([^:]+):(\w+):(success|error)(?::(.+))?")

# 상태 감지 패턴들
PAUSE_PATTERNS = [
    re.compile(r"rate.*limit", re.IGNORECASE),
    re.compile(r"please.*wait", re.IGNORECASE),
    re.compile(r"try.*again", re.IGNORECASE),
    re.compile(r"weekly.*limit", re.IGNORECASE),
    re.compile(r"resets.*at", re.IGNORECASE),
    re.compile(r"context.*limit", re.IGNORECASE),
    re.compile(r"conversation.*too.*long", re.IGNORECASE),
    re.compile(r"overloaded", re.IGNORECASE),
    re.compile(r"capacity", re.IGNORECASE),
]

ERROR_PATTERNS = [
    re.compile(r"Error:", re.IGNORECASE),
    re.compile(r"Failed:", re.IGNORECASE),
    re.compile(r"Exception:", re.IGNORECASE),
    re.compile(r"❌"),
    re.compile(r"fatal:", re.IGNORECASE),
]

BLOCKED_PATTERNS = [
    re.compile(r"\?\s*$"),
    re.compile(r"\(y/n\)", re.IGNORECASE),
    re.compile(r"선택", re.IGNORECASE),
    re.compile(r"Press.*to continue", re.IGNORECASE),
]

PROMPT_PATTERNS = [
    re.compile(r"^>\s*$", re.MULTILINE),
    re.compile(r"╭─"),
    re.compile(r"❯"),
]


@dataclass
class DoneInfo:
    """ORCHAY_DONE 파싱 결과."""

    task_id: str
    action: str
    status: Literal["success", "error"]
    message: str | None = None


def parse_done_signal(text: str) -> DoneInfo | None:
    """ORCHAY_DONE 신호를 파싱합니다.

    Args:
        text: pane 출력 텍스트

    Returns:
        DoneInfo 또는 None (패턴 미매칭 시)
    """
    matches = list(DONE_PATTERN.finditer(text))
    if not matches:
        return None

    # 마지막 매치 사용 (가장 최근 완료 신호)
    match = matches[-1]
    return DoneInfo(
        task_id=match.group(1),
        action=match.group(2),
        status=match.group(3),  # type: ignore[arg-type]
        message=match.group(4),
    )


WorkerState = Literal["dead", "done", "paused", "error", "blocked", "idle", "busy"]


async def detect_worker_state(pane_id: int) -> tuple[WorkerState, DoneInfo | None]:
    """Worker 상태를 감지합니다.

    우선순위: dead > done > paused > error > blocked > idle > busy

    Args:
        pane_id: WezTerm pane ID

    Returns:
        (상태, DoneInfo 또는 None) 튜플
    """
    # 0. pane 존재 확인
    if not await pane_exists(pane_id):
        return "dead", None

    # 출력 텍스트 조회 (최근 50줄)
    output = await wezterm_get_text(pane_id, lines=50)

    # 빈 출력이면 busy로 간주
    if not output.strip():
        return "busy", None

    # 1. 완료 신호 패턴 (최우선)
    done_info = parse_done_signal(output)
    if done_info:
        return "done", done_info

    # 2. 일시 중단 패턴
    for pattern in PAUSE_PATTERNS:
        if pattern.search(output):
            return "paused", None

    # 3. 에러 패턴
    for pattern in ERROR_PATTERNS:
        if pattern.search(output):
            return "error", None

    # 4. 질문/입력 대기 패턴
    for pattern in BLOCKED_PATTERNS:
        if pattern.search(output):
            return "blocked", None

    # 5. 프롬프트 패턴 (idle) - 마지막 3줄에서 확인
    last_lines = output.strip().split("\n")[-3:]
    last_text = "\n".join(last_lines)
    for pattern in PROMPT_PATTERNS:
        if pattern.search(last_text):
            return "idle", None

    # 6. 기본값: 작업 중
    return "busy", None
