from src.entities.combo import Combo
from src.entities.combo_set import ComboSet
from src.entities.entry import Entry
from src.entities.event import Event
from src.entities.game import Game


class DataStore:
    def __init__(self):
        self.games = {}
        self.events = {}
        self.entries = {}
        self.combo_sets = {}

    def _sample_game(self):
        game = Game('1', '1', None, None)
        self.games[game.game_id] = game

    def _sample_event(self):
        game_id = '1'
        self.events[game_id] = [Event(None, game_id, 'e0', 0, False)]

    def _sample_entry(self):
        game_id = '1'
        player_id = 'player_id'
        self.entries[game_id][player_id] = \
            Entry('entry_id', game_id, 'player_id', None)

    def _sample_combo_set(self):
        game_id = '1'
        player_id = 'player_id'
        self.combo_sets[game_id][player_id] = \
            ComboSet(player_id, [Combo(None, None, 0)])
