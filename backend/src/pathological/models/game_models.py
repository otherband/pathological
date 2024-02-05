from typing import List

from attrs import define


@define(frozen=True)
class Challenge:
    challenge_id: str
    image_path: str
    correct_answer: str
    possible_answers: {str}


@define(frozen=True)
class ChallengeResponse:
    challenge_id: str
    possible_answers: List[str]


@define
class PlayerSession:
    player_id: str
    challenges_faced: {str}
    challenges_solved: {str}
    timestamp_start: float
