from abc import ABCMeta, abstractmethod

from pathological.open_api.event_models import MultiplayerGameEvent


class GameEventDispatcher(metaclass=ABCMeta):
    @abstractmethod
    def dispatch(self, event: MultiplayerGameEvent) -> None:
        pass
