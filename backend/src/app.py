import attrs
from flask import Flask, request
from flask_cors import CORS

from game_domain.game_service import GameService
from models.game_models import Challenge

app = Flask(__name__)
CORS(app)
game_service = GameService()


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
    return game_service.solve_challenge(data["player_id"], data["challenge_key"], data["answer"])


def _to_response(challenge):
    # noinspection PyTypeChecker
    return attrs.asdict(Challenge(challenge_id=challenge.challenge_id, correct_answer=challenge.correct_answer,
                                  possible_answers=list(challenge.possible_answers)))


if __name__ == "__main__":
    app.run(port=5000, debug=True)
