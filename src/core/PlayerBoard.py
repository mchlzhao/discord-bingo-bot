class PlayerBoard:
    def __init__(self, board_order):
        self.board_order = board_order
    
    def get_mask(self, events_hit_dict):
        return [events_hit_dict[event_ind] for event_ind in self.board_order]
    
    def has_won(self, events_hit_dict):
        return all(self.get_mask(events_hit_dict))
