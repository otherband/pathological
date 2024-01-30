import time
import uuid

from pathological.game_domain.challenge_repository import ChallengeRepository, DummyChallengeRepository
from pathological.game_domain.player_repository import EmbeddedPlayerSessionRepository, PlayerSessionRepository
from pathological.models.game_models import Challenge, PlayerSession


class GameService:
    def __init__(self, player_repository: PlayerSessionRepository = EmbeddedPlayerSessionRepository(),
                 challenge_repository: ChallengeRepository = DummyChallengeRepository()):
        self.player_repository = player_repository
        self.challenge_repository = challenge_repository

    def register_new_player(self) -> str:
        player = PlayerSession(player_id=str(uuid.uuid4()),
                               challenges_faced=set(),
                               challenges_solved=set(),
                               timestamp_start=time.time())
        self.player_repository.add_player_session(player)
        return player.player_id

    def request_challenge(self, player_id) -> Challenge:
        player = self.player_repository.get_player(player_id)
        random_challenge = self.challenge_repository.get_random_challenge(excluded=player.challenges_faced)
        player.challenges_faced.add(random_challenge.challenge_id)
        self.player_repository.update_player(player)
        return self._remove_answer(random_challenge)

    def solve_challenge(self, player_id: str, challenge_id: str, player_answer: str) -> None:
        player = self.player_repository.get_player(player_id)
        if player_answer == self._get_answer(challenge_id):
            player.challenges_solved.add(challenge_id)
            self.player_repository.update_player(player)

    def get_player_score(self, player_id: str):
        return len(self.player_repository.get_player(player_id).challenges_solved)

    def _remove_answer(self, challenge: Challenge):
        response_challenge = Challenge(challenge_id=challenge.challenge_id,
                                       correct_answer="",
                                       possible_answers=challenge.possible_answers,
                                       image_id="")
        return response_challenge

    def _get_answer(self, challenge_key):
        return self.challenge_repository.get_challenge_by_id(challenge_key).correct_answer
