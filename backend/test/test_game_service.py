import unittest
import uuid

from pathological.game_domain.game_service import GameService

CORRECT_ANSWER = "1"


def wrong_answer() -> str:
    return str(uuid.uuid4())


class GameServiceTest(unittest.TestCase):
    def setUp(self):
        self.game = GameService()

    def test_game(self):
        player = self.game.register_new_player()
        player_id = player['player_id']
        self.assertIsNotNone(player_id)

        correct_answers = 3

        for i in range(correct_answers):
            challenge = self.game.request_challenge(player_id)
            self.game.solve_challenge(player_id, challenge.challenge_id, "death")
        wrong_answers = 10
        for j in range(wrong_answers):
            challenge = self.game.request_challenge(player_id)
            self.game.solve_challenge(player_id, challenge.challenge_id, wrong_answer())

        self.assertEqual(correct_answers + wrong_answers,
                         len(self.game.player_repository.get_player(player_id).challenges_faced))
        self.assertEqual(correct_answers, self.game.get_player_score(player_id)['player_score'])
