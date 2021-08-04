from typing import List, Optional

from entities.event import Event
from repos.abstract.ievent_repo import IEventRepo


class PostgresEventRepo(IEventRepo):
    def create_events(self, game_id: str, event_strs: List[str]) -> None:
        pass

    def read_all_events(self, game_id: str) -> List[Event]:
        pass

    def read_event_by_index(self, game_id: str, index: int) -> Optional[Event]:
        pass

    def read_events_by_desc(self, game_id: str, desc_search_str: str) \
            -> List[Event]:
        pass

    def update_event(self, game_id: str, event: Event) -> None:
        pass
