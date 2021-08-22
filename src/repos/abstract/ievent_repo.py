from abc import ABC, abstractmethod
from typing import List

from src.entities.event import Event


class IEventRepo(ABC):
    @abstractmethod
    def create_events(self, game_id: int, event_strs: List[str]) \
            -> List[Event]:
        pass

    @abstractmethod
    def read_all_events(self, game_id: int) -> List[Event]:
        pass

    @abstractmethod
    def update_event(self, game_id: int, event: Event) -> None:
        pass
