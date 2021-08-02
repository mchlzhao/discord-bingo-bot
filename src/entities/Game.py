from datetime import datetime
from typing import List


class Game:
    def __init__(self, guild_id: str, time_created: datetime,
                 time_finished: datetime, player_win_order: List[str]) -> None:
        self.guild_id = guild_id
        self.time_created = time_created
        self.time_finished = time_finished
        self.player_win_order = player_win_order

    def add_winner(self, player_id: str) -> None:
        self.player_win_order.append(player_id)

    def remove_winner(self, player_id: str) -> None:
        self.player_win_order.remove(player_id)

    def has_finished(self) -> bool:
        return self.time_finished is not None
