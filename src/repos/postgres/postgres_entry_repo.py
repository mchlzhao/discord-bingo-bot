from typing import List, Optional, Tuple

from src.entites.entry import Entry
from src.entities.combo import Combo


class PostgresEntryRepo:
    def create_entry(self, game_id: str, player_id: str,
                     combos: List[Combo]) -> None:
        pass

    def read_combos_by_player(self, game_id: str, player_id: str) \
            -> List[Combo]:
        pass

    def read_all_combos(self, game_id: str) -> Tuple[str, List[Combo]]:
        pass

    def read_entry(self, game_id: str, player_id: str) -> Optional[Entry]:
        pass

    def read_all_entries(self, game_id: str) -> List[Entry]:
        pass

    def update_entries(self, entries: List[Entry]) -> None:
        pass

    def delete_entry(self, game_id: str, player_id: str) -> None:
        pass
