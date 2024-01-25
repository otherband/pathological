import random
import time
import uuid
from typing import Dict

from models.game_models import Challenge, PlayerSession


class GameService:
    def __init__(self):
        self.active_sessions = {}
        self.active_sessions: Dict[str, PlayerSession]
        self.challenges = {
            str(k): Challenge(str(k), str(k), {str(k), "A", "B"}) for k in range(300)
        }

    def register_new_player(self) -> str:
        player_session = PlayerSession(player_id=str(uuid.uuid4()),
                                       images_faced=set(),
                                       images_solved=set(),
                                       timestamp_start=time.time())
        self.active_sessions[player_session.player_id] = player_session
        return player_session.player_id

    def request_challenge(self, player_id) -> Challenge:
        all_choices = list(self.challenges.keys())
        all_choices = [choice for choice in all_choices if choice not in self.active_sessions[player_id].images_faced]
        random_key = random.choice(all_choices)
        self.active_sessions[player_id].images_faced.add(random_key)
        return self._to_response(random_key)

    def solve_challenge(self, player_id: str, challenge_key: str, challenge_answer: str) -> None:
        if challenge_answer == self.challenges[challenge_key].correct_answer:
            self.active_sessions[player_id].images_solved.add(challenge_key)

    def get_player_score(self, player_id: str):
        return len(self.active_sessions[player_id].images_solved)

    def _to_response(self, random_key: str):
        full_challenge = self.challenges[random_key]
        response_challenge = Challenge(full_challenge.challenge_id, "", full_challenge.possible_answers)
        return response_challenge
