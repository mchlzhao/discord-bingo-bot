from typing import List, Optional

from entities.Event import Event
from repos.abstract.IEventRepo import IEventRepo
from repos.in_memory.data_store import game_store


class InMemoryEventRepo(IEventRepo):
    def create_events(self, game_id: str, event_strs: List[str]) -> None:
        game_store[game_id]['events'].extend(
            [Event(desc, i, False) for i, desc in enumerate(event_strs)]
        )

    def read_all_events(self, game_id: str) -> List[Event]:
        return game_store[game_id]['events']

    def read_event_by_index(self, game_id: str, index: int) -> Optional[Event]:
        events = game_store[game_id]['events']
        if index >= len(events):
            return None
        return events[index]

    def read_events_by_desc(self, game_id: str, desc_search_str: str) \
            -> List[Event]:
        results = []
        for event in game_store[game_id]['events']:
            if desc_search_str in event.desc:
                results.append(event)
        return results

    def update_event(self, game_id: str, event: Event) -> None:
        game_store[game_id]['events'][event.index] = event
