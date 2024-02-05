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


