import re
import itertools
import functools
import collections
import timeit
from enum import IntEnum

# ------- get input - one of three versions of data, two in files, one inline -------

lines_ex = '''
The first floor contains a hydrogen-compatible microchip, and a lithium-compatible microchip.
The second floor contains a hydrogen generator.
The third floor contains a lithium generator.
The fourth floor contains nothing relevant.
'''[1:-1].split('\n')  # split example in lines, keep line endings

input_version = 1
if input_version == 0:
    lines = lines_ex
else:
    input_file = 'input.txt' if input_version == 1 else 'input Teil2.txt'
    # example data needs 11 steps, 190 visited nodes
    # puzzle part 1 needs 37 steps, 0.296 secs, 4331 visited nodes
    # puzzle part 2 needs 61 steps, 1.5 sec, 15165 visited nodes
    #   CacheInfo(hits=236422, misses=9613, maxsize=None, currsize=9613)
    with open(input_file) as f:
        lines = f.readlines()  # # read complete file, results in list of lines with endings


# ------- parser ------
# assumption, not checked by code: for each material, we have exactly one generator and one microchip

items_start = dict()  # for each material, a tuple (position of generator, position of microchip) is stored here
for s, n in zip(lines, itertools.count()):
    s = s.rstrip('\n')
    r = re.sub(r"The .+ floor contains ", "", s)
    r = re.sub(r"[.]", "", r)
    r = re.sub(r"and ", "", r)
    r = re.sub(r"a ", "", r)
    r = re.sub(r"-compatible", "", r)
    things = r.split(", ")
    print(n, things)
    for thing in things:
        if thing == 'nothing relevant':
            break
        material, obj = thing.split(" ")
        # print(material, obj)
        if material not in items_start:
            items_start[material] = tuple()
        if obj == "generator":
            items_start[material] = (n,) + items_start[material]
        else:
            items_start[material] = items_start[material] + (n,)
print("---")


# -------------- solution ------------

# - BFS over the possible states of the system.
# - States and edges are calculated on the fly, since not all are visited.
# - Two states can be regarded as equal w.r.t. the search for a path with minimal length, if an
#   exchange of two materials leads from one to the other.
# This is used as follows:
# - A state is described by a tuple. For each material, it contains a tuple
#   (generator position, microchip position, material). These tuples are sorted.
# - For comparing states for the BFS, the material info is ignored (removed). This
#   does not invalidate the sorting. So, we get a normalized state for the comparison,
#   that does not depend on the concrete materials, but preserves structural information.
#   ("There is a pair of chip and generator on levels X and Y - material does not matter")
# - For pretty printing the found solution path, the material is still available in the state.

# Start state: elevator at level 0, items on levels acc. to puzzle
start_state = (0, tuple(sorted((pos1, pos2, material) for material, (pos1, pos2) in items_start.items())))
# Goal state: elevator at level 3, items on level 3
goal_state = (3, tuple(sorted((3, 3, material) for material, (pos1, pos2) in items_start.items())))


def hash_node(state):
    # Remove the material info from the state. Return a tuples as needed for hashing.
    elevator_pos, item_state = state
    return elevator_pos, tuple((pos1, pos2) for pos1, pos2, material in item_state)


def check_state_on_level(item_state, l):
    # No generators on this level --> ok
    # For all chips on this level, the matching generator is there, too --> ok
    return all(pos1 != l for (pos1, pos2, material) in item_state) or\
           all(pos2 != l or pos1 == l for (pos1, pos2, material) in item_state)


def next_states(state, visited):
    # Calculate possible next states according to the rules how the elevator works
    # and when a situation is allowed or not.
    # print(state)
    elevator_pos, item_state = state
    items_in_level = sum((1 if pos1 == elevator_pos else 0) + (1 if pos2 == elevator_pos else 0)
                         for (pos1, pos2, material) in item_state)
    # print(" number of items on the level:", items_in_level)
    for elev_goal in (e for e in (elevator_pos + 1, elevator_pos - 1) if 0 <= e <= 3):
        for move1 in range(items_in_level):  # Number of first item (within the level items) to move
            for move2 in range(move1+1, items_in_level+1, 1):  # Number of second item (one to high = no second move)
                # Change state by moving the move items and the elevator to the new elevator position
                counter = itertools.count()
                moves = (move1, move2)
                new_item_state = ((elev_goal if pos1 == elevator_pos and next(counter) in moves else pos1,
                                   elev_goal if pos2 == elevator_pos and next(counter) in moves else pos2,
                                   material)
                                  for (pos1, pos2, material) in item_state)
                new_item_state = tuple(sorted(new_item_state))
                new_state = (elev_goal, new_item_state)
                # Check new state for validity. If already visited, omit check (increases speed) and discard directly.
                if hash_node(new_state) not in visited \
                        and check_state_on_level(new_item_state, elev_goal) \
                        and check_state_on_level(new_item_state, elevator_pos):
                    # print("yield:", state, new_state)
                    yield new_state


def describe_solution(path):
    # Pretty print the solution path: Compare states and display the changes between them.
    for old_state, new_state in zip(path, path[1:]):
        old_elev, old_item_state = old_state
        new_elev, new_item_state = new_state
        item_info = [(("generator " + n_pos_m, o_pos_g, n_pos_g), ("microchip " + n_pos_m, o_pos_c, n_pos_c))
                     for (o_pos_g, o_pos_c, o_pos_m), (n_pos_g, n_pos_c, n_pos_m)
                     in zip(old_item_state, new_item_state)]
        item_info = itertools.chain(*item_info)
        item_names = [i for i, o_pos, n_pos in item_info if o_pos != n_pos]
        print("from level", old_elev, "to level", new_elev, "move:", item_names)


def breadth_first_search(*, start, is_goal, get_neighbors, hash_node):
    # similar to: https://johnlekberg.com/blog/2020-01-01-cabbage-goat-wolf.html
    predecessor = dict()
    to_visit = [start]
    visited = {hash_node(start)}
    no_visited = 0
    while to_visit:
        vertex = to_visit.pop(0)
        no_visited += 1
        if is_goal(vertex):
            path = []
            while vertex is not None:
                path.insert(0, vertex)
                vertex = predecessor.get(vertex)
            return path, no_visited
        for neighbor in get_neighbors(vertex, visited):
            node_hash = hash_node(neighbor)
            if node_hash not in visited:
                visited.add(node_hash)
                predecessor[neighbor] = vertex
                to_visit.append(neighbor)


# ------ start search -------
start = timeit.default_timer()
path, no_visited = breadth_first_search(start=start_state, is_goal=goal_state.__eq__,
                                        get_neighbors=next_states, hash_node=hash_node)
stop = timeit.default_timer()
if path is None:
    raise RuntimeError("solution not found")
print('Time: ', stop - start)
print("-- finished with distance", len(path) - 1, "--")
describe_solution(path)
print("Visited nodes:", no_visited)