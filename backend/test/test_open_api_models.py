import unittest

from pathological.open_api.event_models import *


class OpenApiModelsTest(unittest.TestCase):
    """Exists to document behavior and ensure everything open-api-related continues to work as expected"""

    def test_cannot_add_new_properties(self):
        started = GameStarted(game_id="123")
        with self.assertRaises(Exception) as ctx:
            started.non_existent = ""
        self.assertTrue("Object has no attribute 'non_existent'" in str(ctx.exception))

    def test_must_respect_type(self):
        requested = ChallengeRequested(game_id="123")
        with self.assertRaises(Exception) as ctx:
            requested.player_id = 15
        self.assertTrue("Input should be a valid string" in str(ctx.exception))
