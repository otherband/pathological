from typing import List

from pathological.app_config.game_parameters import GAME_PARAMETERS
from pathological.events.event_dispatcher import EventDispatcher
from pathological.events.task_scheduler import TaskScheduler
from pathological.exceptions.user_input_exception import UserInputException
from pathological.game_domain.challenge_repository import ChallengeRepository, DummyChallengeRepository
from pathological.game_domain.multiplayer.multiplayer_game_repository import MultiplayerGameRepository, \
    EmbeddedMultiplayerGameRepository
from pathological.models.game_models import MultiplayerGame, MultiplayerPlayerData
from pathological.open_api.event_models import *


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
                               connected_players=[MultiplayerPlayerData.new(
                                   player_id=player_id,
                                   game_id=game_id
                               )],
                               running=False)
        self._game_repository.update_game(game)
        return game

    def join_game(self, game_id: str, player_id: str):
        self._verify_exists(game_id)

        game = self._game_repository.get_game(game_id)

        if player_id in [p.player_id for p in game.connected_players]:
            raise UserInputException(f"Name '{player_id}' is already taken in the game '{game_id}'.")

        game.connected_players.append(MultiplayerPlayerData.new(player_id=player_id, game_id=game_id))
        self._game_repository.update_game(game)

        event = PlayerJoin()
        event.player_id = player_id
        event.game_id = game_id
        event.connected_players = self._to_player_data_objects(game)

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
        event.connected_players = self._to_player_data_objects(game)
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
        starting_event.connected_players = self._to_player_data_objects(game)
        starting_event.start_game_delay = delay
        starting_event.message = f"Game starting in {delay} seconds..."

        self._event_dispatcher.dispatch(starting_event)

        self._task_scheduler.run_after(
            seconds_delay=delay,
            f=lambda: self._start_game(game_id)
        )

        return game

    def get_next_challenge(self,
                           game_id: str,
                           player_id: str,
                           answer_to_previous: str):

        game = self._from_verified_pair(game_id, player_id)
        player = [p for p in game.connected_players if p.player_id == player_id][0]

        self._register_previous_answer(player, answer_to_previous)

        challenge = self._challenge_repository.get_random_challenge(excluded=player.challenges_faced)
        player.current_challenge_id = challenge.challenge_id
        player.current_image_id = challenge.image_id
        player.current_challenge_options = list(challenge.possible_answers)
        player.challenges_faced.add(challenge.challenge_id)

        self._game_repository.update_game(game)

        event = UpdatePlayersData()

        event.game_id = game_id
        event.connected_players = self._to_player_data_objects(game)

        self._event_dispatcher.dispatch(event)

    def _register_previous_answer(self, player: MultiplayerPlayerData, answer_to_previous: str):
        if player.current_challenge_id:
            previous_challenge = self._challenge_repository.get_challenge_by_id(player.current_challenge_id)
            if previous_challenge.correct_answer == answer_to_previous:
                player.current_score += 1

    def _get_delay(self) -> int:
        """Override for tests!"""
        return GAME_PARAMETERS.start_multiplayer_game_delay_seconds

    def _start_game(self, game_id: str):
        self._verify_exists(game_id)
        game = self._game_repository.get_game(game_id)

        event = GameStarted()
        event.game_id = game_id
        event.connected_players = self._to_player_data_objects(game)
        event.message = "Game started!"

        self._event_dispatcher.dispatch(event)

    def _to_player_data_objects(self, game: MultiplayerGame) -> List[PlayerData]:
        result = []
        for player in game.connected_players:
            data = PlayerData()
            data.player_id = player.player_id
            data.current_challenge_id = player.current_challenge_id
            data.current_score = player.current_score
            data.current_challenge_options = player.current_challenge_options
            data.current_image_id = player.current_image_id
            result.append(data)
        return result

    def _from_verified_pair(self, game_id: str, player_id: str) -> MultiplayerGame:
        self._verify_exists(game_id)
        game = self._game_repository.get_game(game_id)
        self._verify_player_in(game, game_id, player_id)
        return game

    def _verify_player_in(self, game: MultiplayerGame, game_id: str, player_id: str):
        if player_id not in game.get_connected_ids():
            raise UserInputException(f"Name '{player_id}' is not in the game '{game_id}'.")

    def _verify_exists(self, game_id):
        if not self._game_repository.exists(game_id):
            raise UserInputException(f"Game with ID {game_id} does not exist.")
