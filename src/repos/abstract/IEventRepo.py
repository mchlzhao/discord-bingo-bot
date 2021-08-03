from abc import ABC, abstractmethod
from typing import List, Optional

from entities.Event import Event


class IEventRepo(ABC):
    @abstractmethod
    def create_events(self, game_id: str, event_strs: List[str]) -> None:
        pass

    @abstractmethod
    def read_events(self, game_id: str) -> List[Event]:
        pass

    @abstractmethod
    def read_event_by_index(self, game_id: str, index: int) -> Optional[Event]:
        pass

    @abstractmethod
    def read_event_by_desc(self, game_id: str, desc_search_str: str) \
            -> Optional[Event]:
        pass

    @abstractmethod
    def update_event(self, Event) -> None:
        pass
