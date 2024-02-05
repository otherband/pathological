import attrs
from flask import Flask, request, make_response
from flask_cors import CORS

from pathological.app_config.app_parameters import APP_PARAMETERS
from pathological.challenges.pandas_challenge_repo import PandasChallengeRepository
from pathological.challenges.challenge_service import ChallengeService
from pathological.game_domain.game_service import GameService

app = Flask(__name__)
CORS(app)
challenge_service = ChallengeService(PandasChallengeRepository(APP_PARAMETERS.dataset_name))
game_service = GameService(challenge_service=challenge_service)


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
    # noinspection PyTypeChecker
    return attrs.asdict(challenge)


@app.route(endpoint("/solve-challenge"), methods=["POST"])
def solve_challenge():
    data = request.json
    game_service.solve_challenge(data["player_id"], data["challenge_id"], data["answer"])
    return '', 200


@app.route(endpoint("/image/<challenge_id>"))
def get_image(challenge_id: str):
    response = make_response(challenge_service.get_image_by(challenge_id=challenge_id))
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


if __name__ == "__main__":
    app.run(port=5000, debug=True)
