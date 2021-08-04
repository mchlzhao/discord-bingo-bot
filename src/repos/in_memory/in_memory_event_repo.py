from typing import List, Optional

from src.entities.event import Event
from src.repos.abstract.ievent_repo import IEventRepo
from src.repos.in_memory.data_store import (
    get_events_from_game, add_events_to_game, update_event_by_index)


class InMemoryEventRepo(IEventRepo):
    def create_events(self, game_id: str, event_strs: List[str]) -> None:
        add_events_to_game(
            game_id, [Event(desc, i, False)
                      for i, desc in enumerate(event_strs)])

    def read_all_events(self, game_id: str) -> List[Event]:
        return get_events_from_game(game_id)

    def read_event_by_index(self, game_id: str, index: int) -> Optional[Event]:
        events = get_events_from_game(game_id)
        if index >= len(events):
            return None
        return events[index]

    def read_events_by_desc(self, game_id: str, desc_search_str: str) \
            -> List[Event]:
        results = []
        for event in get_events_from_game(game_id):
            if desc_search_str in event.desc:
                results.append(event)
        return results

    def update_event(self, game_id: str, event: Event) -> None:
        update_event_by_index(game_id, event)
