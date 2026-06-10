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
    sorted_attendees = sorted(
        A,
        key=lambda a: len(avail[a] - mand[a])
    )

    # 3. Process attendees one at a time in order of availiability.
    for a in sorted_attendees:
      if len(assign[a]) >= need[a]:
            continue
      for m in avail[a]:
          if m in assign[a]:
                continue
          if len(roster[m]) < cap[m]:
                assign[a].add(m)
                roster[m].add(a)
          else:
                # Attempt to find a removable attendee.
                victim = displace(
                    m,
                    roster,
                    assign,
                    mand,
                    need
                )
                if victim is not None:
                    roster[m].remove(victim)
                    assign[victim].remove(m)

                    roster[m].add(a)
                    assign[a].add(m)
          if len(assign[a]) >= need[a]:
                break
    return assign, roster


def displace(m, roster, assign, mand, need):
    """
    Attempts to find someone who can safely lose meeting m.

    Returns:
        victim attendee
        OR
        None if nobody can be safely removed
    """
    candidates = []
    for b in roster[m]:
        # Never remove someone from a mandatory assignment.
        # If meeting m is mandatory for attendee b they are not allowed to be removed.
        if m in mand[b]:
            continue

        # Only remove attendee b if they would still satisfy their minimum meeting requirement afterward.
        if len(assign[b]) - 1 >= need[b]:
            candidates.append(b)

    if len(candidates) == 0:
        return None

    # Choose the attendee with the most flexibility
    victim = max(
        candidates,
        key=lambda b: len(assign[b])
    )
    return victim