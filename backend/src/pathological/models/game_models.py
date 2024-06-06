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
    challenges_faced: {str}
    challenges_solved: {str}
    timestamp_start: float


@define
class MultiplayerGame:
    game_id: str
    connected_players: [str]


@define
class PlayerJoinEvent:
    player_id: str
    game_id: str
