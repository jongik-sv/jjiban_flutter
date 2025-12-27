"""Worker 상태 감지 모듈.

Worker pane의 출력을 분석하여 상태를 감지합니다.
파일 기반 상태 관리와 pane 출력 분석을 병행합니다.
"""

import re
import time
from dataclasses import dataclass
from typing import Literal

from orchay.utils.active_tasks import get_task_by_pane, is_pane_active, unregister_active_task
from orchay.utils.wezterm import pane_exists, wezterm_get_text

# 모듈 시작 시간 (idle 감지 지연용)
_startup_time: float = time.time()
_IDLE_DETECTION_DELAY: float = 10.0  # 시작 후 10초간 idle 감지 비활성화

# ORCHAY_DONE 패턴: ORCHAY_DONE:{task-id}:{action}:{status}[:{message}]
DONE_PATTERN = re.compile(r"ORCHAY_DONE:([^:]+):(\w+):(success|error)(?::(.+))?")

# 상태 감지 패턴들
PAUSE_PATTERNS = [
    re.compile(r"rate.*limit.*exceeded", re.IGNORECASE),
    re.compile(r"rate.*limit.*reached", re.IGNORECASE),
    re.compile(r"hit.*rate.*limit", re.IGNORECASE),
    re.compile(r"please.*wait", re.IGNORECASE),
    re.compile(r"try.*again.*later", re.IGNORECASE),
    re.compile(r"weekly.*limit.*reached", re.IGNORECASE),
    re.compile(r"resets.*at", re.IGNORECASE),
    re.compile(r"context.*limit.*exceeded", re.IGNORECASE),
    re.compile(r"conversation.*too.*long", re.IGNORECASE),
    re.compile(r"overloaded", re.IGNORECASE),
    re.compile(r"at.*capacity", re.IGNORECASE),
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
    re.compile(r"^>\s", re.MULTILINE),  # ">" 뒤에 공백 (텍스트 있어도 됨)
    re.compile(r"^>\s*$", re.MULTILINE),  # ">" 만 있는 경우
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

    파일 기반 상태 관리:
    - 파일에 작업이 있으면: ORCHAY_DONE 체크 후 busy 또는 done
    - 파일에 없으면: pane 출력으로 idle/paused/error/blocked/busy 판단

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

    # 1. 파일 기반 상태 확인 (작업 중인 pane인지)
    if is_pane_active(pane_id):
        # 작업 중인 pane: ORCHAY_DONE 신호만 체크
        done_info = parse_done_signal(output)
        if done_info:
            # 완료 신호 감지 → 파일에서 제거
            task_id = get_task_by_pane(pane_id)
            if task_id:
                unregister_active_task(task_id)
            return "done", done_info

        # 완료 신호 없으면 계속 busy
        return "busy", None

    # 2. 파일에 없으면: pane 출력 기반 판단 (초기 상태 또는 작업 완료 후)

    # 2-1. 완료 신호 패턴 (혹시 남아있는 경우)
    done_info = parse_done_signal(output)
    if done_info:
        return "done", done_info

    # 2-2. 일시 중단 패턴 (idle보다 우선)
    for pattern in PAUSE_PATTERNS:
        if pattern.search(output):
            return "paused", None

    # 2-3. 에러 패턴
    for pattern in ERROR_PATTERNS:
        if pattern.search(output):
            return "error", None

    # 2-4. 질문/입력 대기 패턴
    for pattern in BLOCKED_PATTERNS:
        if pattern.search(output):
            return "blocked", None

    # 2-5. 프롬프트 패턴 (idle) - 마지막 5줄에서 확인
    # 시작 후 10초간은 idle 감지 비활성화 (Worker 초기화 대기)
    elapsed = time.time() - _startup_time
    if elapsed >= _IDLE_DETECTION_DELAY:
        last_lines = output.strip().split("\n")[-5:]
        last_text = "\n".join(last_lines)
        for pattern in PROMPT_PATTERNS:
            if pattern.search(last_text):
                return "idle", None

    # 2-6. 기본값: 작업 중
    return "busy", None
