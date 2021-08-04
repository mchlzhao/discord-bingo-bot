from datetime import datetime


class Game:
    def __init__(self, game_id: str, server_id: str, time_started: datetime,
                 time_finished: datetime) -> None:
        self.game_id = game_id
        self.server_id = server_id
        self.time_started = time_started
        self.time_finished = time_finished

    def __str__(self):
        return f'Game id={self.game_id}: server_id = {self.server_id} {self.time_started} {self.time_finished}'
