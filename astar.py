from utils import *
from heapq import heappop, heappush
from collections import defaultdict
from functools import reduce


def is_final_uctp(state, constraints):
    for subject, students in constraints[SUBJECTS].items():
        if state.assigned_students[subject] < students:
            return 0
        
    return 1

# (zi, interval, sala) -> (materie, prof)
def check_hard(entry, state):
    if entry.get_key() in state:
        return 0
    
    if state.hours[entry.prof] >= 7:
        return 0
    
    return 1
    

def check_soft(entry, preferances):
    if entry.i in preferances[entry.prof][UNPREFERRED_DAY]:
        return 0

    if entry.h in preferances[entry.prof][UNPREFERRED_INTERVAL]:
        return 0

    return 1


def get_neighbours_uctp(state, constraints):
    neigh = []

    for d in constraints[DAYS]:
        for h in constraints[INTERVALS]:
            for r in constraints[ROOMS]:
                for s in constraints[ROOMS][r][SUBJECTS]:
                    for p in constraints[PROFESSORS].keys():
                        if constraints[PROFESSORS][p][SUBJECTS] == s:
                            entry = Entry(d, h, r, s, p)

                            if check_hard(entry, state) and check_soft(entry, constraints.preferences):
                                neigh.append(State(state, entry, constraints[ROOMS][r][CAPACITY]))

    return neigh


def heuristic_uctp(state):
    pass


def astar(start, h, neighbours, is_final, constraints):
    frontier = []
    heappush(frontier, (0 + h(start), start))
    
    discovered = {start: (None, 0)}

    while frontier:
        nod_crt = heappop(frontier)
        if is_final(nod_crt[1]):
            break

        next_cost = discovered[nod_crt[1]][1] + 1
        for n in neighbours(nod_crt[1], constraints):
            if n not in discovered or discovered[n][1] > next_cost:
                discovered[n] = (nod_crt[1], next_cost)
                heappush(frontier, (next_cost + h(n), n))

    return None