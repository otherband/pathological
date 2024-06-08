from flask import Flask
from flask_socketio import emit
from openapi_client.api_response import BaseModel

from pathological.events.event_dispatcher import EventDispatcher


class WebSocketsEventDispatcher(EventDispatcher):

    def dispatch(self, event: BaseModel) -> None:
        event_name = type(event).__name__
        print(f"Emitting event {event_name} with data {event}")
        emit(
            event_name,
            event.dict(),
            broadcast=True,
            include_self=True,
            namespace="/"
        )
