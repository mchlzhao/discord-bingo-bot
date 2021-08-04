from datetime import datetime
from typing import Optional

from src.entities.game import Game
from src.repos.in_memory.data_store import DataStore


class InMemoryGameRepo:
    def __init__(self, data_store: DataStore) -> None:
        self.next_game_id = 0
        self.data_store = data_store

    def create_game(self, server_id: str) -> Game:
        self.next_game_id += 1
        game = Game(self.next_game_id, server_id, datetime.now(), None)
        self.data_store.games[game.game_id] = game
        return game

    def read_active_game(self, server_id: str) -> Optional[Game]:
        for game_id, game in self.data_store.games.items():
            if game.server_id == server_id and game.time_finished is None:
                return game
        return None

    def update_game(self, game: Game) -> None:
        self.data_store.games[game.game_id] = game
