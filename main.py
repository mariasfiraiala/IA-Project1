from argparse import ArgumentParser
from pathlib import Path
from utils import *
from astar import *


def astar_helper(constraints: Constraint) -> None:
    total_students = sum(constraints.specs[SUBJECTS].values())
    initial = State(total_students, constraints)

    final = astar(initial, heuristic_uctp, get_neighbours_uctp, is_final_uctp, constraints)
    return final.coverage


def hc_helper(constraints: Constraint) -> None:
    pass


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("run", nargs="?", choices=("astar", "hc"))
    parser.add_argument("inpath")
    parser.add_argument("outpath")
    args = parser.parse_args()

    constraints = read_yaml_file(args.inpath)
    preferences = parse_soft_constraints(constraints)

    c = Constraint(constraints, preferences)
    coverage = None

    if args.run == "astar":
        coverage = astar_helper(c)
    elif args.run == "hc":
        coverage = hc_helper(c)

    timetable = coverage_to_timetable(coverage, c)
    write_timetable(pretty_print_timetable(timetable, args.inpath), args.outpath)
