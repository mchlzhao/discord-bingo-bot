from abc import ABC, abstractmethod
from typing import List, Optional

from src.entities.combo_set import ComboSet
from src.entities.entry import Entry


class IPlayerRepo(ABC):
    @abstractmethod
    def create_entry(self, game_id: str, combo_set: ComboSet) -> None:
        pass

    @abstractmethod
    def read_combo_set(self, game_id: str, player_id: str) -> ComboSet:
        pass

    @abstractmethod
    def read_all_combo_sets(self, game_id: str) -> List[ComboSet]:
        pass

    @abstractmethod
    def read_entry(self, game_id: str, player_id: str) -> Optional[Entry]:
        pass

    @abstractmethod
    def read_all_entries(self, game_id: str) -> List[Entry]:
        pass

    @abstractmethod
    def update_entry(self, entry: Entry) -> None:
        pass

    @abstractmethod
    def delete_entry(self, game_id: str, player_id: str) -> None:
        pass
