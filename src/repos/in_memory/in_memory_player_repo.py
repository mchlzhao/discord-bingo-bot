from typing import List, Optional

from src.entities.combo_set import ComboSet
from src.entities.entry import Entry
from src.repos.abstract.iplayer_repo import IPlayerRepo
from src.repos.in_memory.data_store import DataStore


class InMemoryPlayerRepo(IPlayerRepo):
    def __init__(self, data_store: DataStore):
        self.data_store = data_store
        self.next_entry_id = 0

    def create_entry(self, game_id: int, combo_set: ComboSet) -> None:
        self.next_entry_id += 1
        self.data_store.entries[game_id][combo_set.player_id] = \
            Entry(self.next_entry_id, game_id, combo_set.player_id, None)
        self.data_store.combo_sets[game_id][combo_set.player_id] = combo_set

    def read_combo_set(self, game_id: int, player_id: str) \
            -> Optional[ComboSet]:
        return self.data_store.combo_sets[game_id][player_id]

    def read_all_combo_sets(self, game_id: int) -> List[ComboSet]:
        return [combo_set
                for combo_set in self.data_store.combo_sets[game_id].values()]

    def read_entry(self, game_id: int, player_id: str) -> Optional[Entry]:
        return self.data_store.entries[game_id].get(player_id, None)

    def read_all_entries(self, game_id: int) -> List[Entry]:
        return self.data_store.entries[game_id].values()

    def update_entry(self, entry: Entry) -> None:
        self.data_store.entries[entry.game_id][entry.player_id] = entry

    def delete_entry(self, game_id: int, player_id: str) -> None:
        try:
            del self.data_store.entries[game_id][player_id]
        except KeyError:
            pass
