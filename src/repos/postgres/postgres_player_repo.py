from collections import defaultdict
from typing import List, Optional, Tuple

from src.entities.combo import Combo
from src.entities.combo_set import ComboSet
from src.entities.entry import Entry
from src.entities.event import Event
from src.repos.abstract.iplayer_repo import IPlayerRepo


def create_combo_set(game_id: int, player_id: str, entries: Tuple) -> ComboSet:
    # data = [(combo.combo_id, combo.index_in_entry, gameevent.event_id,
    #         event_desc, index_in_game, is_hit
    combo_infos = list(dict.fromkeys(
        map(lambda x: x[:2], entries)
    ))
    combo_set = ComboSet(player_id, [
        Combo(info[0], [], info[1]) for info in combo_infos])
    for data in entries:
        combo_set.combos[data[1]].events.append(
            Event(data[2], game_id, data[3], data[4], data[5]))
    return combo_set


class PostgresPlayerRepo(IPlayerRepo):
    def __init__(self, conn):
        self.conn = conn

    def create_entry(self, game_id: int, combo_set: ComboSet) -> None:
        # TODO: optimise this function
        query1 = '''INSERT INTO GameEntry (game_id, player_id, time_won)
                    VALUES (%s, %s, NULL)
                    RETURNING entry_id'''
        data1 = (game_id, combo_set.player_id)
        cur = self.conn.cursor()
        cur.execute(query1, data1)
        entry_id = cur.fetchone()[0]
        for combo_index, combo in enumerate(combo_set.combos):
            query2 = '''INSERT INTO Combo (entry_id, index_in_entry)
                        VALUES (%s, %s)
                        RETURNING combo_id'''
            data2 = (entry_id, combo_index)
            cur.execute(query2, data2)
            combo.combo_id = cur.fetchone()[0]
            for event in combo.events:
                query3 = '''INSERT INTO EventInCombo
                            (combo_id, event_id, index_in_combo)
                            VALUES (%s, %s, %s)'''
                data3 = (combo.combo_id, event.event_id, event.index)
                cur.execute(query3, data3)
        self.conn.commit()

    def read_combo_set(self, game_id: int, player_id: str) \
            -> Optional[ComboSet]:
        query = '''SELECT combo.combo_id, combo.index_in_entry,
                   gameevent.event_id, event_desc, index_in_game, is_hit
                   FROM gameentry
                   JOIN combo ON gameentry.entry_id = combo.entry_id
                   JOIN eventincombo ON combo.combo_id = eventincombo.combo_id
                   JOIN gameevent ON eventincombo.event_id = gameevent.event_id
                   WHERE gameentry.game_id = %s
                   AND player_id = %s
                   ORDER BY (combo.entry_id, index_in_entry, index_in_combo)'''
        data = (game_id, player_id)
        cur = self.conn.cursor()
        cur.execute(query, data)
        results = cur.fetchall()
        if results is None:
            return None
        return create_combo_set(game_id, player_id, results)

    def read_all_combo_sets(self, game_id: int) -> List[ComboSet]:
        query = '''SELECT player_id, combo.combo_id, combo.index_in_entry,
                   gameevent.event_id, event_desc, index_in_game, is_hit
                   FROM gameentry
                   JOIN combo ON gameentry.entry_id = combo.entry_id
                   JOIN eventincombo ON combo.combo_id = eventincombo.combo_id
                   JOIN gameevent ON eventincombo.event_id = gameevent.event_id
                   WHERE gameentry.game_id = %s
                   ORDER BY (player_id, combo.entry_id, index_in_entry,
                             index_in_combo)'''
        cur = self.conn.cursor()
        cur.execute(query, (game_id,))
        results = cur.fetchall()
        player_results = defaultdict(lambda: [])
        for data in results:
            player_results[data[0]].append(data[1:])
        return list(map(
            lambda pair: create_combo_set(game_id, pair[0], pair[1]),
            player_results.items()
        ))

    def read_entry(self, game_id: int, player_id: str) -> Optional[Entry]:
        query = '''SELECT entry_id, time_won
                   FROM GameEntry
                   WHERE game_id = %s
                   AND player_id = %s'''
        data = (game_id, player_id)
        cur = self.conn.cursor()
        cur.execute(query, data)
        results = cur.fetchone()
        if results is None:
            return None
        return Entry(results[0], game_id, player_id, results[1])

    def read_all_entries(self, game_id: int) -> List[Entry]:
        query = '''SELECT entry_id, player_id, time_won
                   FROM GameEntry
                   WHERE game_id = %s'''
        cur = self.conn.cursor()
        cur.execute(query, (game_id,))
        results = cur.fetchall()
        return [Entry(data[0], game_id, data[1], data[2]) for data in results]

    def update_entry(self, entry: Entry) -> None:
        query = '''UPDATE GameEntry
                   SET game_id = %s,
                   player_id = %s,
                   time_won = %s
                   WHERE entry_id = %s'''
        data = (entry.game_id, entry.player_id, entry.time_won, entry.entry_id)
        cur = self.conn.cursor()
        cur.execute(query, data)
        self.conn.commit()

    def delete_entry(self, game_id: int, player_id: str) -> None:
        query = '''DELETE FROM GameEntry
                   WHERE game_id = %s
                   AND player_id = %s'''
        data = (game_id, player_id)
        cur = self.conn.cursor()
        cur.execute(query, data)
        self.conn.commit()
