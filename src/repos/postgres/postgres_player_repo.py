from typing import List, Optional

from src.entities.combo_set import ComboSet
from src.entities.entry import Entry
from src.repos.abstract.iplayer_repo import IPlayerRepo


class PostgresPlayerRepo(IPlayerRepo):
    def create_entry(self, game_id: str, combo_set: ComboSet) -> None:
        pass

    def read_combo_set(self, game_id: str, player_id: str) -> ComboSet:
        pass

    def read_all_combo_sets(self, game_id: str) -> List[ComboSet]:
        pass

    def read_entry(self, game_id: str, player_id: str) -> Optional[Entry]:
        pass

    def read_all_entries(self, game_id: str) -> List[Entry]:
        pass

    def update_entry(self, entry: Entry) -> None:
        pass

    def delete_entry(self, game_id: str, player_id: str) -> None:
        pass
