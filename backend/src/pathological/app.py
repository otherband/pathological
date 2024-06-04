import attrs
from flask import Flask, request, make_response
from flask_cors import CORS
from flask_socketio import SocketIO, emit

from pathological.game_domain.game_service import GameService
from pathological.game_domain.multiplayer_game_repository import EmbeddedMultiplayerGameRepository
from pathological.images.image_service import ImageService
from pathological.models.game_models import Challenge, MultiplayerGame

app = Flask(__name__)
CORS(app)
game_service = GameService()
image_service = ImageService()
multiplayer_game_repository = EmbeddedMultiplayerGameRepository()
app_with_sockets = SocketIO(app, cors_allowed_origins="*")


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


@app.route("/actuator/health")
def health():
    return {
        "status": "UP"
    }


@app_with_sockets.on("client_join_game")
def client_join_game(event_data: dict):
    requested_game_id = event_data["game_id"]
    game = multiplayer_game_repository.get_game(requested_game_id)
    player = game_service.register_new_named_player(event_data["player_id"])
    if game is None:
        game = MultiplayerGame(game_id=requested_game_id, connected_players=[
            player
        ])
    else:
        print(f"Player {player} joined ")
        game.connected_players.append(player)

    multiplayer_game_repository.update_game(game)

    emit_event(f"successful_join_{requested_game_id}", {
        "game_id": requested_game_id,
        "player_id": player["player_id"]
    })
    emit_event(f"new_player_joined_{requested_game_id}", {
        "game_id": requested_game_id,
        "player_id": player["player_id"]
    })


def emit_event(event_id: str, event_body: dict, namespace="/"):
    print(f"Emitting event {event_id} with body {event_body} ")
    emit(event_id, event_body, namespace=namespace)


def _to_response(challenge):
    # noinspection PyTypeChecker
    return attrs.asdict(Challenge(challenge_id=challenge.challenge_id,
                                  image_id=challenge.image_id,
                                  correct_answer=challenge.correct_answer,
                                  possible_answers=list(challenge.possible_answers)))


if __name__ == "__main__":
    app_with_sockets.run(app, port=5000, debug=True)
