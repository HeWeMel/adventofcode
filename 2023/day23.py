import functools
from collections import defaultdict
from collections.abc import Iterable, Sequence

from mylib.aoc_frame2 import Day
import nographs as nog


moves = nog.Position.moves()
gliding = {direction_char: move
           for direction_char, move in zip("^<>v", moves)}


def paths(a: nog.Array, start: nog.Position, on_path: set[nog.Position],
          length_so_far: int,
          moves: Iterable[Sequence[int]], goals: set[nog.Position],
          limits,
          check_directions: bool = True
          ) -> Iterable[tuple[nog.Position, int, Sequence[int]]]:
    """
    Yield paths suffixes starting at *start*, ending in a goals position,
    vertices on_path (on the current path to start) are forbidden, and knowing
    the length of the path so far (to start). Report a path with tuple
    (goal position, length of the total path to it, last move to it).
    """
    # print(start)
    my_moves = moves
    c = a[start]
    if check_directions:
        if c in gliding.keys():
            my_moves = [gliding[c]]

    for move in my_moves:
        p2 = start + move
        # print(">>", p2, limits)
        if not p2.is_in_cuboid(limits):
            continue
        if p2 in on_path:
            continue
        c2 = a[p2]
        if c2 == "#":
            continue
        if p2 in goals:
            yield p2, length_so_far + 1, move
            continue
        on_path.add(p2)
        results = list(paths(a, p2, on_path, length_so_far + 1, moves, goals, limits,
                             check_directions))
        on_path.remove(p2)
        yield from results


def longest_path_from_segments(
        segments: dict,
        start: nog.Position, goal: nog.Position,
) -> tuple[int, list[nog.Position]]:
    """ Combine the path segments to a longest path from start to goal. """

    # @functools.cache
    def do_recursive(start: nog.Position, goal: nog.Position,
                     on_path: frozenset[nog.Position]
                     ) -> tuple[int, list[nog.Position]]:
        if start == goal:
            return 0, []
        longest = -1
        longest_path = []
        for p2, length in segments[start].items():
            if p2 in on_path:
                continue

            longest_p2, path_to_p2 = do_recursive(
                p2, goal, on_path | {p2}
            )
            if longest_p2 == -1:
                continue

            longest_p2 += length
            if longest < longest_p2:
                longest = longest_p2
                longest_path = path_to_p2
                longest_path.insert(0, start)
        return longest, longest_path
    return do_recursive(start, goal, frozenset())


def parse(text: str):
    a = nog.Array(text.splitlines())
    a = a.mutable_copy()
    moves = nog.Position.moves()
    limits = a.limits()

    size_y, size_x = a.size()
    start = nog.Position((0, 1))
    goal = nog.Position((size_y - 1, size_x - 2))

    directions = "^v<>"

    junctions = [start, goal]
    for pos, content in a.items():
        gliders = 0
        for neighbors in pos.neighbors(moves, limits):
            if a[neighbors] in directions:
                gliders += 1
        if gliders >= 3:
            junctions.append(pos)

    return a, moves, set(junctions), start, goal, limits


class PartA(Day):
    check_directions = True

    def compute(self, text, config):
        a, moves, junctions, start, goal, limits = parse(text)

        segment_length = defaultdict(dict)
        for segment_start in junctions:
            for pos, length, move in paths(
                    a, segment_start, {segment_start}, 0,
                    moves, junctions, limits, check_directions=self.check_directions):
                segment_length[segment_start][pos] = length

        length, path = longest_path_from_segments(segment_length, start, goal)
        return length

    def tests(self):
        yield self.test_solve(example), 94, "example"


class PartB(PartA):
    check_directions = False

    def tests(self):
        yield self.test_solve(example), 154, "example"


example = '''
#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#
'''

Day.do_day(day=23, year=2023, part_a=PartA, part_b=PartB)
