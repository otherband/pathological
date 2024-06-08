from abc import ABCMeta, abstractmethod

from pathological.events.named_events import MultiplayerGameEvent


class EventDispatcher(metaclass=ABCMeta):
    @abstractmethod
    def dispatch(self,
                 event_name: str,
                 event_data: dict) -> None:
        pass

    @abstractmethod
    def dispatch_named(self, event: MultiplayerGameEvent):
        pass
