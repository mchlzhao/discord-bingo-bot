from typing import List, Optional

from src.entities.event import Event
from src.repos.abstract.ievent_repo import IEventRepo
from src.repos.in_memory.data_store import DataStore


class InMemoryEventRepo(IEventRepo):
    def __init__(self, data_store: DataStore):
        self.data_store = data_store

    def create_events(self, game_id: int, event_strs: List[str]) \
            -> List[Event]:
        events = [Event(None, game_id, desc, i, False)
                  for i, desc in enumerate(event_strs)]
        self.data_store.events[game_id] = events
        return events

    def read_all_events(self, game_id: int) -> List[Event]:
        return self.data_store.events[game_id]

    def read_event_by_index(self, game_id: int, index: int) -> Optional[Event]:
        events = self.data_store.events[game_id]
        if index >= len(events):
            return None
        return events[index]

    def read_events_by_desc(self, game_id: int,
                            desc_search_str: str) -> List[Event]:
        results = []
        for event in self.data_store.events[game_id]:
            if desc_search_str in event.desc:
                results.append(event)
        return results

    def update_event(self, game_id: int, event: Event) -> None:
        self.data_store.events[game_id][event.index] = event
