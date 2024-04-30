Copyright 2024 Maria Sfiraiala (maria.sfiraiala@stud.acs.upb.ro)

#  University Course Timetabling Problem - Project1

The University Course Timetabling Problem (UCTP) is a scheduling problem of planning classes in certain intervals and rooms by considering constraints such as the number of students, lecturers, and departments.
The constraints may be hard (encouraged to be satisfied) or soft (better to be fulfilled).

While this problem is easier solved with a Constraint Satisfaction Problem (CSP) approach, we tried to implement a solution based on both the A* and Hill-Climbing algorithms; they use the same state and constraints representation.

## State representation

### Entries

```Python
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
```

The main aspect of the `State` class is the `coverage` dictionary, which stores key - value tuples used for filling up an interval in our timetable.
The key is represented by a `(day, interval, room)` tuple, while the value is represented by a `(subject, prof)` tuple.
As a result, the `coverage` dictionary maintains all the intervals set, up until the present.

The rest of the entries form extra information, maintained in order to have better times when checking for hard/soft constraints violations.
For instance, the `hours` dictionary stores how many intervals each prof was appointed.
The `remaining_students` dictionary retains for each subject how many students are left to be seated (used for computing the heuristic value).
The `total_students` value stores the total number of students in the uni (used for computing the heuristic value).

### Logic

The first state of each algorithm is empty; there are no intervals appointed.
The second level of states (the neighbours of the first one) have only one interval set, in how many possibilities there are, all while checking both hard and soft constraints.
The third level of states (the neighbours of the second one) have only two intervals set, in how many possibilities there are, still while checking both hard and soft constraints.
And so on, until there are no students left to appoint to intervals.
In our implementation, **all generated states must satisfy the hard and soft constraints**.
In other words, we decided to not even insert neighbours that do not check the conditions, while our soft constraints are just as equally important as the hard ones. 

## Constraints representation

### Functions

```Python
class Constraint:
    def __init__(self, specs : dict, preferences : dict):
        self.specs = specs
        self.preferences = preferences
```

The `Constraint` class is described by the `specs` dictionary, containing all the information parsed at the beginning from the `yaml` file and by the `preferences` dictionary, which for each professor keeps a dictionary with all the preferred and unpreferred days and intervals.
This representation helps us speed up the functions used for checking hard and soft constraints:

```Python
def check_hard(entry : Entry, state : State) -> bool:
    if entry.get_key() in state.coverage.keys():
        return False

    for (d, h, _), (_, p) in state.coverage.items():
        if d == entry.day and h == entry.hour and entry.prof == p:
            return False
    
    if state.hours.get(entry.prof, 1) >= 7:
        return False
    
    return True
    

def check_soft(entry : Entry, constraints : Constraint) -> bool:
    if entry.day in constraints.preferences[entry.prof].get(UNPREFERRED_DAY, []):
        return False

    if entry.hour in constraints.preferences[entry.prof].get(UNPREFERRED_INTERVAL, []):
        return False

    return True
```

### Logic

When it comes to A* and Hill-Climbing, we had to make a decision between how much we **explore** and how much we **exploit**; by exploring meaning a more permissive function for generating states and a more complicated heuristic function and by exploiting meaning a more restrictive state generator and a more relaxed and easier to model heuristic.
We went the exploitation way and we checked both hard and soft conditions when constructing the neighbours.
Regarding the hard constraints, some of them didn't even make their way into the above method as they were implicitly checked when traversing the `yaml` dictionary and the constraint to have all students for a subject seated is used to check for algorithm termination and success.
Regarding the soft constraints, the preferred days and intervals are virtually meaningless as we are interested in what the prof **doesn't wish to do**.
We parsed them, nevertheless.

## Heuristic

### Functions

```Python
def heuristic_uctp(state : State, constraints : Constraint) -> float:
    f_students = sum(state.remaining_students.values()) / state.total_students
    f_rooms = heuristic_uctp_helper(state, constraints)

    if f_students == 0:
        return 0
    
    return f_students + f_rooms
```

The heuristic is made up from two factors, one concerned with the number of students to seat and one concerned with how limited a certain subject can become.

### Logic

The first factor is the most basic one.
It's the first thing to check also, if there are no more students to seat, then return the mark that we reached a final state. **With this factor only, the algorithm doesn't converge.**

