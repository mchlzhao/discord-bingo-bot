import unittest

from src.core.game_engine import GameEngine
from src.repos.in_memory.data_store import DataStore
from src.repos.in_memory.in_memory_event_repo import InMemoryEventRepo
from src.repos.in_memory.in_memory_game_repo import InMemoryGameRepo
from src.repos.in_memory.in_memory_player_repo import InMemoryPlayerRepo


class TestInMemoryIntegration(unittest.TestCase):
    def setUp(self):
        data_store = DataStore()
        self.event_repo = InMemoryEventRepo(data_store)
        self.game_repo = InMemoryGameRepo(data_store)
        self.player_repo = InMemoryPlayerRepo(data_store)
        self.game_engine = GameEngine(
            self.event_repo, self.game_repo, self.player_repo)

        self.server_id = 'server0'
        self.player_id = 'player0'

    def test_start_game(self):
        self.game_engine.start_game(
            self.server_id,
            [f'event {i}' for i in range(11)])
        self.assertIsNotNone(self.game_repo.read_active_game(self.server_id))

    def test_finish_game(self):
        self.game_engine.start_game(
            self.server_id,
            [f'event {i}' for i in range(11)])
        self.game_engine.finish_game(self.server_id)
        self.assertIsNone(self.game_repo.read_active_game(self.server_id))

    def test_set_entry(self):
        self.game_engine.start_game(
            self.server_id,
            [f'event {i}' for i in range(11)])
        self.game_engine.set_entry(self.server_id, self.player_id,
                                   [[0, 1, 2], [3, 4, 5]])

    def test_bingo(self):
        self.game_engine.start_game(
            self.server_id,
            [f'event {i}' for i in range(11)])
        self.game_engine.set_entry(self.server_id, self.player_id,
                                   [[0, 1, 2], [3, 4, 5]])
        self.game_engine.change_hit(self.server_id, True, index=0)
        response = self.game_engine.bingo(self.server_id, self.player_id)
        self.assertIsNotNone(response.display_error)

        self.game_engine.change_hit(self.server_id, True, index=1)
        response = self.game_engine.bingo(self.server_id, self.player_id)
        self.assertIsNotNone(response.display_error)

        self.game_engine.change_hit(self.server_id, True, index=2)
        response = self.game_engine.bingo(self.server_id, self.player_id)
        self.assertIsNone(response.display_error)
