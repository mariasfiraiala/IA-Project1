from argparse import ArgumentParser
from pathlib import Path
from utils import *
from astar import *


def astar_helper(constraints: Constraint) -> None:
   pass 


def hc_helper(constraints: Constraint) -> None:
    pass


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("run", nargs="?", choices=("astar", "hc"))
    args = parser.parse_args()


    paths = Path("inputs").rglob("*")
    for p in paths:
        constraints = read_yaml_file(str(p))
        preferences = parse_soft_constraints(constraints)

        c = Constraint(constraints, preferences)
    
        if args.run == "astar":
            astar_helper(c)
        elif args.run == "hc":
            hc_helper(c)
