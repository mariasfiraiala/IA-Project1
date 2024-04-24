from copy import deepcopy
import yaml
import argparse
import sys

class State:
    def __init__(self):
        self.coverage = {}
        self.hours = {}
        self.assigned_students = {}

    def __init__(self, state, entry, students):
        self = deepcopy(state)
        self.coverage[entry.get_key()] = entry.get_value()
        self.assigned_students[entry.subject] = self.assigned_students.get(entry.subject, 0) + students
        self.hours[entry.prof] = self.hours.get(entry.prof, 0) + 1


class Entry:
    def __init__(self, day, hour, room, subject, prof):
        self.day = day
        self.hour = hour
        self.room = room
        self.subject = subject
        self.prof = prof

    def get_key(self):
        return (self.day, self.hour, self.room)
    
    def get_value(self):
        return (self.subject, self.prof)


class Constraint:
    def __init__(self, specs, preferences):
        self.specs = specs
        self.preferences = preferences


##################### MACROURI #####################
INTERVALS = "Intervale"
DAYS = "Zile"
SUBJECTS = "Materii"
PROFESSORS = "Profesori"
ROOMS = "Sali"
CAPACITY = "Capacitate"
CONSTRAINTS = "Constrangeri"

UNPREFERRED_INTERVAL = "unpreferred_i"
UNPREFERRED_DAY = "unpreferred_d"
PREFERRED_INTERVAL = "preferred_i"
PREFERRED_DAY = "preferred_d"


def read_yaml_file(file_path : str) -> dict:
    '''
    Citeste un fișier yaml și returnează conținutul său sub formă de dicționar
    '''
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)


def parse_soft_constraints(constraints):
    preferances = {}

    for prof in constraints[PROFESSORS]:
        for const in constraints[PROFESSORS][prof][CONSTRAINTS]:
            if "!" in const:
                if "-" in const:
                    preferances.setdefault(prof, {}).setdefault(UNPREFERRED_INTERVAL, []).append(const[1:])
                else:
                    preferances.setdefault(prof, {}).setdefault(UNPREFERRED_DAY, []).append(const[1:])

            else:
                if "-" in const:
                    preferances.setdefault(prof, {}).setdefault(PREFERRED_INTERVAL, []).append(const)
                else:
                    preferances.setdefault(prof, {}).setdefault(PREFERRED_DAY, []).append(const)

    return preferances
