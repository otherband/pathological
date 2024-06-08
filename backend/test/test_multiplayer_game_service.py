import unittest
from typing import List, Dict, Callable

from pathological.events.event_dispatcher import EventDispatcher
from pathological.events.task_scheduler import TaskScheduler
from pathological.exceptions.user_input_exception import UserInputException
from pathological.game_domain.multiplayer_game_service import MultiplayerGameService

NO_DELAY = -1


class DummyEventDispatcher(EventDispatcher):

    def __init__(self):
        self.dispatched_events: List[Dict[str, dict]] = []
        self.latest_delay: int = NO_DELAY

    def dispatch(self, event_name: str, event_data: dict) -> None:
        self.latest_delay = NO_DELAY
        self.dispatched_events.append({
            "event_name": event_name,
            "event_data": event_data,
        })


class TestableMultiplayerGameService(MultiplayerGameService):
    def _get_delay(self):
        return 0


class DummyTaskScheduler(TaskScheduler):

    def run_after(self, seconds_delay: int, f: Callable) -> None:
        f()


class MultiplayerGameServiceTest(unittest.TestCase):
    def setUp(self):
        self.event_dispatcher = DummyEventDispatcher()
        self.game_service = TestableMultiplayerGameService(event_dispatcher=self.event_dispatcher,
                                                           task_scheduler=DummyTaskScheduler()
                                                           )

    def test_create_game(self):
        game = self.game_service.create_game("game_1", "player_1")
        self.assertEqual(["player_1"], game.get_connected_ids())
        with self.assertRaises(UserInputException) as ctx:
            self.game_service.create_game("game_1", "player_2")
        self.assertEqual(ctx.exception.args[0], "Game with ID game_1 already exists.")

    def test_join_game(self):
        game = self.game_service.create_game("game_2", "player_1")
        self.assertEqual(["player_1"], game.get_connected_ids())
        updated_game = self.game_service.join_game("game_2", "player_2")
        self.assertEqual(["player_1", "player_2"], updated_game.get_connected_ids())

        with self.assertRaises(UserInputException) as ctx:
            self.game_service.join_game("game_2", "player_1")
        self.assertEqual(ctx.exception.args[0], "Name 'player_1' is already taken in the game 'game_2'.")

        latest_event = self._get_latest_event()
        self.assertEqual("player_join_event", latest_event["event_name"])
        self.assertEqual({
            "player_id": "player_2",
            "game_id": "game_2",
            "connected_players": ["player_1", "player_2"]
        }, latest_event["event_data"])
        self.assertEqual(NO_DELAY, self.event_dispatcher.latest_delay)

    def test_leave_game(self):
        self.game_service.create_game("game13", "player1")
        self.game_service.join_game("game13", "player2")
        updated_game = self.game_service.leave_game("game13", "player2")
        self.assertEqual(["player1"], updated_game.get_connected_ids())

        latest_event = self._get_latest_event()
        self.assertEqual("player_left_game", latest_event["event_name"])
        self.assertEqual({
            "game_id": "game13",
            "player_id": "player2",
            "connected_players": ["player1"]
        }, latest_event["event_data"])
        self.assertEqual(NO_DELAY, self.event_dispatcher.latest_delay)

    def test_trigger_start_game(self):
        self.game_service.create_game("game42", "player1")
        self.game_service.trigger_game_starting("game42")

        second_to_last = self.event_dispatcher.dispatched_events[-2]

        self.assertEqual("game_starting", second_to_last["event_name"])
        self.assertEqual({
            "game_id": "game42",
            "connected_players": ["player1"],
            "start_game_delay": 0,
            "message": "Game starting in 0 seconds..."
        }, second_to_last["event_data"])

        last_event = self._get_latest_event()

        self.assertEqual("game_started", last_event["event_name"])
        self.assertEqual({
            "game_id": "game42",
            "connected_players": ["player1"],
            "message": "Game started!"
        }, last_event["event_data"])

    def full_game(self):
        game = self.game_service.create_game("game_full", "player_1")

        self.game_service.join_game("game_full", "player_2")
        self.game_service.join_game("game_full", "player_3")

        self.game_service.trigger_game_starting("game_full")

        self.game_service.request_challenge("game_full", "player_1")
        event = self._get_latest_event()
        self.assertEqual("challenge_requested", event["event_name"])
        self.assertEqual("player_1", event["event_data"]["player_id"])
        self.assertEqual("game_full", event["event_data"]["game_id"])
        self.assertTrue("challenge_id" in event["event_data"].keys())

        self.game_service.submit_answer("game_full", "player_1", event["event_data"]["challenge_id"])

        event = self._get_latest_event()
        self.assertEqual("answer_submitted", event["event_name"])
        self.assertEqual({
            "player_1": 1,
            "player_2": 0,
            "player_3": 0
        }, event["event_data"]["players_scores"])
        self.assertTrue("players_current_challenges" in event["event_data"].keys())

    def _get_latest_event(self):
        latest_event = self.event_dispatcher.dispatched_events[-1]
        return latest_event

    @unittest.skip
    def test_all_players_leave_while_game_starting(self):
        """We should gracefully handle multi-threading scenarios"""
        pass

    @unittest.skip
    def test_cannot_join_running_game(self):
        pass
