from typing import List

from src.entities.combo import Combo


class ComboSet:
    def __init__(self, player_id: str, combos: List[Combo]):
        self.player_id = player_id
        self.combos = combos

    def has_won(self):
        return any(map(lambda combo: combo.has_won(), self.combos))
