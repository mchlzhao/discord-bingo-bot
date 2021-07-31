import sys

from checker import *
from grid import *
from inputparser import *
from randomiser import *

SIZE = 5
PRINT_GRID = True

def is_win(seed):
    randomiser = Randomiser(seed, False)
    parser = InputParser('lines.csv')

    did_occur = parser.get_did_occur()
    randomised_did_occur = custom_random_shuffle(randomiser, did_occur)

    grid = Grid(SIZE, SIZE, 1, 1, 1, 0)
    
    for i in range(SIZE*SIZE):
        if randomised_did_occur[i]:
            grid.write_to_box('*', i//SIZE, i%SIZE)
    
    is_win = is_success(randomised_did_occur, SIZE)

    return (grid, is_win)

if __name__ == '__main__':
    name = sys.argv[1]
    seed = int(sys.argv[2])

    print(name + ': ' + str(seed))

    grid, has_won = is_win(seed)

    print('WIN' if has_won else 'LOSS')
    if PRINT_GRID:
        grid.print_grid()
