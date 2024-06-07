import threading

import eventlet

from pathological.app_config.game_parameters import GAME_PARAMETERS
from pathological.events.event_dispatcher import EventDispatcher
from pathological.events.task_scheduler import TaskScheduler
from pathological.exceptions.user_input_exception import UserInputException
from pathological.game_domain.multiplayer_game_repository import MultiplayerGameRepository, \
    EmbeddedMultiplayerGameRepository
from pathological.models.game_models import MultiplayerGame
import socketio


class MultiplayerGameService:
    """Event-based multiplayer game service"""

    def __init__(self,
                 event_dispatcher: EventDispatcher,
                 task_scheduler: TaskScheduler,
                 multiplayer_game_repository: MultiplayerGameRepository = EmbeddedMultiplayerGameRepository(),
                 ):
        self._game_repository = multiplayer_game_repository
        self._event_dispatcher = event_dispatcher
        self._task_scheduler = task_scheduler

    def create_game(self, game_id: str, player_id: str):
        if self._game_repository.exists(game_id):
            raise UserInputException(f"Game with ID {game_id} already exists.")
        game = MultiplayerGame(game_id=game_id,
                               connected_players=[player_id],
                               running=False)
        self._game_repository.update_game(game)
        return game

    def trigger_game_starting(self, game_id: str):
        self._verify_exists(game_id)

        game = self._game_repository.get_game(game_id)
        game.running = True
        self._game_repository.update_game(game)

        delay = self._get_delay()

        self._event_dispatcher.dispatch("game_starting", {
            "game_id": game_id,
            "connected_players": game.connected_players,
            "start_game_delay": delay,
            "message": f"Game starting in {delay} seconds..."
        })

        self._task_scheduler.run_after(
            seconds_delay=delay,
            f=lambda: self._start_game(game_id)
        )

        return game

    def _get_delay(self) -> int:
        """Override for tests!"""
        return GAME_PARAMETERS.start_multiplayer_game_delay_seconds

    def _start_game(self, game_id: str):
        self._verify_exists(game_id)
        game = self._game_repository.get_game(game_id)
        self._event_dispatcher.dispatch(
            "game_started",
            {
                "game_id": game_id,
                "connected_players": game.connected_players,
                "message": "Game started!"
            }
        )

    def _verify_exists(self, game_id):
        if not self._game_repository.exists(game_id):
            raise UserInputException(f"Game with ID {game_id} does not exist.")

    def join_game(self, game_id: str, player_id: str):
        self._verify_exists(game_id)

        game = self._game_repository.get_game(game_id)

        if player_id in game.connected_players:
            raise UserInputException(f"Name '{player_id}' is already taken in the game '{game_id}'.")

        game.connected_players.append(player_id)
        self._game_repository.update_game(game)
        self._event_dispatcher.dispatch("player_join_event", {
            "player_id": player_id,
            "game_id": game_id,
            "connected_players": game.connected_players
        })
        return game

    def leave_game(self, game_id: str, player_id: str):
        if not self._game_repository.exists(game_id):
            raise ValueError(f"Game {game_id} does not exist")

        game = self._game_repository.get_game(game_id)

        if player_id not in game.connected_players:
            raise ValueError(f"Player {player_id} not found in game {game_id}")

        game.connected_players = [p for p in game.connected_players if p != player_id]
        if len(game.connected_players) == 0:
            self._game_repository.delete_game(game_id)
        else:
            self._game_repository.update_game(game)

        self._event_dispatcher.dispatch("player_left_game", {
            "player_id": player_id,
            "game_id": game_id,
            "connected_players": game.connected_players
        })

        return game
