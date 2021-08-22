from datetime import datetime
from typing import Optional


class Entry:
    def __init__(self, entry_id: str, game_id: int, player_id: str,
                 time_won: Optional[datetime]):
        self.entry_id = entry_id
        self.game_id = game_id
        self.player_id = player_id
        self.time_won = time_won

    def __str__(self):
        return f'Entry id={self.entry_id}: game={self.game_id} player={self.player_id} time_won={self.time_won}'
