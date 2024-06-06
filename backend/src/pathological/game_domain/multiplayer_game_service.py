from pathological.events.event_dispatcher import EventDispatcher
from pathological.exceptions.user_input_exception import UserInputException
from pathological.game_domain.multiplayer_game_repository import MultiplayerGameRepository, \
    EmbeddedMultiplayerGameRepository
from pathological.models.game_models import MultiplayerGame


class MultiplayerGameService:
    """Event-based multiplayer game service"""

    def __init__(self,
                 event_dispatcher: EventDispatcher,
                 multiplayer_game_repository: MultiplayerGameRepository = EmbeddedMultiplayerGameRepository()):
        self._game_repository = multiplayer_game_repository
        self._event_dispatcher = event_dispatcher

    def create_game(self, game_id: str, player_id: str):
        if self._exists_by_id(game_id):
            raise UserInputException(f"Game with ID {game_id} already exists.")
        game = MultiplayerGame(game_id=game_id, connected_players=[player_id])
        self._game_repository.update_game(game)
        return game

    def join_game(self, game_id: str, player_id: str):
        if not self._exists_by_id(game_id):
            raise UserInputException(f"Game with ID {game_id} does not exist.")

        game = self._game_repository.get_game(game_id)

        if player_id in game.connected_players:
            raise UserInputException(f"Player '{player_id}' has already joined the game '{game_id}'.")

        game.connected_players.append(player_id)
        self._game_repository.update_game(game)
        self._event_dispatcher.dispatch("player_join_event", {
            "player_id": player_id,
            "game_id": game_id
        })
        return game

    def _exists_by_id(self, game_id) -> bool:
        game = self._game_repository.get_game(game_id=game_id)
        return game is not None
