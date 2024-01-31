import unittest

from pathological.app import app


class AppTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_health(self):
        response = self.app.get("/actuator/health")
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.json["status"], "UP")

    def test_game(self):
        session_id_response = self.app.post("/api/v1/new-session-id")
        self.assertEqual(200, session_id_response.status_code)
        self.assertIsNotNone(session_id_response.text)
