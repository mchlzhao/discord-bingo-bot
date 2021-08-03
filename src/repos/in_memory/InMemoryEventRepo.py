from typing import List, Optional

from entities.Event import Event
from repos.abstract.IEventRepo import IEventRepo
from repos.in_memory.data_store import game_store


class InMemoryEventRepo(IEventRepo):
    def create_events(self, game_id: str, event_strs: List[str]) -> None:
        pass

    def read_all_events(self, game_id: str) -> List[Event]:
        pass

    def read_event_by_index(self, game_id: str, index: int) -> Optional[Event]:
        pass

    def read_event_by_desc(self, game_id: str, desc_search_str: str) \
            -> Optional[Event]:
        pass

    def update_event(self, Event) -> None:
        pass
