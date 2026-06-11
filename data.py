"""
Mock dataset for testing allocate()

7 people compete for 5 total seats across 3 meetings, so demand exceeds the supply and not everyone can be placed. This is the case where the fairness weighting matters and the algorithm has to choose who gets a seat.

Import into a test with:  from data import M, cap, A, avail, mand, need
"""

# 3 meetings, 5 seats total
M = ["mon", "tue", "wed"]
cap = {
    "mon": 2,
    "tue": 2,
    "wed": 1,
}

# 7 attendees, so 7 people chase 5 seats (oversubscribed by 2)
A = ["p1", "p2", "p3", "p4", "p5", "p6", "p7"]

# meetings each person can attend.
# p2/p4/p7 are "constrained" — only one option each — so they test whether
# the algorithm protects people who have nowhere else to go.
avail = {
    "p1": {"mon", "tue"},
    "p2": {"mon"},            # only mon
    "p3": {"mon", "wed"},
    "p4": {"tue"},            # only tue
    "p5": {"tue", "wed"},
    "p6": {"mon", "tue", "wed"},
    "p7": {"wed"},            # only wed
}

# no one is required for any meeting in this scenario
mand = {a: set() for a in A}

# everyone just needs 1 meeting to count as satisfied
need = {a: 1 for a in A}
