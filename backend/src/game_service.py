import random
import uuid
from typing import Dict


class PlayerSession:
    def __init__(self):
        self.player_uuid = uuid.uuid4()
        self.images_solved = 0


class Challenge:
    def __init__(self,
                 challenge_id: str,
                 correct_answer: str):
        self.challenge_id = challenge_id
        self.correct_answer = correct_answer


class GameService:
    def __init__(self):
        self.active_sessions = {}
        self.active_sessions: Dict[str, PlayerSession]
        self.challenges = {
            "1": Challenge("1", "1")
        }

    def register_new_player(self) -> uuid.UUID:
        player_session = PlayerSession()
        self.active_sessions[player_session.player_uuid] = player_session
        return player_session.player_uuid

    def request_challenge(self) -> str:
        random_key = random.choice(list(self.challenges.keys()))
        return self.challenges[random_key].challenge_id

    def solve_challenge(self, player_id, challenge_key, challenge_answer) -> None:
        user_correct = (self.challenges[challenge_key].correct_answer == challenge_answer)
        self.active_sessions[player_id].images_solved += user_correct

    def get_player_score(self, player_id):
        return self.active_sessions[player_id].images_solved
