from typing import Optional

from src.entities.game import Game
from src.repos.abstract.igame_repo import IGameRepo


class PostgresGameRepo(IGameRepo):
    def create_game(self, server_id: str) -> Game:
        pass

    def read_active_game(self, server_id: str) -> Optional[Game]:
        pass

    def update_game(self, game: Game) -> None:
        pass
