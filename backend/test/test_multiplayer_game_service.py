import unittest
from typing import List, Dict

from pathological.exceptions.user_input_exception import UserInputException
from pathological.game_domain.multiplayer_game_service import MultiplayerGameService
from pathological.events.event_dispatcher import EventDispatcher


class DummyEventDispatcher(EventDispatcher):
    def __init__(self):
        self.dispatched_events: List[Dict[str, dict]] = []

    def dispatch(self, event_name: str, event_data: dict) -> None:
        self.dispatched_events.append({
            "event_name": event_name,
            "event_data": event_data,
        })


class MultiplayerGameServiceTest(unittest.TestCase):
    def setUp(self):
        self.event_dispatcher = DummyEventDispatcher()
        self.game_service = MultiplayerGameService(event_dispatcher=self.event_dispatcher)

    def test_create_game(self):
        game = self.game_service.create_game("game_1", "player_1")
        self.assertEquals(["player_1"], game.connected_players)
        with self.assertRaises(UserInputException) as ctx:
            self.game_service.create_game("game_1", "player_2")
        self.assertEquals(ctx.exception.args[0], "Game with ID game_1 already exists.")

    def test_join_game(self):
        game = self.game_service.create_game("game_2", "player_1")
        self.assertEquals(["player_1"], game.connected_players)
        updated_game = self.game_service.join_game("game_2", "player_2")
        self.assertEquals(["player_1", "player_2"], updated_game.connected_players)

        with self.assertRaises(UserInputException) as ctx:
            self.game_service.join_game("game_2", "player_1")
        self.assertEquals(ctx.exception.args[0], "Player 'player_1' has already joined the game 'game_2'.")

        latest_event = self.event_dispatcher.dispatched_events[-1]
        self.assertEquals("player_join_event", latest_event["event_name"])
        self.assertEquals({
            "player_id": "player_2",
            "game_id": "game_2",
            "connected_players": ["player_1", "player_2"]
        }, latest_event["event_data"])

    def test_leave_game(self):
        self.game_service.create_game("game13", "player1")
        self.game_service.join_game("game13", "player2")
        updated_game = self.game_service.leave_game("game13", "player2")
        self.assertEquals(["player1"], updated_game.connected_players)

        latest_event = self.event_dispatcher.dispatched_events[-1]
        self.assertEquals("player_left_game", latest_event["event_name"])
        self.assertEquals({
            "game_id": "game13",
            "player_id": "player2",
            "connected_players": ["player1"]
        }, latest_event["event_data"])
