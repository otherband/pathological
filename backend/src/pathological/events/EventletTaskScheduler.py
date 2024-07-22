from typing import Callable

from pathological.events.task_scheduler import TaskScheduler
import eventlet


class EventletTaskScheduler(TaskScheduler):
    def run_after(self, seconds_delay: int, f: Callable) -> None:
        eventlet.spawn_after(
            seconds=seconds_delay,
            func=f
        )
