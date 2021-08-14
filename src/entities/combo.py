from typing import List

from src.entities.event import Event


class Combo:
    def __init__(self, events: List[Event], index: int):
        self.events = events
        self.index = index

    def has_won(self):
        return all(map(lambda event: event.is_hit, self.events))
