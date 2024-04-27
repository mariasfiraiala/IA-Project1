from typing import Callable
from heapq import heappop, heappush
from utils import *


def is_final_uctp(state : State, constraints : Constraint) -> bool:
    for subject, students in constraints.specs[SUBJECTS].items():
        if state.assigned_students[subject] < students:
            return False
        
    return True

# (zi, interval, sala) -> (materie, prof)
def check_hard(entry : Entry, state : State) -> bool:
    if entry.get_key() in state.coverage:
        return False
    
    if state.hours.get(entry.prof, 0) >= 7:
        return False
    
    return True
    

def check_soft(entry : Entry, constraints : Constraint) -> bool:
    if entry.day in constraints.preferences[entry.prof].get(UNPREFERRED_DAY, []):
        return False

    if entry.hour in constraints.preferences[entry.prof].get(UNPREFERRED_INTERVAL, []):
        return False

    return True


def create_neigh(state : State, entry : Entry, students : int) -> State:
    neigh = deepcopy(state)
    neigh.coverage[entry.get_key()] = entry.get_value()
    neigh.assigned_students[entry.subject] = neigh.assigned_students.get(entry.subject, 0) + students
    neigh.hours[entry.prof] = neigh.hours.get(entry.prof, 0) + 1

    return neigh


def get_neighbours_uctp(state : State, constraints : Constraint) -> list:
    neigh = []

    for d in constraints.specs[DAYS]:
        for h in constraints.specs[INTERVALS]:
            for r in constraints.specs[ROOMS]:
                for s in constraints.specs[ROOMS][r][SUBJECTS]:
                    for p in constraints.specs[PROFESSORS].keys():
                        if s in constraints.specs[PROFESSORS][p][SUBJECTS]:
                            entry = Entry(d, h, r, s, p)

                            if check_hard(entry, state) and check_soft(entry, constraints):
                                neigh.append(create_neigh(state, entry, constraints.specs[ROOMS][r][CAPACITY]))

    return neigh


def heuristic_uctp(state : State):
    pass


def astar(start : State, h : Callable, neighbours : Callable, is_final : Callable, constraints : Constraint):
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