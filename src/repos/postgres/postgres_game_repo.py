from typing import Optional

from src.entities.game import Game


class PostgresGameRepo:
    def create_game(self, server_id: str) -> Game:
        pass

    def read_active_game(self, server_id: str) -> Optional[Game]:
        pass

    def update_game(self, game: Game) -> None:
        pass
