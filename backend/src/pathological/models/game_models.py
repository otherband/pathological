from typing import Set, List

from attrs import define


@define(frozen=True)
class Challenge:
    challenge_id: str
    image_id: str
    correct_answer: str
    possible_answers: Set[str]


@define
class PlayerSession:
    player_id: str
    challenges_faced: Set[str]
    challenges_solved: Set[str]
    timestamp_start: float


@define
class MultiplayerPlayerData:
    game_id: str
    player_id: str
    current_challenge_id: str
    current_challenge_options: List[str]
    current_score: int
    challenges_faced: Set[str]

    @classmethod
    def new(cls, game_id: str, player_id: str):
        return MultiplayerPlayerData(
            game_id=game_id,
            player_id=player_id,
            current_challenge_id="",
            current_score=0,
            challenges_faced=set(),
            current_challenge_options=[]
        )


@define
class MultiplayerGame:
    game_id: str
    connected_players: List[MultiplayerPlayerData]
    running: bool

    def get_connected_ids(self):
        return [p.player_id for p in self.connected_players]

    def get_truncated_player_objects(self):
        return [{"player_id": p.player_id} for p in self.connected_players]
