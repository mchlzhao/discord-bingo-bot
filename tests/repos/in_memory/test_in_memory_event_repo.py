import unittest

from src.entities.event import Event
from src.repos.in_memory.data_store import DataStore
from src.repos.in_memory.in_memory_event_repo import InMemoryEventRepo


class TestInMemoryEventRepo(unittest.TestCase):
    def setUp(self):
        data_store = DataStore()
        self.event_repo = InMemoryEventRepo(data_store)
        self.game_id = 'test_game'
        self.events = [Event(f'event{i}', i, False) for i in range(11)]
        self.event_repo.create_events(self.game_id,
                                      list(map(lambda x: x.desc, self.events)))

    def assertEventsEqual(self, e1: Event, e2: Event):
        self.assertEqual(e1.desc, e2.desc)
        self.assertEqual(e1.index, e2.index)
        self.assertEqual(e1.is_hit, e2.is_hit)

    def test_read_all(self):
        events = self.event_repo.read_all_events(self.game_id)
        for e_write, e_read in zip(self.events, events):
            self.assertEventsEqual(e_write, e_read)

    def test_read_by_index(self):
        for event in self.events:
            self.assertEventsEqual(self.event_repo.read_event_by_index(
                self.game_id, event.index), event)

    def test_read_by_desc(self):
        events = self.event_repo.read_events_by_desc(self.game_id, '0')
        # should receive 'event0' and 'event10'
        self.assertEqual(len(events), 2)
        self.assertEventsEqual(events[0], self.events[0])
        self.assertEventsEqual(events[1], self.events[10])

    def test_update_event(self):
        new_event = self.events[0]
        new_event.desc += 'new'
        new_event.is_hit = True
        self.event_repo.update_event(self.game_id, new_event)
        self.assertEventsEqual(self.event_repo.read_event_by_index(
            self.game_id, new_event.index), new_event)
