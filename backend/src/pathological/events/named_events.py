from typing import List

from attrs import define

from pathological.models.game_models import PlayerSession


class MultiplayerGameEvent:
    pass


@define
class BasicPlayerData:
    player_id: str


@define
class GameStarting(MultiplayerGameEvent):
    game_id: str
    connected_players: List[BasicPlayerData]
    start_game_delay: int
    message: str


@define
class GameStarted(MultiplayerGameEvent):
    game_id: str
    connected_players: List[BasicPlayerData]
    message: str


@define
class ChallengeRequested(MultiplayerGameEvent):
    player_id: str
    challenge_id: str


@define
class PlayerJoin(MultiplayerGameEvent):
    player_id: str
    game_id: str
    connected_players: List[BasicPlayerData]
