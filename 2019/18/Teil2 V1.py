import itertools
import collections
from heapq import *
import timeit


def parse(puzzle_raw):
    # read puzzle as given, create list of strings
    puzzle = [s.rstrip('\n') for s in puzzle_raw]
    #  for line in puzzle:
    #      print(line)
    return puzzle


def distances_to_goals(*, start, is_goal, get_neighbors):
    # BFS, many goals, save distance to each reached goal
    distances = dict()
    to_visit = [(start, 0)]
    visited = {start}
    while to_visit:
        vertex, distance = to_visit.pop(0)
        distance += 1
        for neighbor in get_neighbors(vertex):
            if neighbor not in visited:
                visited.add(neighbor)
                if is_goal(neighbor):
                    distances[neighbor] = distance
                else:
                    to_visit.append((neighbor, distance))
    return distances


def all_distances(puzzle):
    # create and return dict (position, content): [ (position2, content2), # steps from 1 to 2 ]
    sy = len(puzzle)
    sx = len(puzzle[0])

    def is_goal(state):
        x, y = state
        return puzzle[y][x] != '.'


    def get_neighbors(state):
        xs, ys = state
        return ((x,y) for x, y in ((xs-1, ys),(xs+1, ys),
         (xs, ys-1),(xs, ys+1))
         if puzzle[y][x] != '#'
        )

    # Find places in puzzle that is neither "#" nor ".".
    # For solving the puzzle, these will be the nodes.
    distances = dict()
    for y in range(sy):
        for x in range(sx):
            c = puzzle[y][x]
            if c in ('#', '.'):
                continue
            # Calculate distance from each node to all other nodes that can be
            # directly reached in the puzzle without passing an other node.
            c_distances = distances_to_goals(
                start=(x, y), is_goal=is_goal, get_neighbors=get_neighbors
            )
            distances[((x, y), puzzle[y][x])] = [
                (((x, y), puzzle[y][x]),
                 d)
                for (x, y), d in c_distances.items()
            ]
    print("distances in puzzle determined")
    # print("distances in puzzle:", distances)
    return distances
# ------------------------------


def calculate_distance_to_a_goal(starting_vertex, is_goal, get_neighbors):
    # Dijkstra, one starting node, goal node predicate, neighbors generating function
    # ---
    # Vertices without stored distance are seen as having infinite distance to starting vertex so far.
    # Pre-initialization for all nodes would be faster than extending the dict during the search, but
    # in this way, we can generate nodes on the fly.
    distances = collections.defaultdict(lambda: float('infinity'))
    # At start, only the distance 0 from the starting vertex to itself is known.
    distances[starting_vertex] = 0
    pred = {}
    pq = [(0, starting_vertex)]
    while pq:
        current_distance, current_vertex = heappop(pq)
        # print(">>", current_vertex, current_distance)
        if is_goal(current_vertex):
            return current_distance, current_vertex, pred

        # Nodes can get added to the priority queue multiple times. We only
        # process a vertex the first time we remove it from the priority queue.
        if current_distance > distances[current_vertex]:
            continue

        for neighbor, weight in get_neighbors(current_vertex):
            distance = current_distance + weight

            # Only consider this new path if it's better than any path we've
            # already found.
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heappush(pq, (distance, neighbor))
                pred[neighbor] = current_vertex

    raise RuntimeError

# ------------------------------


