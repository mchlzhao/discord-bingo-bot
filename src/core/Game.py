from core.Event import Event
from core.PlayerEntry import PlayerEntry

class Game:
    def __init__(self, name, created_by):
        self.name = name
        self.created_by = created_by
        self.events = []
        self.players = {}

        self.events_hit = []
    
    def set_events(self, events):
        self.events = [Event(desc, ind) for ind, desc in enumerate(events)]
    
    def set_player(self, player_id, board_order):
        self.players[player_id] = PlayerEntry(board_order)
    
    def hit(self, id):
        event = self.events[id]
        if event not in self.events_hit:
            event.is_hit = True
            self.events_hit.append(event)
    
    def unhit(self, id):
        event = self.events[id]
        if event in self.events_hit:
            event.is_hit = False
            self.events_hit.remove(event)
    
    def calculate_players_won(self):
        players_won = []
        for player_id, entry in self.players.items():
            if entry.has_won(self.events_hit):
                players_won.append(player_id)
        return players_won

    def has_game_started(self):
        return len(self.events_hit) > 0
