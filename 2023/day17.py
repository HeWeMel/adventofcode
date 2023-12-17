from typing import Iterable
from mylib.aoc_frame2 import Day
import nographs as nog

State = tuple[nog.Position, nog.Position, int]  # position, previous direction, count


def parse(text: str):
    a = nog.Array(text.splitlines())
    limits = a.limits()
    moves = nog.Position.moves()
    start_position = nog.Position((0, 0))
    goal_position = nog.Position((limits[0][1]-1, limits[1][1]-1))
    return a, limits, moves, start_position, goal_position


class PartA(Day):
    max_in_same_direction = 3
    min_in_same_direction = 0

    def compute(self, text, config):
        def next_edges(state: State, _) -> Iterable[tuple[State, int]]:
            pos, prev_direction, prev_count = state
            for pos_to in pos.neighbors(moves, limits):
                d = pos_to - pos
                if d == prev_direction * -1:
                    # turn forbidden
                    continue
                if d == prev_direction and prev_count == self.max_in_same_direction:
                    # to much steps in this direction
                    continue
                if prev_direction != d and prev_count < self.min_in_same_direction:
                    # d is a turn - but there are not enough straight moves so far
                    continue
                yield ((pos_to, d, prev_count + 1 if d == prev_direction else 1),
                       int(a[pos_to]))

        a, limits, moves, start_position, goal_position = parse(text)
        t = nog.TraversalShortestPaths(next_edges)
        for pos, prev_direction, prev_count in t.start_from(
               (start_position, nog.Position((0, 0)), 5)):
            if pos != goal_position:
                continue
            if prev_count < self.min_in_same_direction:
                # there need to be 5 consecutive steps in the same direction
                continue
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
