from entities.Event import Event
from entities.EventCombo import EventCombo


class InMemoryEventRepository:
    def __init__(self):
        self.events_
        self.events = [Event(f'Event {i}', i, False) for i in range(12)]
    

