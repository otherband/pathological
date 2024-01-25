from attrs import define


@define(frozen=True)
class Challenge:
    challenge_id: str
    correct_answer: str
    possible_answers: {str}


@define
class PlayerSession:
    player_id: str
    images_faced: {str}
    images_solved: {str}
    timestamp_start: float