The second factor is the one that brings the most sensitivity to the heuristic.
The main problem with the heuristic with only one factor is that we might seat all students for every subject but one.
And that one subject won't have any interval and room proper for its functioning.
To approach this issue we determined for every subject the ratio between the number of students that are remaining to be assigned and the number of students that we can seat in unused slots.
We, then, calculate the average for this value between all subjects and return it.
The idea behind this choice is that a very bad assignment for a subject will influence the other very good subject assignments and therefore make the state less favored.
On the other hand, however, a fully covered subject will produce the value 0, perfect because it doesn't contribute to the overall addition to the heuristic value.

## Differences between lab and project algo

### A*

We didn't really changed the lab implementation apart from the fact that we removed the cost.
That is due to the fact that, as we explained earlier, we went the exploitation route, so the cost was now redundant (the states are cost wise, equally good).
We would have been interested in a cost function if we did generate states that break the soft constraints, but that's not the case.
We also gave up on the reconstruction of the solution step, as our result is already stored in the final state (the `coverage` dictionary with the fully assigned timetable).

### Hill-Climbing

Between all the Hill-Climbing versions we chose "Random Restart Hill-Climbing" which for every iteration calls "Stochastic Hill-Climning".
Even though, when we firts implemented the labs, the inner Hill-Climbing algorithm of choice was the regular one, for this project, generating a random timetable to start the program with is cumbersome.
The trick we came up with is to fully restart the program with the empty state, and by applying the "Stochastic" variant, we almost everytime, result in a totally different state than the previous iteration.

## Comparisons between approaches

### A*

| Test | Execution Time In Seconds | Number of States |
|------|---------------------------|------------------|
| dummy.yaml | 0.00962 | 185 |
| orar_mic_exact.yaml | 0.35537 | 3208 |
| orar_mediu_relaxat.yaml | 9.21104 | 45565 |
| orar_mare_relaxat.yaml | 24.48589 | 75115 |
| orar_constrans_incalcat.yaml | - |  - |

For every test (except "orar_constrans_incalcat", because the heuristic doesn't converge), the implementation creates a timetable with **0 hard constrains and 0 soft constrains violations**.

### Hill-Climbing

| Number Of Iteration | Test | Execution Time In Seconds | Number of States |
|---------------------|------|---------------------------|------------------|
| 1 | dummy.yaml | 0.00865 | 166 |
| 2 | dummy.yaml | 0.00865 | 159 |
| 3 | dummy.yaml | 0.00865 | 154 |
| 4 | dummy.yaml | 0.00865 | 161 |
| 5 | dummy.yaml | 0.00865 | 168 |
| 1 | orar_mic_exact.yaml | 0.56399 | 3887 |
| 2 | orar_mic_exact.yaml | 0.98533 | 7782 |
| 3 | orar_mic_exact.yaml | 0.47522 | 3824 |
| 4 | orar_mic_exact.yaml | 0.49777 | 3974 |
| 5 | orar_mic_exact.yaml | 0.94669 | 7616 |
| 1 | orar_mediu_relaxat.yaml | 14.02567 | 58177 |
| 2 | orar_mediu_relaxat.yaml | 14.39143 | 57048 |
| 3 | orar_mediu_relaxat.yaml | 13.88922 | 58285 |
| 4 | orar_mediu_relaxat.yaml | 44.91382 | 173413 |
| 5 | orar_mediu_relaxat.yaml | 29.70279 | 117318 |
| 1 | orar_mare_relaxat.yaml | 36.15732 | 100791 |
| 2 | orar_mare_relaxat.yaml | 35.45102 | 94873 |
| 3 | orar_mare_relaxat.yaml | 34.34551 | 95305 |
| 4 | orar_mare_relaxat.yaml | 34.94145 | 97808 |
| 5 | orar_mare_relaxat.yaml | 36.67619 | 98590 |
| 1 | orar_constrans_incalcat.yaml | - |  - |

For every test (except "orar_constrans_incalcat", because the heuristic doesn't converge), the implementation creates a timetable with **0 hard constrains and 0 soft constrains violations**.

## Conclusions

Overall the A* approach is more reliable, as it produces a valid timetable in less time and states and in a more deterministic manner.
The Hill-Climbing algorithm suffers from the randomness effect of the Stochastic variant and therefore doesn't make the best decision at every step, but rather hopes that at least one of the iterations will come up with a good enough result.
