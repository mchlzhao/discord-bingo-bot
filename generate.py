import sys

from grid import *
from inputparser import *
from randomiser import *

SIZE = 5
BOX_WIDTH = 11
BOX_HEIGHT = 3
SHOW_PROBS = False

def generate(seed):
    randomiser = Randomiser(seed, False)
    parser = InputParser('lines.csv')

    lines = parser.get_lines()
    if SHOW_PROBS:
        lines = [
            line+' '+str(prob) for line, prob in
                zip(parser.lines, parser.probs)
        ]
    randomised_lines = custom_random_shuffle(randomiser, lines)

    grid = Grid(SIZE, SIZE, BOX_WIDTH, BOX_HEIGHT)
    for i in range(SIZE*SIZE):
        grid.write_to_box(randomised_lines[i], i//SIZE, i%SIZE)
    return grid

if __name__ == '__main__':
    name = sys.argv[1]
    seed = int(sys.argv[2])

    print(name + ': ' + str(seed))

    grid = generate(seed)
    grid.print_grid()
