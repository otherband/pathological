import time

from pathological.app_config.game_parameters import GAME_PARAMETERS
from pathological.events.event_dispatcher import EventDispatcher
from pathological.events.task_scheduler import TaskScheduler
from pathological.exceptions.user_input_exception import UserInputException
from pathological.game_domain.challenge_repository import ChallengeRepository, DummyChallengeRepository
from pathological.game_domain.multiplayer.multiplayer_game_repository import MultiplayerGameRepository, \
    EmbeddedMultiplayerGameRepository
from pathological.models.game_models import MultiplayerGame, PlayerSession
from openapi_client.models.game_starting import GameStarting
from openapi_client.models.challenge_requested import ChallengeRequested
from openapi_client.models.player_join import PlayerJoin
from openapi_client.models.player_left import PlayerLeft
from openapi_client.models.game_started import GameStarted
from openapi_client.models.submit_answer import SubmitAnswer


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

    def join_game(self, game_id: str, player_id: str):
        self._verify_exists(game_id)

        game = self._game_repository.get_game(game_id)

        if player_id in [p.player_id for p in game.connected_players]:
            raise UserInputException(f"Name '{player_id}' is already taken in the game '{game_id}'.")

        game.connected_players.append(PlayerSession(
            challenges_solved=set(),
            challenges_faced=set(),
            player_id=player_id,
            timestamp_start=time.time()
        ))
        self._game_repository.update_game(game)

        event = PlayerJoin()
        event.player_id = player_id
        event.game_id = game_id
        event.connected_players = game.get_truncated_player_objects()

        self._event_dispatcher.dispatch(event)
        return game

    def leave_game(self, game_id: str, player_id: str):
        game = self._from_verified_pair(game_id=game_id, player_id=player_id)

        game.connected_players = [p for p in game.connected_players if p.player_id != player_id]
        if len(game.connected_players) == 0:
            self._game_repository.delete_game(game_id)
        else:
            self._game_repository.update_game(game)

        event = PlayerLeft()
        event.player_id = player_id
        event.game_id = game_id
        event.connected_players = game.get_truncated_player_objects()
        self._event_dispatcher.dispatch(event)

        return game

    def trigger_game_starting(self, game_id: str):
        self._verify_exists(game_id)

        game = self._game_repository.get_game(game_id)
        game.running = True
        self._game_repository.update_game(game)

        delay = self._get_delay()

        starting_event = GameStarting()
        starting_event.game_id = game_id
        starting_event.connected_players = game.get_truncated_player_objects()
        starting_event.start_game_delay = delay
        starting_event.message = f"Game starting in {delay} seconds..."

        self._event_dispatcher.dispatch(starting_event)

        self._task_scheduler.run_after(
            seconds_delay=delay,
            f=lambda: self._start_game(game_id)
        )

        return game

    def get_challenge(self, game_id: str, player_id: str):
        game = self._from_verified_pair(game_id, player_id)

        player = [p for p in game.connected_players if p.player_id == player_id][0]
        challenge = self._challenge_repository.get_random_challenge(excluded=player.challenges_faced)

        event = ChallengeRequested()
        event.player_id = player_id
        event.game_id = game_id
        event.challenge_id = challenge.challenge_id
        self._event_dispatcher.dispatch(event)

    def submit_answer(self, game_id: str, player_id: str, challenge_id: str):
        event = SubmitAnswer()
        event.game_id = game_id
        event.player_id = player_id
        event.challenge_id = challenge_id
        self._event_dispatcher.dispatch(event)

    def _get_delay(self) -> int:
        """Override for tests!"""
        return GAME_PARAMETERS.start_multiplayer_game_delay_seconds

    def _start_game(self, game_id: str):
        self._verify_exists(game_id)
        game = self._game_repository.get_game(game_id)

        event = GameStarted()
        event.game_id = game_id
        event.connected_players = game.get_truncated_player_objects()
        event.message = "Game started!"

        self._event_dispatcher.dispatch(event)

    def _from_verified_pair(self, game_id: str, player_id: str) -> MultiplayerGame:
        self._verify_exists(game_id)
        game = self._game_repository.get_game(game_id)
        self._verify_player_in(game, game_id, player_id)
        return game

    def _verify_player_in(self, game, game_id, player_id):
        if player_id not in game.get_connected_ids():
            raise UserInputException(f"Name '{player_id}' is not in the game '{game_id}'.")

    def _verify_exists(self, game_id):
        if not self._game_repository.exists(game_id):
            raise UserInputException(f"Game with ID {game_id} does not exist.")
