from core.Event import Event
from core.PlayerEntry import PlayerEntry

class Game:
    def __init__(self, name, created_by):
        self.name = name
        self.created_by = created_by
        self.events = []
        self.players = {}

        self.events_hit_dict = {}
        self.players_won_dict = {}
    
    def set_events(self, events):
        self.events = [Event(desc, ind) for ind, desc in enumerate(events)]
        self.events_hit_dict = {event.index: False for event in self.events}
    
    def set_player(self, player_id, board_order):
        self.players[player_id] = PlayerEntry(board_order)
        self.players_won_dict[player_id] = False
    
    def hit(self, id):
        event = self.events[id]
        new_winners = []
        if not self.events_hit_dict[event.index]:
            event.is_hit = True
            self.events_hit_dict[event.index] = True
            for player_id, has_won in self.players_won_dict.items():
                if not has_won and self.players[player_id].has_won(self.events_hit_dict):
                    new_winners.append(player_id)
                    self.players_won_dict[player_id] = True
        return new_winners
    
    def unhit(self, id):
        event = self.events[id]
        if self.events_hit_dict[event.index]:
            event.is_hit = False
            self.events_hit_dict[event.index] = False
            for player_id, has_won in self.players_won_dict.items():
                if has_won and not self.players[player_id].has_won(self.events_hit_dict):
                    self.players_won_dict[player_id] = False
    
    def calculate_players_won(self):
        players_won = []
        for player_id, entry in self.players.items():
            if entry.has_won(self.events_hit_dict):
                players_won.append(player_id)
        return players_won

    def has_started(self):
        return any(self.events_hit_dict.values())
