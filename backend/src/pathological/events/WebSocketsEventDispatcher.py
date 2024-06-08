from flask import Flask
from flask_socketio import emit
from openapi_client.api_response import BaseModel

from pathological.events.event_dispatcher import EventDispatcher


class WebSocketsEventDispatcher(EventDispatcher):

    def __init__(self, flask_app: Flask):
        self._flask_app_context = flask_app.app_context()

    def dispatch(self, event_data: BaseModel) -> None:
        event_name = type(event_data).__name__
        print(f"Emitting event {event_name} with data {event_data}")
        with self._flask_app_context:
            emit(
                event_name,
                event_data.dict(),
                broadcast=True,
                include_self=True,
                namespace="/"
            )
