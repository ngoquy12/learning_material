import asyncio
from typing import Dict, Set, Optional

# Global task registries and cancellation state
_ACTIVE_TASKS: Dict[int, asyncio.Task] = {}
_ACTIVE_COURSE_MAP: Dict[int, int] = {}  # lesson_id -> course_id
_CANCELLED_LESSONS: Set[int] = set()
_CANCELLED_COURSES: Set[int] = set()
_CANCEL_ALL_FLAG: bool = False


def reset_cancel_flags():
    global _CANCEL_ALL_FLAG
    _CANCEL_ALL_FLAG = False


def register_task(lesson_id: int, course_id: Optional[int], task: asyncio.Task):
    _ACTIVE_TASKS[lesson_id] = task
    if course_id is not None:
        _ACTIVE_COURSE_MAP[lesson_id] = course_id
    _CANCELLED_LESSONS.discard(lesson_id)


def unregister_task(lesson_id: int):
    _ACTIVE_TASKS.pop(lesson_id, None)
    _ACTIVE_COURSE_MAP.pop(lesson_id, None)


def is_cancelled(lesson_id: int, course_id: Optional[int] = None) -> bool:
    if _CANCEL_ALL_FLAG:
        return True
    if lesson_id in _CANCELLED_LESSONS:
        return True
    c_id = course_id or _ACTIVE_COURSE_MAP.get(lesson_id)
    if c_id and c_id in _CANCELLED_COURSES:
        return True
    return False


def get_active_task_count() -> int:
    return sum(1 for task in _ACTIVE_TASKS.values() if not task.done())


def get_active_lesson_ids() -> list[int]:
    return [lid for lid, task in _ACTIVE_TASKS.items() if not task.done()]



def cancel_all_tasks() -> int:
    global _CANCEL_ALL_FLAG
    _CANCEL_ALL_FLAG = True
    cancelled_count = 0

    for lesson_id, task in list(_ACTIVE_TASKS.items()):
        if not task.done():
            task.cancel()
            cancelled_count += 1
            print(f"[ProcessManager] Cancelled task for lesson_id {lesson_id}")

    return cancelled_count


def cancel_course_tasks(course_id: int) -> int:
    _CANCELLED_COURSES.add(course_id)
    cancelled_count = 0

    for lesson_id, c_id in list(_ACTIVE_COURSE_MAP.items()):
        if c_id == course_id:
            task = _ACTIVE_TASKS.get(lesson_id)
            if task and not task.done():
                task.cancel()
                cancelled_count += 1
                print(f"[ProcessManager] Cancelled lesson_id {lesson_id} for course {course_id}")

    return cancelled_count


def cancel_lesson_task(lesson_id: int) -> bool:
    _CANCELLED_LESSONS.add(lesson_id)
    task = _ACTIVE_TASKS.get(lesson_id)
    if task and not task.done():
        task.cancel()
        print(f"[ProcessManager] Cancelled lesson_id {lesson_id}")
        return True
    return False
