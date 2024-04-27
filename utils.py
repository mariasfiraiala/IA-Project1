import yaml


class State:
    def __init__(self, total_students : int, constraints : 'Constraint'):
        self.coverage = {}
        self.hours = {}
        self.remaining_students = {}
        self.total_students = total_students

        for sub, stud in constraints.specs[SUBJECTS].items():
            self.remaining_students[sub] = stud


    def __lt__(self, other):
        return sum(self.remaining_students.values()) < sum(other.remaining_students.values())


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


def parse_soft_constraints(constraints : dict) -> dict:
    preferances = {}

    for prof in constraints[PROFESSORS]:
        for const in constraints[PROFESSORS][prof][CONSTRAINTS]:
            if "!" in const:
                if "-" in const:
                    x, y = int(const[1:].split("-")[0]), int(const[1:].split("-")[1])
                    intervals = [(x, y) if y - x <= 2 else (i, i + 2) for i in range(x, y, 2)]

                    preferances.setdefault(prof, {}).setdefault(UNPREFERRED_INTERVAL, []).extend(intervals)
                else:
                    preferances.setdefault(prof, {}).setdefault(UNPREFERRED_DAY, []).append(const[1:])

            else:
                if "-" in const:
                    x, y = int(const.split("-")[0]), int(const.split("-")[1])
                    intervals = [(x, y) if y - x <= 2 else (i, i + 2) for i in range(x, y, 2)]

                    preferances.setdefault(prof, {}).setdefault(PREFERRED_INTERVAL, []).extend(intervals)
                else:
                    preferances.setdefault(prof, {}).setdefault(PREFERRED_DAY, []).append(const)

    return preferances
