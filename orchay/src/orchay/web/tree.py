"""트리 구조 변환 모듈.

TSK-02-01: WBS 트리 데이터 API
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from orchay.models import Task


@dataclass
class TreeNode:
    """트리 노드 데이터."""

    id: str  # WP-01, ACT-01-01, TSK-01-01
    type: str  # "wp", "act", "task"
    title: str  # 노드 제목
    status: str | None = None  # Task인 경우 상태 코드
    progress: float = 0.0  # WP/ACT인 경우 진행률 (0.0-100.0)
    children: list[TreeNode] = field(default_factory=list)
    level: int = 0  # 들여쓰기 레벨 (0, 1, 2)


def build_tree(tasks: list[Task]) -> list[TreeNode]:
    """Task 목록을 트리 구조로 변환.

    3레벨 Task ID (TSK-XX-XX): WP > Task
    4레벨 Task ID (TSK-XX-XX-XX): WP > ACT > Task

    Args:
        tasks: Task 목록

    Returns:
        TreeNode 리스트 (WP 노드들)
    """
    if not tasks:
        return []

    # WP별로 Task 그룹화
    wp_map: dict[str, dict[str, list[Task]]] = {}

    for task in tasks:
        hierarchy = parse_task_hierarchy(task.id)
        wp_id = hierarchy["wp"]
        act_id = hierarchy.get("act")

        if wp_id not in wp_map:
            wp_map[wp_id] = {}

        if act_id:
            if act_id not in wp_map[wp_id]:
                wp_map[wp_id][act_id] = []
            wp_map[wp_id][act_id].append(task)
        else:
            # 3레벨: ACT 없이 직접 WP 하위
            if "_direct" not in wp_map[wp_id]:
                wp_map[wp_id]["_direct"] = []
            wp_map[wp_id]["_direct"].append(task)

    # TreeNode 구조 생성
    tree: list[TreeNode] = []

    for wp_id in sorted(wp_map.keys()):
        all_tasks_under_wp: list[Task] = []
        wp_children: list[TreeNode] = []

        for act_id, act_tasks in sorted(wp_map[wp_id].items()):
            all_tasks_under_wp.extend(act_tasks)

            if act_id == "_direct":
                # 3레벨 Task들은 직접 WP 하위에 추가
                for task in act_tasks:
                    wp_children.append(
                        TreeNode(
                            id=task.id,
                            type="task",
                            title=task.title,
                            status=(
                                task.status.value
                                if hasattr(task.status, "value")
                                else str(task.status)
                            ),
                            level=1,
                        )
                    )
            else:
                # 4레벨: ACT 노드 생성
                act_children: list[TreeNode] = []
                for task in act_tasks:
                    act_children.append(
                        TreeNode(
                            id=task.id,
                            type="task",
                            title=task.title,
                            status=(
                                task.status.value
                                if hasattr(task.status, "value")
                                else str(task.status)
                            ),
                            level=2,
                        )
                    )
                act_node = TreeNode(
                    id=act_id,
                    type="act",
                    title=_extract_act_title(act_id, act_tasks),
                    progress=calculate_progress(act_tasks),
                    children=act_children,
                    level=1,
                )
                wp_children.append(act_node)

        wp_node = TreeNode(
            id=wp_id,
            type="wp",
            title=_extract_wp_title(wp_id),
            progress=calculate_progress(all_tasks_under_wp),
            children=wp_children,
            level=0,
        )
        tree.append(wp_node)

    return tree


def build_wp_children(tasks: list[Task], wp_id: str) -> list[TreeNode]:
    """특정 WP의 하위 노드만 반환.

    Args:
        tasks: 전체 Task 목록
        wp_id: WP ID (예: WP-02)

    Returns:
        해당 WP 하위의 TreeNode 리스트

    Raises:
        ValueError: WP가 존재하지 않을 때
    """
    # WP 번호 추출 (WP-02 -> 02)
    wp_num = wp_id.replace("WP-", "")

    # 해당 WP에 속한 Task 필터링
    filtered_tasks = [t for t in tasks if _belongs_to_wp(t.id, wp_num)]

    if not filtered_tasks:
        raise ValueError(f"WP '{wp_id}'를 찾을 수 없습니다")

    # 해당 WP의 전체 트리 구축 후 children 반환
    tree = build_tree(filtered_tasks)
    if tree:
        return tree[0].children
    return []


def calculate_progress(tasks: list[Task]) -> float:
    """완료된 Task 비율 계산.

    Args:
        tasks: Task 목록

    Returns:
        완료 비율 (0.0-100.0)
    """
    if not tasks:
        return 0.0

    completed = 0
    for t in tasks:
        status_value = t.status.value if hasattr(t.status, "value") else str(t.status)
        if status_value == "[xx]":
            completed += 1

    return (completed / len(tasks)) * 100


def parse_task_hierarchy(task_id: str) -> dict[str, str | None]:
    """Task ID를 WP/ACT/TSK 계층으로 파싱.

    TSK-02-01 → {"wp": "WP-02", "act": None, "task": "TSK-02-01"}
    TSK-01-01-01 → {"wp": "WP-01", "act": "ACT-01-01", "task": "TSK-01-01-01"}

    Args:
        task_id: Task ID

    Returns:
        계층 정보 딕셔너리
    """
    parts = task_id.replace("TSK-", "").split("-")

    if len(parts) == 2:
        # 3레벨: WP > TSK
        wp = f"WP-{parts[0]}"
        return {"wp": wp, "act": None, "task": task_id}
    elif len(parts) >= 3:
        # 4레벨: WP > ACT > TSK
        wp = f"WP-{parts[0]}"
        act = f"ACT-{parts[0]}-{parts[1]}"
        return {"wp": wp, "act": act, "task": task_id}
    else:
        # 비정상 ID: 기본값
        return {"wp": "WP-00", "act": None, "task": task_id}


def _belongs_to_wp(task_id: str, wp_num: str) -> bool:
    """Task가 특정 WP에 속하는지 확인."""
    # TSK-02-01 -> 02
    # TSK-01-01-01 -> 01
    parts = task_id.replace("TSK-", "").split("-")
    if parts:
        return parts[0] == wp_num
    return False


def _extract_wp_title(wp_id: str) -> str:
    """WP ID에서 제목 추출 (현재는 ID 반환)."""
    return wp_id


def _extract_act_title(act_id: str, tasks: list[Task]) -> str:
    """ACT ID에서 제목 추출 (현재는 ID 반환)."""
    return act_id
