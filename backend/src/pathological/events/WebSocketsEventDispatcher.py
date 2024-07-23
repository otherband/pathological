from flask import Flask
from flask_socketio import emit
from pathological.open_api.event_models import MultiplayerGameEvent


from pathological.events.event_dispatcher import GameEventDispatcher


class WebSocketsGameEventDispatcher(GameEventDispatcher):

    def __init__(self, flask_app: Flask):
        self._flask_app_context = flask_app.app_context()

    def dispatch(self, event_data: MultiplayerGameEvent) -> None:
        event_name = type(event_data).__name__
        print(f"Emitting event {event_name} with data {event_data}")
        with self._flask_app_context:
            as_dict = event_data.model_dump()
            emit(
                event_name,
                as_dict,
                broadcast=True,
                include_self=True,
                room=event_data.game_id,
                namespace="/"
            )
