from typing import List, Optional, Tuple

from entities.entry import Entry
from entities.event_combo import EventCombo


class InMemoryEntryRepo:
    def create_entry(self, game_id: str, player_id: str,
                     combos: List[EventCombo]) -> None:
        pass

    def read_combos_by_player(self, game_id: str, player_id: str) \
            -> List[EventCombo]:
        pass

    def read_all_combos(self, game_id: str) -> Tuple[str, List[EventCombo]]:
        pass

    def read_entry(self, game_id: str, player_id: str) -> Optional[Entry]:
        pass

    def read_all_entries(self, game_id: str) -> List[Entry]:
        pass

    def update_entries(self, entries: List[Entry]) -> None:
        pass

    def delete_entry(self, game_id: str, player_id: str) -> None:
        pass
