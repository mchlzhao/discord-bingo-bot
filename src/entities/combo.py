from typing import List, Optional

from src.entities.event import Event


class Combo:
    def __init__(self, combo_id: Optional[int], events: List[Event],
                 index: int):
        self.combo_id = combo_id
        self.events = events
        self.index = index

    def has_won(self):
        return all(map(lambda event: event.is_hit, self.events))
