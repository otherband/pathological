import random
from abc import ABCMeta, abstractmethod
from typing import List

from pathological.models.game_models import Challenge


class ChallengeRepository(metaclass=ABCMeta):
    @abstractmethod
    def get_random_challenge(self, excluded: List[str] = None) -> Challenge:
        pass

    @abstractmethod
    def get_challenge_by_id(self, challenge_id: str) -> Challenge:
        pass

    @abstractmethod
    def get_random_batch(self, batch_size: int, excluded: List[str] = None) -> List[Challenge]:
        pass


class DummyChallengeRepository(ChallengeRepository):
    def __init__(self):
        self._challenges = {
            str(k): Challenge(challenge_id=str(k),
                              image_path=random.choice(["path1.jpeg", "path2.png"]),
                              correct_answer="death",
                              possible_answers={"death", "double death", "triple death"})
            for k in range(300)
        }

    def get_random_batch(self, batch_size: int, excluded: List[str] = None) -> List[Challenge]:
        if excluded is None:
            excluded = []
        valid_ids = [choice for choice in self._all_ids() if choice not in excluded]
        id_batch = random.sample(population=valid_ids, k=batch_size)
        return [self._challenges[challenge_id] for challenge_id in id_batch]

    def get_random_challenge(self, excluded: List[str] = None) -> Challenge:
        if excluded is None:
            excluded = []
        valid_ids = [choice for choice in self._all_ids() if choice not in excluded]
        return self._challenges[random.choice(valid_ids)]

    def get_challenge_by_id(self, challenge_id: str):
        return self._challenges[challenge_id]

    def _all_ids(self):
        return list(self._challenges.keys())
