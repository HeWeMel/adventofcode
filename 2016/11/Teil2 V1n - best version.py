import sys
import re
import itertools
import functools
import collections
import timeit
from enum import IntEnum
from functools import partial

with open('input Teil2.txt') as f:
    # puzzle part 2 needs 61 steps, 2.2534416999999998 sec
    # CacheInfo(hits=236422, misses=9613, maxsize=None, currsize=9613)
# with open('input.txt') as f:
    # puzzle part 1 needs 37 steps, 0.31746 secs
    lines = f.readlines()  # # read complete file, results in list of lines with endings

lines_ex = '''
The first floor contains a hydrogen-compatible microchip, and a lithium-compatible microchip.
The second floor contains a hydrogen generator.
The third floor contains a lithium generator.
The fourth floor contains nothing relevant.
'''[1:-1].split('\n')  # split example in lines, keep line endings

#------- parser ------

Object = IntEnum("Obj", ["generator", "microchip"])
Item = collections.namedtuple('Item', ['material', 'obj', 'name', 'start_pos'])  # new class
items = []
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
        items.append(Item(material, Object[obj], thing, n))
print("---")

# -------------- solution ------------

items = sorted(items)  # for each material come its generator and microchip
start_state = (0, tuple(item.start_pos for item in items))  # elevator at level 0, items on levels acc. to puzzle
goal_state = (3, len(items) * (3,))  # elevator and all items are on level 3


# For each material of items, list the pair of positions of its generator and its microchip.
# This relies on the special sorting of the items, see above!
def pos_tuples_for_materials(item_state):
    items_with_pairing_mark = zip(itertools.cycle((True, False)), item_state)
    generators = (pos for even, pos in items_with_pairing_mark if even)
    microchips = (pos for even, pos in items_with_pairing_mark if not even)
    return zip(generators, microchips)


def hash_node(state):
    # Two states can be regarded as equal w.r.t. the search for a path with minimal length,
    # if an exchange of two materials leads from one to the other. Thus, a state is
    # normalized to a state in that the materials are sorted by a fixed sorting.
    elevator_pos, item_state = state
    return elevator_pos, tuple(sorted(pos_tuples_for_materials(item_state)))


@functools.cache
def check_level_item_configuration(item_selector):
    # Configuration is tuple of true/false values denoting whether the item is in the configuration.
    # This allows for level-independent caching.
    generators_in_level = frozenset(
        item.material for selector, item in zip(item_selector, items) if selector and item.obj is Object.generator)
    # no generators on this level --> ok
    if len(generators_in_level) == 0:
        return True
    # for all chips on this level, the matching generator is there, too --> ok
    chips_in_level = frozenset(
        item.material for selector, item in zip(item_selector, items) if selector and item.obj is Object.microchip)
    return chips_in_level.issubset(generators_in_level)


def check_state_on_level(state, l):
    elevator_pos, item_state = state
    # calculate the item configuration on this level and check it
    return check_level_item_configuration(tuple(pos == l for pos in item_state))


def next_states(state, visited):
    elevator_pos, item_state = state
    items_in_level = [item_no for item_no, pos, item
                      in zip(itertools.count(0), item_state, items)
                      if pos == elevator_pos]
    # print(" items here:", items_in_level)
    move_item_candidates = list(itertools.combinations(items_in_level, 2))  # move two items
    move_item_candidates.extend(zip(items_in_level))  # or move one object (pack each item in one-item tuple)
    # print(" move item options", move_item_options)
    for elev_goal in [elevator_pos + 1, elevator_pos - 1]:
        if elev_goal < 0 or elev_goal > 3:
            continue
        for move_items in move_item_candidates:
            # change item state by moving the move items and the elevator to the new elevator position
            new_state = (elev_goal,
                         tuple(elev_goal if item_no in move_items else pos
                               for item_no, pos in zip(itertools.count(0), item_state)))
            if hash_node(new_state) not in visited \
                    and check_state_on_level(new_state, elev_goal) \
                    and check_state_on_level(new_state, elevator_pos):
                # print(" add move with", move_items, "to", new_state)
                yield new_state


def describe_solution(path):
    for old, new in zip(path, path[1:]):
        old_elev, old_item_state = old
        new_elev, new_item_state = new
        item_names = [item.name for item, oldpos, newpos
                      in zip(items, old_item_state, new_item_state) if oldpos != newpos]
        print("from level", old_elev, "to level", new_elev, "move:", item_names)


def breadth_first_search(*, start, is_goal, get_neighbors):
    # similar to: https://johnlekberg.com/blog/2020-01-01-cabbage-goat-wolf.html
    predecessor = dict()
    to_visit = [start]
    visited = {start}
    while to_visit:
        vertex = to_visit.pop(0)
        if is_goal(vertex):
            path = []
            while vertex is not None:
                path.insert(0, vertex)
                vertex = predecessor.get(vertex)
            return path
        for neighbor in get_neighbors(vertex, visited):
            if neighbor not in visited:
                visited.add(hash_node(neighbor))
                predecessor[neighbor] = vertex
                to_visit.append(neighbor)


start = timeit.default_timer()
path = breadth_first_search(start=start_state, is_goal=goal_state.__eq__, get_neighbors=next_states)
stop = timeit.default_timer()
if path is None:
    raise RuntimeError("solution not found")
print('Time: ', stop - start)
print("-- finished with distance", len(path) - 1, "--")
# 61
describe_solution(path)

print(check_level_item_configuration.cache_info())
