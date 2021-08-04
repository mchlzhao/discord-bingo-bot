from datetime import datetime
from typing import Optional

from src.entities.game import Game
from src.repos.in_memory.data_store import (
    get_game_store, read_game, write_game)


class InMemoryGameRepo:
    def __init__(self):
        self.next_game_id = 0

    @staticmethod
    def _game_dict_to_object(game_id, game_dict):
        return Game(game_id, game_dict['server_id'], game_dict['time_started'],
                    game_dict['time_finished'])

    def create_game(self, server_id: str) -> Game:
        self.next_game_id += 1
        cur_game = {
            'server_id': server_id,
            'time_started': datetime.now(),
            'time_finished': None,
            'events': [],
            'player_entries': []
        }
        write_game(self.next_game_id, cur_game)
        return InMemoryGameRepo._game_dict_to_object(self.next_game_id,
                                                     cur_game)

    def read_active_game(self, server_id: str) -> Optional[Game]:
        for game_id, game_dict in get_game_store().items():
            if game_dict['server_id'] == server_id and \
               game_dict['time_finished'] is None:
                return InMemoryGameRepo._game_dict_to_object(game_id,
                                                             game_dict)
        return None

    def update_game(self, game: Game) -> None:
        game_dict = read_game(game.game_id)
        game_dict['time_started'] = game.time_started
        game_dict['time_finished'] = game.time_finished
        write_game(game.game_id, game_dict)
