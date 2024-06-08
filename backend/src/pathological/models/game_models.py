from typing import Set, List

from attrs import define


@define(frozen=True)
class Challenge:
    challenge_id: str
    image_id: str
    correct_answer: str
    possible_answers: {str}


@define
class PlayerSession:
    player_id: str
    challenges_faced: Set[str]
    challenges_solved: Set[str]
    timestamp_start: float


@define
class MultiplayerGame:
    game_id: str
    connected_players: List[PlayerSession]
    running: bool

    def get_connected_ids(self):
        return [p.player_id for p in self.connected_players]

    def get_truncated_player_objects(self):
        return [{"player_id": p.player_id} for p in self.connected_players]
