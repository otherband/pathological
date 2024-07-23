from abc import ABCMeta, abstractmethod
from typing import Union

from pathological.models.game_models import MultiplayerGame


class MultiplayerGameRepository(metaclass=ABCMeta):
    @abstractmethod
    def update_game(self, game: MultiplayerGame) -> None:
        pass

    @abstractmethod
    def get_game(self, game_id: str) -> Union[MultiplayerGame, None]:
        pass

    @abstractmethod
    def delete_game(self, game_id: str) -> None:
        pass

    @abstractmethod
    def exists(self, game_id: str) -> bool:
        pass


class EmbeddedMultiplayerGameRepository(MultiplayerGameRepository):

    def __init__(self):
        self.all_games = {}

    def exists(self, game_id: str) -> bool:
        return game_id in self.all_games

    def get_game(self, game_id: str) -> Union[MultiplayerGame, None]:
        return self.all_games.get(game_id, None)

    def update_game(self, game: MultiplayerGame) -> None:
        self.all_games[game.game_id] = game

    def delete_game(self, game_id: str) -> None:
        self.all_games.pop(game_id)
