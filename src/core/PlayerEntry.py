from core.PlayerBoard import PlayerBoard

class PlayerEntry:
    def __init__(self, board_order):
        self.NUM_BOARDS = 4
        self.BOARD_SIZE = 3

        self.boards = []
        for i in range(0, self.NUM_BOARDS * self.BOARD_SIZE, self.BOARD_SIZE):
            self.boards.append(PlayerBoard(board_order[i:i + self.BOARD_SIZE]))
    
    def get_masks(self, events_hit_dict):
        return [board.get_mask(events_hit_dict) for board in self.boards]

    def has_won(self, events_hit_dict):
        return any([board.has_won(events_hit_dict) for board in self.boards])
