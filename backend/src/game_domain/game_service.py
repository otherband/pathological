import random
import time
import uuid

from game_domain.player_repository import EmbeddedPlayerRepository, PlayerRepository
from models.game_models import Challenge, PlayerSession


class GameService:
    def __init__(self, player_repository: PlayerRepository = EmbeddedPlayerRepository()):
        self.player_repository = player_repository
        self.challenges = {
            str(k): Challenge(str(k), str(k), {str(k), "A", "B"}) for k in range(300)
        }

    def register_new_player(self) -> str:
        player = PlayerSession(player_id=str(uuid.uuid4()),
                                       images_faced=set(),
                                       images_solved=set(),
                                       timestamp_start=time.time())
        self.player_repository.add_player_session(player)
        return player.player_id

    def request_challenge(self, player_id) -> Challenge:
        player = self.player_repository.get_player(player_id)
        all_choices = list(self.challenges.keys())
        valid_choices = [choice for choice in all_choices if choice not in player.images_faced]
        random_key = random.choice(valid_choices)
        player.images_faced.add(random_key)
        self.player_repository.update_player(player)
        return self._to_response(random_key)

    def solve_challenge(self, player_id: str, challenge_key: str, challenge_answer: str) -> None:
        player = self.player_repository.get_player(player_id)
        if challenge_answer == self.challenges[challenge_key].correct_answer:
            player.images_solved.add(challenge_key)
            self.player_repository.update_player(player)

    def get_player_score(self, player_id: str):
        return len(self.player_repository.get_player(player_id).images_solved)

    def _to_response(self, random_key: str):
        full_challenge = self.challenges[random_key]
        response_challenge = Challenge(full_challenge.challenge_id, "", full_challenge.possible_answers)
        return response_challenge
