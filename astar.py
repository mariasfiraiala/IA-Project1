from typing import Callable
from heapq import heappop, heappush
from utils import *


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
