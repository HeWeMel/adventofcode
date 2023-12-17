from typing import Iterable
from mylib.aoc_frame2 import Day
import nographs as nog

State = tuple[nog.Position, nog.Position]  # position, previous direction


def parse(text: str):
    a = nog.Array(text.splitlines())
    limits = a.limits()
    moves = nog.Position.moves()
    start_position = nog.Position((0, 0))
    goal_position = nog.Position((limits[0][1]-1, limits[1][1]-1))
    return a, limits, moves, start_position, goal_position


class PartA(Day):
    max_in_same_direction = 3
    min_in_same_direction = 1

    def compute(self, text, config):
        def next_edges(state: State, _) -> Iterable[tuple[State, int]]:
            pos, prev_direction = state
            for direction in moves:
                direction = nog.Position(direction)
                if direction == prev_direction or direction == prev_direction * -1:
                    # need to be a turn, and 180 degree turns are forbidden
                    continue
                pos_to = pos
                weight = 0
                for jump_length in range(1, self.max_in_same_direction + 1):
                    pos_to += direction
                    if not pos_to.is_in_cuboid(limits):
                        break
                    weight += int(a[pos_to])
                    if jump_length >= self.min_in_same_direction:
                        yield (pos_to, direction), weight

        a, limits, moves, start_position, goal_position = parse(text)
        t = nog.TraversalShortestPaths(next_edges)
        for pos, prev_direction in t.start_from(
               (start_position, nog.Position((0, 0)))):
            if pos == goal_position:
                return t.distance
        raise RuntimeError()

    def tests(self):
        yield self.test_solve(example, None), 102, "example"


class PartB(PartA):
    max_in_same_direction = 10
    min_in_same_direction = 4

    def tests(self):
        yield self.test_solve(example, None), 94, "example"


example = '''
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
'''

Day.do_day(day=17, year=2023, part_a=PartA, part_b=PartB)
