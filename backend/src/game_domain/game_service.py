import time
import uuid

from game_domain.challenge_repository import ChallengeRepository, DummyChallengeRepository
from game_domain.player_repository import EmbeddedPlayerSessionRepository, PlayerSessionRepository
from models.game_models import Challenge, PlayerSession


class GameService:
    def __init__(self, player_repository: PlayerSessionRepository = EmbeddedPlayerSessionRepository(),
                 challenge_repository: ChallengeRepository = DummyChallengeRepository()):
        self.player_repository = player_repository
        self.challenge_repository = challenge_repository

    def register_new_player(self) -> str:
        player = PlayerSession(player_id=str(uuid.uuid4()),
                               images_faced=set(),
                               images_solved=set(),
                               timestamp_start=time.time())
        self.player_repository.add_player_session(player)
        return player.player_id

    def request_challenge(self, player_id) -> Challenge:
        player = self.player_repository.get_player(player_id)
        random_challenge = self.challenge_repository.get_random_challenge(excluded=player.images_faced)
        player.images_faced.add(random_challenge.challenge_id)
        self.player_repository.update_player(player)
        return self._to_response(random_challenge)

    def solve_challenge(self, player_id: str, challenge_key: str, challenge_answer: str) -> None:
        player = self.player_repository.get_player(player_id)
        if challenge_answer == self.challenge_repository.get_challenge_by_id(challenge_key).correct_answer:
            player.images_solved.add(challenge_key)
            self.player_repository.update_player(player)

    def get_player_score(self, player_id: str):
        return len(self.player_repository.get_player(player_id).images_solved)

    def _to_response(self, challenge: Challenge):
        response_challenge = Challenge(challenge.challenge_id, "", challenge.possible_answers)
        return response_challenge
