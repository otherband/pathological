from typing import List

import pandas as pd

from pathological.challenges.challenge_repository import ChallengeRepository
from pathological.datasets.grab_util import grab_dataset_dataframe
from pathological.models.game_models import Challenge


class PandasChallengeRepository(ChallengeRepository):
    def __init__(self, dataset_name: str):
        self._dataframe = grab_dataset_dataframe(dataset_name)

    def get_random_challenge(self, excluded: List[str] = None) -> Challenge:
        without_excluded = self._dataframe.drop(labels=excluded)
        challenge_series = without_excluded.sample(1).iloc[0]
        return self._to_challenge(challenge_series)

    def get_challenge_by_id(self, challenge_id: str) -> Challenge:
        challenge_series = self._dataframe.loc[challenge_id]
        return self._to_challenge(challenge_series)

    def get_random_batch(self, batch_size: int, excluded: List[str] = None) -> List[Challenge]:
        if excluded is None:
            excluded = []
        return [self._to_challenge(series) for series in self._dataframe.drop(excluded).sample(batch_size)]

    def _to_challenge(self, challenge_series: pd.Series):
        return Challenge(challenge_id=str(challenge_series.name),
                         correct_answer=challenge_series['correct_answer'],
                         image_path=challenge_series['image_path'],
                         possible_answers=set(challenge_series['possible_answers'].split(";")))
