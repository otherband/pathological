import os

from attrs import define


@define(frozen=True)
class GameParameters:
    player_session_length_seconds: int
    start_multiplayer_game_delay_seconds: int
    delete_game_after_seconds: int


GAME_PARAMETERS = GameParameters(os.environ.get("PLAYER_SESSION_LENGTH_SECONDS", 60),
                                 os.environ.get("START_MULTIPLAYER_GAME_DELAY_SECONDS", 5),
                                 os.environ.get("DELETE_GAME_AFTER_SECONDS", 60)
                                 )
