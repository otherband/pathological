import attrs
from flask import Flask, request, make_response
from flask_cors import CORS

from pathological.game_domain.game_service import GameService
from pathological.images.image_service import ImageService
from pathological.models.game_models import Challenge

app = Flask(__name__)
CORS(app)
game_service = GameService()
image_service = ImageService()


def endpoint(suffix):
    return f"/api/v1{suffix}"


@app.route(endpoint("/new-session-id"), methods=["POST"])
def start_session():
    return game_service.register_new_player()


@app.route(endpoint("/request-challenge"), methods=["POST"])
def request_challenge():
    data = request.json
    challenge = game_service.request_challenge(data["player_id"])
    return _to_response(challenge)


@app.route(endpoint("/solve-challenge"), methods=["POST"])
def solve_challenge():
    data = request.json
    game_service.solve_challenge(data["player_id"], data["challenge_key"], data["answer"])
    return '', 200


@app.route(endpoint("/image/<image_id>"))
def get_image(image_id: str):
    response = make_response(image_service.get_image_by_id(image_id=image_id))
    response.headers["Content-Type"] = "image/png"
    return response


@app.route(endpoint("/score/<player_id>"))
def get_score(player_id: str):
    score = game_service.get_player_score(player_id)
    return {
        "player_id": player_id,
        "player_score": score
    }


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
    app.run(port=5000, debug=True)
