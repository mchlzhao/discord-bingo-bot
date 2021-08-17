from datetime import datetime
from typing import Optional

from src.entities.game import Game
from src.repos.abstract.igame_repo import IGameRepo


class PostgresGameRepo(IGameRepo):
    def __init__(self, conn):
        self.conn = conn

    def create_game(self, server_id: str) -> Game:
        game = Game(None, server_id, datetime.now(), None)
        query = '''INSERT INTO Game (server_id, time_started, time_finished)
                   VALUES (%s, %s, NULL)
                   RETURNING game_id'''
        data = (server_id, game.time_started)
        cur = self.conn.cursor()
        cur.execute(query, data)
        game.game_id = cur.fetchone()[0]
        self.conn.commit()
        return game

    def read_active_game(self, server_id: str) -> Optional[Game]:
        query = '''SELECT * FROM Game
                   WHERE server_id = %s
                   AND time_finished IS NULL'''
        data = (server_id,)
        cur = self.conn.cursor()
        cur.execute(query, data)
        result = cur.fetchone()
        return Game(*result)

    def update_game(self, game: Game) -> None:
        query = '''UPDATE Game
                   SET server_id = %s,
                   time_started = %s,
                   time_finished = %s
                   WHERE game_id = %s'''
        data = (game.server_id, game.time_started,
                game.time_finished, game.game_id)
        cur = self.conn.cursor()
        cur.execute(query, data)
        self.conn.commit()
