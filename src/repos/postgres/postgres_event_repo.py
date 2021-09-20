from typing import List

from src.entities.event import Event
from src.repos.abstract.ievent_repo import IEventRepo


class PostgresEventRepo(IEventRepo):
    def __init__(self, conn):
        self.conn = conn

    def create_events(self, game_id: int, event_strs: List[str]) \
            -> List[Event]:
        query = '''INSERT INTO GameEvent
                   (game_id, event_desc, index_in_game, is_hit)
                   VALUES '''
        event_tups = [(game_id, desc, index)
                      for index, desc in enumerate(event_strs)]
        cur = self.conn.cursor()
        args = ','.join(cur.mogrify('(%s, %s, %s, FALSE)', event_tup)
                        .decode('utf-8') for event_tup in event_tups)
        cur.execute(query + args + ' RETURNING event_id')
        events = []
        for data in zip(event_tups, cur.fetchall()):
            events.append(
                Event(data[1][0], data[0][0], data[0][1], data[0][2]))
        self.conn.commit()
        return events

    def read_all_events(self, game_id: int) -> List[Event]:
        query = '''SELECT event_id, game_id, event_desc, index_in_game, is_hit
                   FROM GameEvent
                   WHERE game_id = %s'''
        cur = self.conn.cursor()
        cur.execute(query, (game_id,))
        return [Event(*data) for data in cur.fetchall()]

    def update_event(self, game_id: int, event: Event) -> None:
        query = '''UPDATE GameEvent
                   SET event_desc = %s,
                   index_in_game = %s,
                   is_hit = %s
                   WHERE event_id = %s'''
        data = (event.desc, event.index, event.is_hit, event.event_id)
        cur = self.conn.cursor()
        cur.execute(query, data)
        self.conn.commit()
