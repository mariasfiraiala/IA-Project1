from typing import Callable
from heapq import heappop, heappush
from copy import deepcopy
from utils import *


def is_final_uctp(state : State) -> bool:
    return sum(state.remaining_students.values()) == 0


def check_hard(entry : Entry, state : State) -> bool:
    if entry.get_key() in state.coverage:
        return False
    
    if state.hours.get(entry.prof, 0) > 7:
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
    neigh.hours[entry.prof] = neigh.hours.get(entry.prof, 0) + 1
    neigh.remaining_students[entry.subject] = max(neigh.remaining_students[entry.subject] - students, 0)

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


def heuristic_uctp_helper(state : State, constraints : Constraint) -> float:
    assignable_students = {}
    for d in constraints.specs[DAYS]:
        for h in constraints.specs[INTERVALS]:
            for r in constraints.specs[ROOMS]:
                if (d, h, r) not in state.coverage.keys():
                    for s in constraints.specs[ROOMS][r][SUBJECTS]:
                        assignable_students[s] = assignable_students.get(s, 0) + constraints.specs[ROOMS][r][CAPACITY]

    bad_max = 0
    for sub, assignable in assignable_students.items():
        to_assign = state.remaining_students[sub]
        bad_max += to_assign / assignable

    return bad_max / len(assignable_students.values())


def heuristic_uctp(state : State, constraints : Constraint) -> float:
    f_students = sum(state.remaining_students.values()) / state.total_students
    f_rooms = heuristic_uctp_helper(state, constraints)

    if f_students == 0:
        return 0
    
    return f_students + f_rooms


def astar(start : State, h : Callable, neighbours : Callable, is_final : Callable, constraints : Constraint):
    num_states = 0

    frontier = []
    heappush(frontier, (h(start, constraints), start))
    
    while frontier:
        current = heappop(frontier)
        if is_final(current[1]):
            print(num_states)
            return current[1]

        neigh = neighbours(current[1], constraints)
        num_states += len(neigh)
        for n in neigh:
            heappush(frontier, (h(n, constraints), n))
