import unittest

from pathological.challenges.pandas_challenge_repo import PandasChallengeRepository
from pathological.models.game_models import Challenge


class PandasRepoTest(unittest.TestCase):
    def setUp(self):
        self.repo = PandasChallengeRepository("dummy")

    def test_get_random(self):
        random_challenge = self.repo.get_random_challenge()
        self.assertTrue(type(random_challenge) is Challenge)

        batch = self.repo.get_random_batch(batch_size=999, excluded=[random_challenge.challenge_id])
        self.assertEqual(999, len(batch))
        self.assertTrue(random_challenge.challenge_id not in
                        [challenge.challenge_id for challenge in batch])

    @unittest.skip
    def test_get_oversize_batch(self):
        batch = self.repo.get_random_batch(batch_size=3000)

    def test_get_challenge_by_id(self):
        challenge = self.repo.get_random_challenge()
        by_id = self.repo.get_challenge_by_id(challenge.challenge_id)
        self.assertEqual(challenge.possible_answers, by_id.possible_answers)
        self.assertEqual(challenge.image_id, by_id.image_id)
        self.assertEqual(challenge.correct_answer, by_id.correct_answer)
