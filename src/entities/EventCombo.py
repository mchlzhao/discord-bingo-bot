from typing import List

from entities.Event import Event


class EventCombo:
    def __init__(self, events: List[Event]):
        self.events = events

    def has_won(self):
        return all(map(lambda x: x.is_hit, self.events))
