from abc import ABC, abstractmethod
from typing import List, Optional

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
    def read_event_by_index(self, game_id: int, index: int) -> Optional[Event]:
        pass

    @abstractmethod
    def read_events_by_desc(self, game_id: int,
                            desc_search_str: str) -> List[Event]:
        pass

    @abstractmethod
    def update_event(self, game_id: int, event: Event) -> None:
        pass
