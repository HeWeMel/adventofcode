from collections.abc import Iterable

from mylib.aoc_frame2 import Day
import nographs as nog


def parse(text: str):
    """Compute the start position and the maze (as possible moves for each position)"""
    a_org = nog.Array(text.splitlines())
    limits = a_org.limits()
    s = a_org.findall("S")[0]

    # Compute the possible walking directions based on the pipes and the limits of the
    # maze
    deltas_for_c = {
        # | is a vertical pipe connecting north and south.
        "|": [(-1, 0), (1, 0)],
        # - is a horizontal pipe connecting east and west.
        "-": [(0, -1), (0, +1)],
        # L is a 90 - degree bend connecting north and east.
        "L": [(-1, 0), (0, 1)],
        # J is a 90 - degree bend connecting north and west.
        "J": [(-1, 0), (0, -1)],
        # 7 is a 90 - degree bend connecting south and west.
        "7": [(1, 0), (0, -1)],
        # F is a 90 - degree bend connecting south and east.
        "F": [(1, 0), (0, 1)],
    }
    maze_of_deltas = {pos: [d for d in deltas_for_c.get(c, [])
                            if (pos + d).is_in_cuboid(limits) ]
                      for pos, c in a_org.items()}

    # Compute the possible walking directions for the start vertex based
    # on the walking directions of the neighboring fields
    deltas_of_start = []
    for neighbor_of_start in s.neighbors(nog.Position.moves(), limits=limits):
        for delta in maze_of_deltas[neighbor_of_start]:
            if s == neighbor_of_start + delta:
                # We found a step from a neighbor back to the start.
                # Add it in the opposite direction as possible step from the start
                deltas_of_start.append(neighbor_of_start - s)
    maze_of_deltas[s] = deltas_of_start

    return s, maze_of_deltas, limits


def find_cycle(s, maze_of_deltas):
    """Return cycle from start s through the maze. Try to compute a topological
    sorting of the maze from s, this fails due to the cycle, and the found cycle
    can be used as result"""
    def next_vertices(pos: nog.Position, t: nog.TraversalTopologicalSort
                      ) -> Iterable[nog.Position]:
        """Report vertices that we reach by using one of the pipes from *pos*,
        except for the vertex we directly came from"""
        # The following line works with a future version of NoGraphs:
        predecessor = t.paths.predecessor(pos)  # None, if the path is empty
        # # The following code works for NoGraphs-3.3.1:
        # path_backwards = t.paths.iter_edges_to_start(pos)
        # try:
        #     predecessor, _ = next(path_backwards)
        # except StopIteration:
        #     predecessor = None
        for delta in maze_of_deltas[pos]:
            if (next_pos := pos + delta) != predecessor:
                yield next_pos

    t = nog.TraversalTopologicalSort(next_vertices)
    try:
        for v in t.start_from(s, build_paths=True):
            pass
        raise ValueError("No cycle found")
    except RuntimeError:  # We have found a cycle
        pass
    return t.cycle_from_start


class PartA(Day):
    def compute(self, text, config):
        s, maze_of_deltas, _ = parse(text)
        cycle = find_cycle(s, maze_of_deltas)
        nr_of_steps = len(cycle) - 1  # cycle starts and ends with the start vertex
        return nr_of_steps // 2

    def tests(self):
        """ Yield testcases as tuple: (test_result, correct_result [, test_name]) """
        yield self.test_solve(example_a1, "config"), 4, "example1"
        yield self.test_solve(example_a2, "config"), 8, "example2"


class PartB(PartA):
    def compute(self, text, config):
        """Iterate through each line. Count fields within the boundary given by the
        cycle. I cycle field containing (the start of) a vertical pipe upwards or
        downwards toggles flags in these directions. As long as both flags are set,
        each found non-cycle field counts for the result."""
        s, maze_of_deltas, limits = parse(text)
        cycle = find_cycle(s, maze_of_deltas)

        half_ins = {-1: False, 0: False, 1: False}  # Only keys != 0 are relevant
        in_tiles = 0
        for pos, deltas in maze_of_deltas.items():
            if pos in cycle:
                for y_delta, x_delta in deltas:
                    half_ins[y_delta] = not half_ins[y_delta]
            else:
                if half_ins[-1] and half_ins[1]:
                    in_tiles += 1
        return in_tiles

    def tests(self):
        """ Yield testcases as tuple: (test_result, correct_result [, test_name]) """
        yield self.test_solve(example_b1, "config"), 4, "example2"
        yield self.test_solve(example_b2, "config"), 8, "example2"


example_a1 = '''
.....
.S-7.
.|.|.
.L-J.
.....
'''

example_a2 = '''
..F7.
.FJ|.
SJ.L7
|F--J
LJ...
'''


example_b1 = '''
...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........
'''


example_b2 = '''
.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
'''


Day.do_day(day=10, year=2023, part_a=PartA, part_b=PartB)
