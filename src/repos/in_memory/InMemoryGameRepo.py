from datetime import datetime
from typing import Optional

from entities.Game import Game
from repos.in_memory.data_store import game_store


class InMemoryGameRepo:
    def __init__(self):
        self.next_game_id = 0

    @staticmethod
    def _game_dict_to_object(index, game_dict):
        return Game(index, game_dict['server_id'], game_dict['time_started'],
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
        game_store[self.next_game_id] = cur_game
        return InMemoryGameRepo._game_dict_to_object(self.next_game_id,
                                                     cur_game)

    def read_active_game(self, server_id: str) -> Optional[Game]:
        for game_id, game_dict in game_store.items():
            if game_dict['server_id'] == server_id and \
               game_dict['time_finished'] is None:
                return InMemoryGameRepo._game_dict_to_object(game_id,
                                                             game_dict)
        return None

    def update_game(self, game: Game) -> None:
        game_store[game.game_id]['time_started'] = game.time_started
        game_store[game.game_id]['time_finished'] = game.time_finished
