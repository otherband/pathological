import unittest
from typing import List, Dict, Callable

from pathological.events.event_dispatcher import GameEventDispatcher
from pathological.events.task_scheduler import TaskScheduler
from pathological.exceptions.user_input_exception import UserInputException
from pathological.game_domain.multiplayer.multiplayer_game_service import MultiplayerGameService
from pathological.open_api.event_models import MultiplayerGameEvent

CORRECT_ANSWER = "death"

NO_DELAY = -1


class DummyGameEventDispatcher(GameEventDispatcher):

    def __init__(self):
        self.dispatched_events: List[Dict[str, Dict]] = []
        self.latest_delay: int = NO_DELAY

    def dispatch(self, event: MultiplayerGameEvent) -> None:
        self.latest_delay = NO_DELAY
        self.dispatched_events.append({
            "event_name": type(event).__name__,
            "event_data": event.model_dump(),
        })


class TestableMultiplayerGameService(MultiplayerGameService):

    def _get_delay(self):
        return 0


class DummyTaskScheduler(TaskScheduler):
    def __init__(self):
        self.scheduled_tasks: List[callable] = []

    def run_after(self, seconds_delay: int, f: Callable) -> None:
        self.scheduled_tasks.append(f)

    def run_latest(self):
        latest_function = self.scheduled_tasks[-1]
        latest_function()

    def run_all(self):
        for func in self.scheduled_tasks:
            func()


class MultiplayerGameServiceTest(unittest.TestCase):
    def setUp(self):
        self.event_dispatcher = DummyGameEventDispatcher()
        self.task_scheduler = DummyTaskScheduler()
        self.game_service = TestableMultiplayerGameService(event_dispatcher=self.event_dispatcher,
                                                           task_scheduler=self.task_scheduler
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
        self.assertEqual("PlayerJoin", latest_event["event_name"])
        self.assertEqual({
            "player_id": "player_2",
            "game_id": "game_2",
            "event_type": None,
            "connected_players": [{
                "player_id": "player_1",
                "current_score": 0,
                "current_image_id": "",
                "current_challenge_id": "",
                "current_challenge_options": []
            },
                {
                    "player_id": "player_2",
                    "current_score": 0,
                    "current_image_id": "",
                    "current_challenge_id": "",
                    "current_challenge_options": []
                }]
        }, latest_event["event_data"])
        self.assertEqual(NO_DELAY, self.event_dispatcher.latest_delay)

    def test_leave_game(self):
        self.game_service.create_game("game13", "player1")
        self.game_service.join_game("game13", "player2")
        updated_game = self.game_service.leave_game("game13", "player2")
        self.assertEqual(["player1"], updated_game.get_connected_ids())

        latest_event = self._get_latest_event()
        self.assertEqual("PlayerLeft", latest_event["event_name"])
        self.assertEqual({
            "game_id": "game13",
            "player_id": "player2",
            "event_type": None,
            "connected_players": [{"player_id": "player1",
                                   "current_score": 0,
                                   "current_image_id": "",
                                   "current_challenge_id": "",
                                   "current_challenge_options": []
                                   }]
        }, latest_event["event_data"])
        self.assertEqual(NO_DELAY, self.event_dispatcher.latest_delay)

    def test_trigger_start_game(self):
        self.game_service.create_game("game42", "player1")
        self.game_service.trigger_game_starting("game42")
        self.task_scheduler.run_latest()  # run delayed start game task!

        second_to_last = self.event_dispatcher.dispatched_events[-2]

        self.assertEqual("GameStarting", second_to_last["event_name"])
        self.assertEqual({
            "game_id": "game42",
            "event_type": None,
            "connected_players": [{
                "player_id": "player1",
                "current_score": 0,
                "current_image_id": "",
                "current_challenge_id": "",
                "current_challenge_options": []
            }],
            "start_game_delay": 0,
            "message": "Game starting in 0 seconds..."
        }, second_to_last["event_data"])

        last_event = self._get_latest_event()

        self.assertEqual("GameStarted", last_event["event_name"])
        self.assertEqual({
            "game_id": "game42",
            "event_type": None,
            "connected_players": [{
                "player_id": "player1",
                "current_score": 0,
                "current_image_id": "",
                "current_challenge_id": "",
                "current_challenge_options": []
            }],
            "message": "Game started!"
        }, last_event["event_data"])

        self.task_scheduler.run_latest()  # run delayed end game task!

    @unittest.skip
    def test_trigger_start_game_when_game_already_started(self):
        pass

    def test_full_game(self):
        self.game_service.create_game("game_full", "player_1")
        self.game_service.join_game("game_full", "player_2")
        self.game_service.join_game("game_full", "player_3")

        self.game_service.trigger_game_starting("game_full")
        self.task_scheduler.run_latest()  # run started!

        self.game_service.request_first_challenge("game_full", "player_2")
        event = self._get_latest_event()
        self.assertEqual("UpdatePlayersData", event["event_name"])
        self.assertTrue("connected_players" in event["event_data"].keys())
        self.assertTrue(CORRECT_ANSWER in event["event_data"]["connected_players"][1]["current_challenge_options"])

        self.game_service.get_next_challenge("game_full",
                                             "player_2",
                                             CORRECT_ANSWER)
        self.game_service.get_next_challenge("game_full",
                                             "player_2",
                                             CORRECT_ANSWER)
        self.game_service.request_first_challenge("game_full",
                                                  "player_3")
        self.game_service.get_next_challenge("game_full",
                                             "player_3",
                                             CORRECT_ANSWER)

        event = self._get_latest_event()
        self.assertEqual("UpdatePlayersData", event["event_name"])
        self.assertEqual(0, event["event_data"]["connected_players"][0]["current_score"])
        self.assertEqual(2, event["event_data"]["connected_players"][1]["current_score"])
        self.assertEqual(1, event["event_data"]["connected_players"][2]["current_score"])

        self.task_scheduler.run_latest()  # run end game!

        event = self._get_latest_event()
        self.assertEqual("GameEnded", event["event_name"])
        ranked_ = event["event_data"]["players_ranked"]
        self.assertEqual(
            ["player_2", "player_3", "player_1"],
            [p["player_id"] for p in ranked_]
        )

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
