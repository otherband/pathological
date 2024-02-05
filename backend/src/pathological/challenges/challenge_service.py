from typing import List

from pathological.challenges.challenge_repository import ChallengeRepository
from pathological.models.game_models import Challenge, ChallengeResponse
from pathological.resources_utils import resource_path


class ChallengeService:
    def __init__(self, challenge_repository: ChallengeRepository):
        self._challenge_repository = challenge_repository

    def get_challenge_by(self, challenge_id: str) -> Challenge:
        return self._challenge_repository.get_challenge_by_id(challenge_id)

    def get_random_challenge(self, excluded=None) -> ChallengeResponse:
        challenge = self._challenge_repository.get_random_challenge(excluded)
        return self._to_response(challenge)

    def get_random_batch(self, batch_size: int, excluded=None) -> List[ChallengeResponse]:
        batch = self._challenge_repository.get_random_batch(batch_size, excluded)
        return [self._to_response(challenge) for challenge in batch]

    def evaluate_answer(self, challenge_id: str, player_answer: str) -> bool:
        challenge = self._challenge_repository.get_challenge_by_id(challenge_id)
        return challenge.correct_answer == player_answer

    def get_image_by(self, challenge_id: str) -> bytes:
        challenge = self._challenge_repository.get_challenge_by_id(challenge_id)
        with open(resource_path(challenge.image_path), "rb") as file:
            return file.read()

    def _to_response(self, challenge: Challenge) -> ChallengeResponse:
        return ChallengeResponse(
            challenge_id=challenge.challenge_id,
            possible_answers=list(challenge.possible_answers)
        )
