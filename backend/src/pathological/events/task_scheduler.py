from abc import ABCMeta, abstractmethod
from typing import Callable


class TaskScheduler(metaclass=ABCMeta):
    @abstractmethod
    def run_after(self,
                  seconds_delay: int,
                  f: Callable) -> None:
        pass
