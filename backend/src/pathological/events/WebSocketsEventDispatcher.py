from pathological.events.event_dispatcher import EventDispatcher
from flask_socketio import SocketIO, emit


class WebSocketsEventDispatcher(EventDispatcher):
    def dispatch(self, event_name: str,
                 event_data: dict) -> None:
        emit(
            event=event_name,
            event_data=event_data,
            broadcast=True,
            include_self=True
        )
