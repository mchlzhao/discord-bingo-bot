from datetime import datetime
from typing import Optional


class Game:
    def __init__(self, game_id: Optional[int], server_id: str,
                 time_started: datetime,
                 time_finished: Optional[datetime]):
        self.game_id = game_id
        self.server_id = server_id
        self.time_started = time_started
        self.time_finished = time_finished

    def __str__(self):
        return f'Game id={self.game_id}: server_id={self.server_id} {self.time_started} {self.time_finished} '
