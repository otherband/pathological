import json
import unittest

from flask import Response

from pathological.app import app


class AppTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_health(self):
        response = self.app.get("/actuator/health")
        self.assertOkay(response)
        self.assertEqual(response.json["status"], "UP")

    def test_scenario(self):
        session_id_response = self.app.post("/api/v1/new-session-id")
        self.assertOkay(session_id_response)
        player_id = session_id_response.json['player_id']
        self.assertGreater(len(player_id), 10)

        challenge_response = self.post_with_body("api/v1/request-challenge",
                                                 {"player_id": player_id})
        self.assertOkay(challenge_response)
        self.assertTrue("challenge_id" in challenge_response.json)

        solution_response = self.post_with_body("/api/v1/solve-challenge",
                                                {
                                                    "player_id": player_id,
                                                    "challenge_id": challenge_response.json["challenge_id"],
                                                    "answer": "ANY"})
        self.assertOkay(solution_response)

        image_response = self.app.get(f"/api/v1/image/{challenge_response.json['image_id']}")
        self.assertOkay(image_response)
        self.assertEqual(image_response.content_type, "image/png")

        score = self.app.get(f"/api/v1/score/{player_id}")
        self.assertOkay(score)
        self.assertTrue("player_score" in score.json)
        self.assertTrue("player_id" in score.json)

    def post_with_body(self, endpoint: str, body: dict) -> Response:
        return self.app.post(endpoint, data=json.dumps(body),
                             content_type="application/json")

    def assertOkay(self, response: Response):
        self.assertEqual(200, response.status_code)
