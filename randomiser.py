import numpy
import random

class Randomiser:
    def __init__(self, seed, old):
        self.rng = numpy.random.RandomState(seed)

        self.old = old
        if self.old:
            random.seed(seed)

    def old_random_shuffle(self, input_list):
        random.shuffle(input_list)

    def random_shuffle(self, input_list):
        if self.old:
            self.old_random_shuffle(input_list)
        else:
            self.rng.shuffle(input_list)

    def old_bernoulli_trial(self, p):
        return random.random() < p

    def bernoulli_trial(self, p):
        if self.old:
            return self.old_bernoulli_trial(p)
        return self.rng.rand() < p

def custom_random_shuffle(randomiser, input_list):
    temp = input_list[1:]
    randomiser.random_shuffle(temp)
    return temp[:12] + [input_list[0]] + temp[12:]

