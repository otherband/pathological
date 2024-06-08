from abc import ABCMeta, abstractmethod


class EventDispatcher(metaclass=ABCMeta):
    @abstractmethod
    def dispatch(self,
                 event_name: str,
                 event_data: dict) -> None:
        pass
