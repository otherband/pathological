import time

from pathological.app_config.game_parameters import GAME_PARAMETERS
from pathological.events.event_dispatcher import EventDispatcher
from pathological.events.task_scheduler import TaskScheduler
from pathological.exceptions.user_input_exception import UserInputException
from pathological.game_domain.challenge_repository import ChallengeRepository, DummyChallengeRepository
from pathological.game_domain.multiplayer_game_repository import MultiplayerGameRepository, \
    EmbeddedMultiplayerGameRepository
from pathological.models.game_models import MultiplayerGame, PlayerSession


class MultiplayerGameService:
    """Event-based multiplayer game service"""

    def __init__(self,
                 event_dispatcher: EventDispatcher,
                 task_scheduler: TaskScheduler,
                 challenge_repository: ChallengeRepository = DummyChallengeRepository(),
                 multiplayer_game_repository: MultiplayerGameRepository = EmbeddedMultiplayerGameRepository(),
                 ):
        self._game_repository = multiplayer_game_repository
        self._event_dispatcher = event_dispatcher
        self._task_scheduler = task_scheduler
        self._challenge_repository = challenge_repository

    def create_game(self, game_id: str, player_id: str):
        if self._game_repository.exists(game_id):
            raise UserInputException(f"Game with ID {game_id} already exists.")
        game = MultiplayerGame(game_id=game_id,
                               connected_players=[PlayerSession(
                                   player_id=player_id,
                                   timestamp_start=time.time(),
                                   challenges_faced=set(),
                                   challenges_solved=set()
                               )],
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
            "connected_players": game.get_connected_ids(),
            "start_game_delay": delay,
            "message": f"Game starting in {delay} seconds..."
        })

        self._task_scheduler.run_after(
            seconds_delay=delay,
            f=lambda: self._start_game(game_id)
        )

        return game

    def request_challenge(self, game_id: str, player_id: str):
        self._verify_exists(game_id)
        game = self._game_repository.get_game(game_id)
        self._verify_player_in_game(game, game_id, player_id)

        player = [p for p in game.connected_players if p.player_id == player_id][0]
        challenge = self._challenge_repository.get_random_challenge(excluded=player.challenges_faced)
        self._event_dispatcher.dispatch(
            "challenge_requested", {
                "player_id": player_id,
                "challenge_id": challenge.challenge_id,
                "": ""
            }
        )

    def submit_answer(self, game_id: str, player_id: str, challenge_id: str):
        pass

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
                "connected_players": game.get_connected_ids(),
                "message": "Game started!"
            }
        )

    def _verify_exists(self, game_id):
        if not self._game_repository.exists(game_id):
            raise UserInputException(f"Game with ID {game_id} does not exist.")

    def join_game(self, game_id: str, player_id: str):
        self._verify_exists(game_id)

        game = self._game_repository.get_game(game_id)

        self._verify_player_in_game(game, game_id, player_id)

        game.connected_players.append(PlayerSession(
            challenges_solved=set(),
            challenges_faced=set(),
            player_id=player_id,
            timestamp_start=time.time()
        ))
        self._game_repository.update_game(game)
        self._event_dispatcher.dispatch("player_join_event", {
            "player_id": player_id,
            "game_id": game_id,
            "connected_players": game.get_connected_ids()
        })
        return game

    def _verify_player_in_game(self, game, game_id, player_id):
        if player_id in [p.player_id for p in game.connected_players]:
            raise UserInputException(f"Name '{player_id}' is already taken in the game '{game_id}'.")

    def leave_game(self, game_id: str, player_id: str):
        if not self._game_repository.exists(game_id):
            raise ValueError(f"Game {game_id} does not exist")

        game = self._game_repository.get_game(game_id)

        if player_id not in game.get_connected_ids():
            raise ValueError(f"Player {player_id} not found in game {game_id}")

        game.connected_players = [p for p in game.connected_players if p.player_id != player_id]
        if len(game.connected_players) == 0:
            self._game_repository.delete_game(game_id)
        else:
            self._game_repository.update_game(game)

        self._event_dispatcher.dispatch("player_left_game", {
            "player_id": player_id,
            "game_id": game_id,
            "connected_players": game.get_connected_ids()
        })

        return game
