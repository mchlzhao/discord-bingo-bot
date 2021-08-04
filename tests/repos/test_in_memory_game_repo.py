from datetime import datetime
import unittest

from src.repos.in_memory.data_store import clear_game_store
from src.repos.in_memory.in_memory_game_repo import InMemoryGameRepo


class TestInMemoryGameRepo(unittest.TestCase):
    def setUp(self):
        clear_game_store()
        self.game_repo = InMemoryGameRepo()
        self.server_id = 'test_server'
        self.game = self.game_repo.create_game(self.server_id)

    def test_read_active_game(self):
        self.assertEqual(self.game_repo.read_active_game(
            self.server_id).game_id, self.game.game_id)

    def test_no_active_game(self):
        self.game.time_finished = datetime.now()
        self.game_repo.update_game(self.game)
        self.assertIsNone(self.game_repo.read_active_game(self.server_id))

    def test_new_active_game(self):
        self.game.time_finished = datetime.now()
        self.game_repo.update_game(self.game)
        game2 = self.game_repo.create_game(self.server_id)
        self.assertEqual(self.game_repo.read_active_game(
            self.server_id).game_id, game2.game_id)
