import time
import uuid

from pathological.challenges.challenge_repository import PandasChallengeRepository
from pathological.challenges.challenge_service import ChallengeService
from pathological.game_domain.player_repository import EmbeddedPlayerSessionRepository, PlayerSessionRepository
from pathological.models.game_models import PlayerSession, ChallengeResponse


class GameService:
    def __init__(self, player_repository: PlayerSessionRepository = EmbeddedPlayerSessionRepository(),
                 challenge_service: ChallengeService = ChallengeService(PandasChallengeRepository("dummy"))):
        self.player_repository = player_repository
        self.challenge_service = challenge_service

    def register_new_player(self) -> dict:
        player = self._create_new_player()
        self.player_repository.add_player_session(player)
        return {"player_id": player.player_id}

    def request_challenge(self, player_id: str) -> ChallengeResponse:
        player = self.player_repository.get_player(player_id)
        random_challenge = self.challenge_service.get_random_challenge(excluded=player.challenges_faced)
        player.challenges_faced.add(random_challenge.challenge_id)
        self.player_repository.update_player(player)
        return random_challenge

    def solve_challenge(self, player_id: str, challenge_id: str, player_answer: str) -> None:
        player = self.player_repository.get_player(player_id)
        if self.challenge_service.evaluate_answer(challenge_id, player_answer):
            player.challenges_solved.add(challenge_id)
            self.player_repository.update_player(player)

    def get_player_score(self, player_id: str) -> dict:
        return {"player_id": player_id,
                "player_score": self._get_score(player_id)}

    def _create_new_player(self) -> PlayerSession:
        return PlayerSession(player_id=str(uuid.uuid4()),
                             challenges_faced=set(),
                             challenges_solved=set(),
                             timestamp_start=time.time())

    def _get_score(self, player_id: str) -> int:
        return len(self.player_repository.get_player(player_id).challenges_solved)
