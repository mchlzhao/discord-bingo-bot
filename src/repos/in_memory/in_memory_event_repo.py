from typing import List

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

    def update_event(self, game_id: int, event: Event) -> None:
        self.data_store.events[game_id][event.index] = event
