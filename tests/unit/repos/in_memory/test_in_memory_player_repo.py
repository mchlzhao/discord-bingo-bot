import unittest

from src.repos.in_memory.data_store import DataStore
from src.repos.in_memory.in_memory_player_repo import InMemoryPlayerRepo


class TestInMemoryPlayerRepo(unittest.TestCase):
    def setUp(self):
        data_store = DataStore()
        self.player_repo = InMemoryPlayerRepo(data_store)
