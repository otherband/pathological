from abc import ABCMeta, abstractmethod

from openapi_client.api_response import BaseModel


class EventDispatcher(metaclass=ABCMeta):
    @abstractmethod
    def dispatch(self, event_data: BaseModel) -> None:
        pass
