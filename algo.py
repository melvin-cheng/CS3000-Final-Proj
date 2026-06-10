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

    seats_left = {m: cap[m] - len(roster[m]) for m in M}

    """
    How much each seat is worth: a person's 1st meeting is worth far more than their 
    2nd, the 2nd more than the 3rd, and so on. Using a base bigger than the
    number of attendees makes "cover one more person" always outweigh 
    "give someone an extra meeting", so coverage wins first and depth second.
    """
    base = len(A) + 1
    need_max = max(need(a) for a in A)
    seat_weight = [base ** (need_max - rank) for rank in range(1, need_max + 1)]

     # describe each person and how many people they have
    people = []
    for a in A:
        already_assigned = len(mand[a])
        room = max(0, need[a] - already_assigned)  # how many more meetings a needs to be satisfied
        options = sorted(avail[a] - mand[a]) # meetings a can still be assigned to
        people.append((a, already_assigned, room, options))

    meetings = sorted(M)
    seats_tuple = tuple(seats_left[m] for m in meetings)
    hold = {}
    choice = {}
    best_score(0, seats_tuple, people, meetings, seat_weight, hold, choice)
 
    # 3. replay the recorded best choices to build the actual assignment
    seats = list(seats_tuple)
    for i in range(len(people)):
        attendee = people[i][0]
        for m in choice[(i, tuple(seats))]:
            assign[attendee].add(m)
            roster[m].add(attendee)
            seats[meetings.index(m)] -= 1
 
    return assign, roster

def seat_reward(already_have, extra_meetings, seat_weight):
    """
    total worth of giving a person `extra_meetings` more metings when they already
    hold `already_have`. Adds up the per seat weights for the new seats which get
    smaller as a person collects more
    """
    total = 0
    for rank in range(already_have + 1, already_have + extra_meetings + 1):
        total += seat_weight[rank - 1]
    return total

def best_score(i, seats, people, meetings, seat_weight, hold, choice):
    """
    Largest total score possible from person i onward given the open seats
    Fills hold[...] and choice[...] along the way.

    Returns:
        the score for this situation
    """
    # no ppl left to place
    if i == len(people):
        return 0

    state = (i, seats)
    if state in hold:          # already solved
        return hold[state]

    attendee, already_have, room, options = people[i]

    # give this person no extra meetings
    best = best_score(i + 1, seats, people, meetings, seat_weight, hold, choice)
    best_meetings = ()

    # give them 1..room extra meetings trying each set of open meetings
    for extra_meetings in range(1, min(room, len(options)) + 1):
        gain = seat_reward(already_have, extra_meetings, seat_weight)
        for chosen in combinations(options, extra_meetings):
            # the chosen meetings must all still have a seat free
            if all(seats[meetings.index(m)] > 0 for m in chosen):
                # use one seat in each chosen meeting then solve everyone after
                remaining = list(seats)
                for m in chosen:
                    remaining[meetings.index(m)] -= 1
                score = gain + best_score(i + 1, tuple(remaining), people, 
                                          meetings, seat_weight, hold, choice)
                if score > best:
                    best = score
                    best_meetings = chosen

    hold[state] = best
    choice[state] = best_meetings
    return best