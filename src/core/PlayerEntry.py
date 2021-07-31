class PlayerEntry:
    def __init__(self, board, IN_A_ROW=4):
        self.board = board
        self.IN_A_ROW = IN_A_ROW
    
    def get_mask(self, events_hit):
        events_ind = list(map(lambda x: x.index, events_hit))
        return [index in events_ind for index in self.board]

    def has_won(self, events_hit):
        mask = self.get_mask(events_hit)
        for i in range(len(mask) - IN_A_ROW + 1):
            sublist = mask[i:i + IN_A_ROW]
            if all(sublist):
                return True
        return False