def solve(puzzle_id, puzzle_raw):
    start = timeit.default_timer()

    # For nonempty fields in puzzle, create relation to directly reachable other such fields
    # as dict (position, content): [ (position2, content2), # steps from 1 to 2 ]
    # This is used as new edge relation in the sense of an edge contraction.
    puzzle = parse(puzzle_raw)
    direct_distances = all_distances(puzzle)

    # Create graph to search in for solving the puzzle
    # Nodes: ((((x,y),c)..), (keys)) where ((x, y),c) are nonempty fields in the puzzle, one for each robot
    # Edges: node to node2 with distance d, if for one of the robots, ((x,y),c) to ((x2,y2),c2) is in direct distances
    #        and the keys respect the rules for getting and using keys for this step of this robot
    number_of_keys = 0
    starting_pos = []
    for pos, element in direct_distances:
        if element == '@':
            starting_pos.append((pos, element))
        elif str.lower(element) == element:  # lowercase means key:
            number_of_keys += 1
    # print("keys", number_of_keys)
    no_of_robots = len(starting_pos)
    starting_vertex = (tuple(starting_pos), ())
    # print("start", starting_vertex)
    def is_goal(state):
        pos_and_elems, keys = state
        return len(keys) == number_of_keys
    def get_neighbors(state):
        s_pos_elems, s_keys = state
        for robot in range(no_of_robots):
            s_pos_element = s_pos_elems[robot]
            for neighbor, weight in direct_distances[s_pos_element]:
                # print("neighbor", state, neighbor, weight)
                pos, element = neighbor
                keys = s_keys
                if 'a' <= element <= 'z':  # key
                    if all(key != element for key in s_keys):
                        # print("got new key")
                        keys = tuple(sorted(s_keys + (element,)))
                elif 'A' <= element <= 'Z':  # door
                    needed_key = element.lower()
                    if all(key != needed_key for key in s_keys):
                        # print("refused because no key")
                        continue  # door needs its key, but we do not have it -> no way
                elif element != '@':
                    raise RuntimeError
                pos_elems = tuple(neighbor if i == robot else s_pos_element
                                  for s_pos_element, i in zip(s_pos_elems, itertools.count()))
                yield (pos_elems, keys), weight

    current_distance, current_vertex, pred =\
        calculate_distance_to_a_goal(starting_vertex=starting_vertex,
                                     is_goal=is_goal, get_neighbors=get_neighbors)
    stop = timeit.default_timer()
    print("result for puzzle", puzzle_id, ":", current_distance)
    print('Time: ', stop - start)
    return current_distance


def solve_and_check(puzzle_id, puzzle, correct_result):
    result = solve(puzzle_id, puzzle)
    if result != correct_result:
        print("puzzle", puzzle_id, ": result", result,
              "instead of correct", correct_result)
        raise RuntimeError()
    print("------------------------------------------")


# -----------------------------------------

puzzle='''
#########
#b.A.@.a#
#########
'''[1:-1].split('\n')   # split example in lines, keep line endings
solve_and_check(1, puzzle, 8)


puzzle='''
########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################
'''[1:-1].split('\n')   # split example in lines, keep line endings
solve_and_check(2, puzzle, 86)

puzzle='''
########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################
'''[1:-1].split('\n')   # split example in lines, keep line endings
solve_and_check(3, puzzle,132)

with open('input.txt') as f:
    puzzle = f.readlines()  # read complete file, results in list of lines with endings
    solve_and_check(101, puzzle, 4228)
    #  result: 4228
    #  Time: 1.2256293 sec org version without multiple robots
    #  Time: 1.810678 sec this version
    #  (1.3386294 sec would be possible for this version if tuple nesting would be omitted for on robot case)

puzzle='''
#######
#a.#Cd#
##@#@##
#######
##@#@##
#cB#Ab#
#######
'''[1:-1].split('\n')   # split example in lines, keep line endings
solve_and_check(5, puzzle,8)

puzzle='''
###############
#d.ABC.#.....a#
######@#@######
###############
######@#@######
#b.....#.....c#
###############
'''[1:-1].split('\n')   # split example in lines, keep line endings
solve_and_check(9, puzzle,24)

puzzle='''
#############
#DcBa.#.GhKl#
#.###@#@#I###
#e#d#####j#k#
###C#@#@###J#
#fEbA.#.FgHi#
#############
'''[1:-1].split('\n')   # split example in lines, keep line endings
solve_and_check(10, puzzle,32)

puzzle='''
#############
#g#f.D#..h#l#
#F###e#E###.#
#dCba@#@BcIJ#
#############
#nK.L@#@G...#
#M###N#H###.#
#o#m..#i#jk.#
#############
'''[1:-1].split('\n')   # split example in lines, keep line endings
solve_and_check(11, puzzle,72)

with open('input2.txt') as f:
    puzzle = f.readlines()  # read complete file, results in list of lines with endings
    solve_and_check(102, puzzle, 1858)
    #  result: 1858
    #  Time: 161.7248779 sec
