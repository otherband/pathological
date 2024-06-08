from attrs import define


class MultiplayerGameEvent:
    pass


@define
class PlayerJoinEvent:
    event_name: str
