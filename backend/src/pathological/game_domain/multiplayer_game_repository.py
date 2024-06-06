from abc import ABCMeta, abstractmethod
from typing import Union

from pathological.models.game_models import MultiplayerGame


class MultiplayerGameRepository(metaclass=ABCMeta):
    @abstractmethod
    def update_game(self, game: MultiplayerGame):
        pass

    @abstractmethod
    def get_game(self, game_id: str) -> Union[MultiplayerGame, None]:
        pass

    @abstractmethod
    def exists(self, game_id: str):
        pass


class EmbeddedMultiplayerGameRepository(MultiplayerGameRepository):
    def __init__(self):
        self.all_games = {}

    def exists(self, game_id: str):
        return game_id in self.all_games

    def get_game(self, game_id: str):
        return self.all_games.get(game_id, None)

    def update_game(self, game: MultiplayerGame):
        self.all_games[game.game_id] = game
