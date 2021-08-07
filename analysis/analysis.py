import matplotlib.pyplot as plt
import numpy as np
import random

NUM_COMBOS = 4
COMBO_SIZE = 3
TOT = NUM_COMBOS * COMBO_SIZE

NUM_ENTRIES = 1000
TRIALS_PER_ENTRY = 250


def n_to_c(x): return chr(ord('A') + x)


def num_to_char(l):
    return list(map(n_to_c, l))


with open('events.csv', 'r') as events_file:
    prob = []
    for line in events_file:
        tokens = line.strip().split('~')
        prob.append(float(tokens[3]))

NUM_EVENTS = len(prob)


def gen_entry(id_list):
    entry = []
    for i in range(NUM_COMBOS):
        np.random.shuffle(id_list)
        entry.extend(id_list[:COMBO_SIZE])
    return entry


def gen_result(prob):
    result = []
    for p in prob:
        result.append(np.random.binomial(1, p) == 1)
    return result


def check_win(entry, result):
    for i in range(0, len(entry), COMBO_SIZE):
        win = all([result[j] for j in entry[i:i + COMBO_SIZE]])
        if win:
            return True
    return False


def calculate_prop(entry):
    global TRIALS_PER_ENTRY
    wins = 0
    for i in range(TRIALS_PER_ENTRY):
        result = gen_result(prob)
        if check_win(entry, result):
            wins += 1
    return wins / TRIALS_PER_ENTRY


def filter():
    by_prop = []
    for i, p in enumerate(prob):
        by_prop.append((p, i))
    by_prop.sort(key=lambda x: -x[0])
    return list(map(lambda x: x[1], by_prop[:12]))


def random_search():
    l = filter()
    best_prop = -1
    best_entry = None
    for _ in range(NUM_ENTRIES):
        entry = gen_entry(l)
        win_prop = calculate_prop(entry)
        if win_prop > best_prop:
            best_prop = win_prop
            best_entry = entry

    print(best_prop, num_to_char(best_entry))


def get_all_triples(l):
    triples = []
    for i in range(0, len(l)):
        for j in range(i+1, len(l)):
            for k in range(j+1, len(l)):
                triples.append([l[i], l[j], l[k]])
    return triples


def logical_brute_force():
    l = filter()
    l = l[:8]
    triples = get_all_triples(l)
    print(f'TRIPLES LENGTH = {len(triples)}')

    best_prop = -1
    best_entry = None
    for i in range(len(triples)):
        print(i)
        for j in range(i+1, len(triples)):
            for k in range(j+1, len(triples)):
                entry = triples[i] + triples[j] + triples[k] + [10, 11, 12]
                win_prop = calculate_prop(entry)
                if win_prop > best_prop:
                    best_prop = win_prop
                    best_entry = entry
    print(best_prop, best_entry)


random_search()
# logical_brute_force()
