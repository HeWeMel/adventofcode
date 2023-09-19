import itertools
import collections
import timeit
import nographs as nog


def parse(puzzle_raw):
    # read puzzle as given, create list of strings
    puzzle = [s.rstrip('\n') for s in puzzle_raw]
    #  for line in puzzle:
    #      print(line)
    return puzzle


def distances_between_nonempty_fields(puzzle):
    # create and return dict (position, content): [ (position2, content2), # steps from 1 to 2 ]
    # Find places in puzzle that is neither "#" nor ".".
    # For solving the puzzle, these will be the nodes.
    sy = len(puzzle)
    sx = len(puzzle[0])
    distances = collections.defaultdict(list)

    def get_neighbors(vertex, p_traversal: nog.TraversalBreadthFirst):
        (xs, ys) = vertex
        if p_traversal.depth > 0 and puzzle[ys][xs] != '.':  # stop at first nonempty field
            return
        for xd, yd in ((-1, 0), (+1, 0), (0, -1), (0, +1)):
            y2, x2 = ys + yd, xs + xd
            if puzzle[y2][x2] != '#':
                yield x2, y2

    for y in range(sy):
        for x in range(sx):
            c = puzzle[y][x]
            if c in ('#', '.'):
                continue
            # Calculate distance from each node to all other nodes that can be
            # directly reached in the puzzle without passing an other node.
            pos = (x, y)
            traversal = nog.TraversalBreadthFirst(get_neighbors)
            for vertex in traversal.start_from(pos):
                pos_i, edge_count_i = vertex, traversal.depth
                x_i, y_i = pos_i
                c_i = puzzle[y_i][x_i]
                if c_i != '.':  # goal
                    distances[(pos, c)].append(((pos_i, c_i), edge_count_i))
    print("distances in puzzle determined")
    # print("distances in puzzle:", distances)
    return distances


def solve(puzzle_id, puzzle_raw):
    start = timeit.default_timer()

    # For nonempty fields in puzzle, create relation to directly reachable other such fields
    # as dict (position, content): [ (position2, content2), # steps from 1 to 2 ]
    # This is used as new edge relation in the sense of an edge contraction.
    puzzle = parse(puzzle_raw)
    direct_distances = distances_between_nonempty_fields(puzzle)

    # Create graph to search in for solving the puzzle
    # Nodes: ((((x,y),c)..), (keys)) where ((x, y),c) are nonempty fields in the puzzle, one for
    #        each robot
    # Edges: node to node2 with distance d, if for one of the robots, ((x,y),c) to ((x2,y2),c2) is
    #        in direct distances and the keys respect the rules for getting and using keys for this
    #        step of this robot
    number_of_keys = 0
    starting_pos = []
    for pos, element in direct_distances:
        if element == '@':
            starting_pos.append((pos, element))
        elif str.lower(element) == element:  # lowercase means key:
            number_of_keys += 1
    # print("keys", number_of_keys)
    no_of_robots = len(starting_pos)
    # print("robots", no_of_robots)
    start_state = (tuple(starting_pos), ())
    # print("start", start_state)

    def next_edges(vertex, _):
        s_pos_elems, s_keys = vertex
        edges = []
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
                edges.append( ((pos_elems, keys), weight) )
        return edges

    traversal = nog.TraversalShortestPaths(next_edges)
    for vertex in traversal.start_from(start_state, build_paths=False):
        pos_and_elems, keys = vertex
        if len(keys) == number_of_keys:
            break
    else:
        raise RuntimeError()
    stop = timeit.default_timer()
    print("result for puzzle", puzzle_id, ":", traversal.distance)
    print('Time: ', stop - start)
    return traversal.distance


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
solve_and_check(3, puzzle, 132)

with open('input.txt') as f:
    puzzle = f.readlines()  # read complete file, results in list of lines with endings
    solve_and_check(101, puzzle, 4228)
    #  result: 4228
    #  Time: 1.2256293 sec org version without multiple robots
    #  Time: 1.810678 sec this version

puzzle='''
#######
#a.#Cd#
##@#@##
#######
##@#@##
#cB#Ab#
#######
'''[1:-1].split('\n')   # split example in lines, keep line endings
solve_and_check(5, puzzle, 8)

puzzle='''
###############
#d.ABC.#.....a#
######@#@######
###############
######@#@######
#b.....#.....c#
###############
'''[1:-1].split('\n')   # split example in lines, keep line endings
solve_and_check(9, puzzle, 24)

puzzle='''
#############
#DcBa.#.GhKl#
#.###@#@#I###
#e#d#####j#k#
###C#@#@###J#
#fEbA.#.FgHi#
#############
'''[1:-1].split('\n')   # split example in lines, keep line endings
solve_and_check(10, puzzle, 32)

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
solve_and_check(11, puzzle, 72)

with open('input2.txt') as f:
    puzzle = f.readlines()  # read complete file, results in list of lines with endings
    solve_and_check(102, puzzle, 1858)
    #  result: 1858
    '''
    distances in puzzle determined
    result for puzzle 102 : 1858
    Time:  124.49655390000001
    '''
