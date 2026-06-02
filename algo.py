"""
ALLOCATE — assigns attendees to meetings without exceeding capacity.
 1. Place all required attendees in their mandatory meetings first.
 2. Then place everyone else, handling the most-constrained attendees (those with the fewest available meetings) first.
 3. If a meeting is full, bump a lower-priority member to make room — but only if that person already has another meeting, so no one
 ends up unassigned.
 Result: capacities are respected, required attendees are guaranteed their spots, and seats go to whoever needs them most.
"""


def allocate(M, cap, A, avail, mand, need):
    """
    M        : array of meetings
    cap[m]   : capacity of meeting m
    A        : array of attendees
    avail[a] : meetings a can attend (from their submitted availability)
    mand[a]  : meetings a is REQUIRED for (subset of avail[a]; usually empty)
    need[a]  : min meetings a must keep to count as "satisfied" (default 1)
  OUTPUT
    assign[a] : meetings assigned to a   |  roster[m] : attendees assigned to m
    """
    assign = {a: set() for a in A}
    roster = {m: set() for m in M}

    # 1. place all required attendees in their mandatory meetings first
    for a in A:
        for m in mand[a]:
            assign[a].add(m)
            roster[m].add(a)

    # 2. place everyone else, handling the most-constrained attendees first
    # (those with the fewest available meetings)
    


    