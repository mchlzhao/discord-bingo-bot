from typing import List, Optional

from src.entities.combo import Combo
from src.entities.combo_set import ComboSet
from src.entities.entry import Entry
from src.entities.event import Event
from src.repos.abstract.iplayer_repo import IPlayerRepo


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

        combo_infos = list(dict.fromkeys(
            map(lambda x: x[:2], results)
        ))
        combo_set = ComboSet(player_id, [
            Combo(info[0], [], info[1]) for info in combo_infos])
        for data in results:
            combo_set.combos[data[1]].events.append(
                Event(data[2], game_id, data[3], data[4], data[5]))
        return combo_set

    def read_all_combo_sets(self, game_id: int) -> List[ComboSet]:
        pass

    def read_entry(self, game_id: int, player_id: str) -> Optional[Entry]:
        pass

    def read_all_entries(self, game_id: int) -> List[Entry]:
        pass

    def update_entry(self, entry: Entry) -> None:
        pass

    def delete_entry(self, game_id: int, player_id: str) -> None:
        pass
