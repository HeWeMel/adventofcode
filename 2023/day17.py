from typing import Iterable
from mylib.aoc_frame2 import Day
import nographs as nog

State = tuple[nog.Position, tuple[nog.Position, ...]]  # position, previous directions


def parse(text: str):
    a = nog.Array(text.splitlines())
    limits = a.limits()
    moves = nog.Position.moves()
    start_position = nog.Position((0, 0))
    goal_position = nog.Position((limits[0][1]-1, limits[1][1]-1))
    return a, limits, moves, start_position, goal_position


class PartA(Day):
    def compute(self, text, config):
        def next_edges(state: State, _) -> Iterable[tuple[State, int]]:
            pos, history = state
            for pos_to in pos.neighbors(moves, limits):
                d = pos_to - pos
                prev_d = history[-1]
                if d == prev_d * -1:
                    # turn forbidden
                    continue
                if all(history_d == d for history_d in history):
                    # d would be the eleventh step in this direction
                    continue
                new_history = history[1:] + (d,)
                yield (pos_to, new_history), int(a[pos_to])

        a, limits, moves, start_position, goal_position = parse(text)
        t = nog.TraversalShortestPaths(next_edges)
        for pos, history in t.start_from((start_position, ((0, 0), (0, 0), (0, 0)))):
            if pos == goal_position:
                return t.distance
        raise RuntimeError()

    def tests(self):
        yield self.test_solve(example, None), 102, "example"


class PartB(PartA):
    def compute(self, text, config):
        def next_edges(state: State, _) -> Iterable[tuple[State, int]]:
            pos, history = state
            for pos_to in pos.neighbors(moves, limits):
                d = pos_to - pos
                prev_d = history[-1]
                if d == prev_d * -1:
                    # turn forbidden
                    continue
                if all(history_d == d for history_d in history):
                    # d would be the eleventh step in this direction
                    continue
                if (prev_d != d and
                        not all(history_d == prev_d for history_d in history[6:-1])):
                    # d is a turn - but there already is one in the previous 4 steps
                    continue
                new_history = history[1:] + (d,)
                yield (pos_to, new_history), int(a[pos_to])

        a, limits, moves, start_position, goal_position = parse(text)
        t = nog.TraversalShortestPaths(next_edges)
        for pos, history in t.start_from(
                (start_position, tuple((0, 0) for i in range(10)))
        ):
            if pos != goal_position:
                continue
            prev_d = history[-1]
            if not all(history_d == prev_d for history_d in history[6:-1]):#
                continue
            return t.distance
        raise RuntimeError()

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
