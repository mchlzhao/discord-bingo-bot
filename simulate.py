import random
import sys

from checker import *
from inputparser import *
from randomiser import *

SIZE = 5
TRIALS = 1000000

def simulate(randomiser, probs):
    num_success = 0
    for _ in range(TRIALS):
        success_list = [False] * len(probs)
        for i in range(len(success_list)):
            success_list[i] = randomiser.bernoulli_trial(probs[i])
        if is_success(success_list, SIZE):
            num_success += 1
    return num_success

def main(seed):
    randomiser = Randomiser(seed, True)

    print("SEED = %d" % seed)

    parser = InputParser('lines.csv')

    probs = parser.get_probs()
    randomised_probs = custom_random_shuffle(randomiser, probs)

    num_success = simulate(randomiser, randomised_probs)

    print(num_success/TRIALS)

seed = int(sys.argv[1])
main(seed)
