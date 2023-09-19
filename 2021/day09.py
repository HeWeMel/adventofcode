import functools
import operator
from mylib.aoc_frame import Day
import nographs as nog


class PartA(Day):
    def parse(self, text, d):  # store puzzle parsing result data into attributes of d
        depth = [[int(n) for n in line] for line in text.splitlines()]
        d.array = nog.Array(depth)
        d.limits = d.array.limits()
        d.moves = nog.Position.moves()

    def low_positions(self, d):
        for pos, depth_at_pos in d.array.items():
            if all(depth_at_pos < d.array[neighbor]
                   for neighbor in pos.neighbors(d.moves, d.limits)):
                yield pos

    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        return sum(d.array[pos] + 1 for pos in self.low_positions(d))


class PartB(PartA):
    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        sizes = []
        for low_pos in self.low_positions(d):
            def next_p(pos, _):
                pos_depth = d.array[pos]
                for neighbor in pos.neighbors(d.moves, d.limits):
                    neighbor_depth = d.array[neighbor]
                    if neighbor_depth != 9 and neighbor_depth > pos_depth:
                        yield neighbor

            traversal = nog.TraversalDepthFirst(next_p)
            size = sum(1 for p in traversal.start_from(low_pos)) + 1
            sizes.append(size)
        return functools.reduce(operator.mul, sorted(sizes)[-3:])


Day.do_day(day=9, year=2021, part_a=PartA, part_b=PartB)
