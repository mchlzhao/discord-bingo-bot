from abc import ABC, abstractmethod
from typing import Optional

from src.entities.game import Game


class IGameRepo(ABC):
    @abstractmethod
    def create_game(self, server_id: str) -> Game:
        pass

    @abstractmethod
    def read_active_game(self, server_id: str) -> Optional[Game]:
        pass

    @abstractmethod
    def update_game(self, game: Game) -> None:
        pass
