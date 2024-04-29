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
    with open(file_path, 'r') as file:
        constraints = yaml.safe_load(file)

    constraints[INTERVALS] = [tuple(int(x) for x in i.strip('()').split(',')) for i in constraints[INTERVALS]]
    return constraints


def write_timetable(timetable : str, file_path : str) -> None:
    with open(file_path, "w") as file:
        file.write(timetable)


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


def coverage_to_timetable(coverage : dict, constraints : Constraint) -> dict:
    timetable = {}

    for (d, h, r), (s, p) in coverage.items():
        timetable.setdefault(d, {}).setdefault(h, {}).setdefault(r, {})
        timetable[d][h][r] = (p, s)

    for d in constraints.specs[DAYS]:
        for h in constraints.specs[INTERVALS]:
            for r in constraints.specs[ROOMS]:
                if (d, h, r) not in coverage.keys():
                    timetable.setdefault(d, {}).setdefault(h, {}).setdefault(r, {})
                    timetable[d][h][r] = None

    return timetable


def get_profs_initials(profs : list) -> dict:
    initials_to_prof = {}
    prof_to_initials = {}
    initials_count = {}

    for prof in profs:
        name_components = prof.split(' ')
        initials = name_components[0][0] + name_components[1][0]

        if initials in initials_count:
            initials_count[initials] += 1
            initials += str(initials_count[initials])
        else:
            initials_count[initials] = 1

        initials_to_prof[initials] = prof
        prof_to_initials[prof] = initials

    return prof_to_initials, initials_to_prof


def allign_string_with_spaces(s : str, max_len : int, allignment_type : str = 'center') -> str:
    len_str = len(s)

    if len_str >= max_len:
        raise ValueError('Lungimea string-ului este mai mare decât lungimea maximă dată')

    if allignment_type == 'left':
        s = 6 * ' ' + s
        s += (max_len - len(s)) * ' '

    elif allignment_type == 'center':
        if len_str % 2 == 1:
            s = ' ' + s
        s = s.center(max_len, ' ')

    return s


def pretty_print_timetable(timetable : {str : {(int, int) : {str : (str, str)}}}, input_path : str) -> str:
    max_len = 30

    profs = read_yaml_file(input_path)[PROFESSORS].keys()
    profs_to_initials, _ = get_profs_initials(profs)

    table_str = '|           Interval           |             Luni             |             Marti            |           Miercuri           |              Joi             |            Vineri            |\n'

    no_classes = len(timetable['Luni'][(8, 10)])

    first_line_len = 187
    delim = '-' * first_line_len + '\n'
    table_str = table_str + delim

    for interval in timetable['Luni']:
        s_interval = '|'

        crt_str = allign_string_with_spaces(f'{interval[0]} - {interval[1]}', max_len, 'center')

        s_interval += crt_str

        for class_idx in range(no_classes):
            if class_idx != 0:
                s_interval += f'|{30 * " "}'

            for day in timetable:
                classes = timetable[day][interval]
                classroom = list(classes.keys())[class_idx]

                s_interval += '|'

                if not classes[classroom]:
                    s_interval += allign_string_with_spaces(f'{classroom} - goala', max_len, 'left')
                else:
                    prof, subject = classes[classroom]
                    s_interval += allign_string_with_spaces(f'{subject} : ({classroom} - {profs_to_initials[prof]})', max_len, 'left')

            s_interval += '|\n'
        table_str += s_interval + delim

    return table_str
