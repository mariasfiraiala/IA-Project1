from random import choice
from utils import *
from typing import Callable


def stochastic_hill_climbing(
        initial: State,
        score: Callable,
        neighbours: Callable,
        is_final: Callable,
        constraints: Constraint,
        max_iters: int = 100) -> tuple[bool, State, int, int]:
    iters, states = 0, 0
    state = initial
    
    while iters < max_iters:
        if is_final(state):
            break

        all_states = neighbours(state, constraints)
        min_states = []

        state_score = score(state, constraints)
        for s in all_states:
            states += 1
            if score(s, constraints) < state_score:
                min_states.append(s)

        if len(min_states) == 0:
            break
        else:
            state = choice(min_states)

        iters += 1
        
    return is_final(state), state, iters, states


def hc(
        initial: State,
        score : Callable,
        neighbours: Callable,
        is_final: Callable,
        constraints: Constraint,
        max_restarts: int = 100,
        run_max_iters: int = 100) -> State:
    total_iters, total_states = 0, 0
    state = initial

    for _ in range(max_restarts):
        final, i_state, iters, states = stochastic_hill_climbing(state, score, neighbours,
                                                                 is_final, constraints, run_max_iters)
        total_iters += iters
        total_states += states
        if final:
            state = i_state
            break
        else:
            state = initial

    print(total_states)
    return state
