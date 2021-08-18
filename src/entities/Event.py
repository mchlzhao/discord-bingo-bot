class Event:
    def __init__(self, event_id: int, game_id: int, desc: str, index: int,
                 is_hit: bool = False):
        self.event_id = event_id
        self.game_id = game_id
        self.desc = desc
        self.index = index
        self.is_hit = is_hit

    def __str__(self):
        return f'Event id={self.event_id}: game_id={self.game_id} {self.desc} {self.index} {self.is_hit}'
