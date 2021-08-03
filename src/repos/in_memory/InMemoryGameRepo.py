from typing import Optional

from src.entities.Game import Game
from src.repos.data_store import game_store


class InMemoryGameRepo:
    def create_game(self, server_id: str) -> Game:
        pass

    def read_active_game(self, server_id: str) -> Optional[Game]:
        pass

    def update_game(self, game: Game) -> None:
        pass
