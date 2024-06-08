from abc import ABCMeta, abstractmethod
from typing import Dict


class ConnectionRepository(metaclass=ABCMeta):
    @abstractmethod
    def add_connection(self, connection_id: str, player_data: dict) -> None:
        pass

    @abstractmethod
    def remove_connection(self, connection_id: str) -> dict:
        pass


class EmbeddedConnectionRepository(ConnectionRepository):
    def __init__(self):
        self._connections: Dict[str, Dict] = {}

    def add_connection(self, connection_id: str, player_data: dict) -> None:
        self._connections[connection_id] = player_data

    def remove_connection(self, connection_id: str) -> dict:
        return self._connections.pop(connection_id)
