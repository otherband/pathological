import unittest
import uuid

from game_service import GameService

CORRECT_ANSWER = "1"


def wrong_answer() -> str:
    return str(uuid.uuid4())


class GameServiceTest(unittest.TestCase):
    def setUp(self):
        self.game = GameService()

    def test_game(self):
        player_id = self.game.register_new_player()
        self.assertIsNotNone(player_id)

        challenge_id = self.game.request_challenge()
        correct_answers = 3
        for i in range(correct_answers):
            self.game.solve_challenge(player_id, challenge_id, CORRECT_ANSWER)
        self.game.solve_challenge(player_id, challenge_id, wrong_answer())
        self.game.solve_challenge(player_id, challenge_id, wrong_answer())

        self.assertEqual(correct_answers, self.game.get_player_score(player_id))
