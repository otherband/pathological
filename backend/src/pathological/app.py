import attrs
from flask import Flask, request, make_response
from flask_cors import CORS
from flask_socketio import SocketIO

from pathological.app_error_handler import register_error_handlers
from pathological.events.WebSocketsEventDispatcher import WebSocketsEventDispatcher
from pathological.events.connections_repository import EmbeddedConnectionRepository, ConnectionRepository
from pathological.game_domain.game_service import GameService
from pathological.game_domain.multiplayer_game_service import MultiplayerGameService
from pathological.images.image_service import ImageService
from pathological.models.game_models import Challenge

SUCCESSFUL_JOIN = "successful_join"

app = Flask(__name__)
CORS(app)
register_error_handlers(app)
app_with_sockets = SocketIO(app, cors_allowed_origins="*")

game_service = GameService()
image_service = ImageService()
event_dispatcher = WebSocketsEventDispatcher()
multiplayer_game_service = MultiplayerGameService(event_dispatcher=event_dispatcher)
connection_repository: ConnectionRepository = EmbeddedConnectionRepository()


def endpoint(suffix):
    return f"/api/v1{suffix}"


@app.route(endpoint("/new-session-id"), methods=["POST"])
def start_session():
    return game_service.register_new_player()


@app.route(endpoint("/request-challenge"), methods=["POST"])
def request_challenge():
    data = request.json
    print(f"Received {data}")
    challenge = game_service.request_challenge(data["player_id"])
    return _to_response(challenge)


@app.route(endpoint("/solve-challenge"), methods=["POST"])
def solve_challenge():
    data = request.json
    game_service.solve_challenge(data["player_id"], data["challenge_id"], data["answer"])
    return '', 200


@app.route(endpoint("/image/<image_id>"))
def get_image(image_id: str):
    response = make_response(image_service.get_image_by_id(image_id=image_id))
    response.headers["Content-Type"] = "image/png"
    return response


@app.route(endpoint("/score/<player_id>"))
def get_score(player_id: str):
    return game_service.get_player_score(player_id)


@app.route(endpoint("/multiplayer/game"), methods=["POST"])
def create_multiplayer_game():
    json = request.json
    game = multiplayer_game_service.create_game(player_id=json["player_id"], game_id=json["game_id"])
    return attrs.asdict(game)


@app.route(endpoint("/multiplayer/game/join"), methods=["PUT"])
def join_multiplayer_game():
    json = request.json
    game = multiplayer_game_service.join_game(game_id=json["game_id"], player_id=json["player_id"])
    return attrs.asdict(game)


@app_with_sockets.on("connect")
def new_connection():
    session_id = get_session_id()
    print(f"New connection established [{session_id}] with data [{request.args}]!")
    connection_repository.add_connection(
        session_id,
        {
            "player_id": request.args["player_id"],
            "game_id": request.args["game_id"]
        }
    )


@app_with_sockets.on("disconnect")
def remove_from_game():
    # noinspection PyUnresolvedReferences
    connection_id = get_session_id()
    print(f"Connection terminated {connection_id}")
    player_data = connection_repository.remove_connection(connection_id)
    multiplayer_game_service.leave_game(game_id=player_data["game_id"],
                                        player_id=player_data["player_id"])


def get_session_id():
    # noinspection PyUnresolvedReferences
    return request.sid


@app.route("/actuator/health")
def health():
    return {
        "status": "UP"
    }


def _to_response(challenge):
    # noinspection PyTypeChecker
    return attrs.asdict(Challenge(challenge_id=challenge.challenge_id,
                                  image_id=challenge.image_id,
                                  correct_answer=challenge.correct_answer,
                                  possible_answers=list(challenge.possible_answers)))


if __name__ == "__main__":
    app_with_sockets.run(app, port=5000, debug=True)
