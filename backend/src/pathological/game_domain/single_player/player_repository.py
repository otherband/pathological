from abc import ABCMeta, abstractmethod

from pathological.models.game_models import PlayerSession


class PlayerSessionRepository(metaclass=ABCMeta):

    @abstractmethod
    def get_player(self, player_id: str) -> PlayerSession:
        pass

    @abstractmethod
    def add_player_session(self, player: PlayerSession):
        pass

    @abstractmethod
    def update_player(self, player_updated: PlayerSession):
        pass


class EmbeddedPlayerSessionRepository(PlayerSessionRepository):
    def __init__(self):
        self.players = {}

    def get_player(self, player_id: str) -> PlayerSession:
        return self.players[player_id]

    def add_player_session(self, player: PlayerSession):
        self.players[player.player_id] = player

    def update_player(self, player_updated: PlayerSession):
        self.players[player_updated.player_id] = player_updated
