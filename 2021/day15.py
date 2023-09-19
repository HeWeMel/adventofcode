from mylib.aoc_frame import Day
import nographs as nog


class PartA(Day):
    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        return do(d, 1)


class PartB(PartA):
    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        return do(d, 5)


def do(d, size_factor):
    levels = nog.Array(d.text.splitlines())
    size = levels.size()[0]
    limits = levels.limits()

    total_high = size * size_factor - 1  # highest coordinate of complete field made of tiles
    total_limits = ((0, total_high+1),) * 2

    moves = nog.Position.moves()

    def next_edges(p, _):
        for neighbor in p.neighbors(moves, total_limits):
            y, x = neighbor
            level = int(levels[neighbor.wrap_to_cuboid(limits)]) + y // size + x // size
            while level > 9:
                level -= 9
            yield neighbor, level

    traversal = nog.TraversalShortestPaths(next_edges)
    traversal.start_from(nog.Position.at(0, 0)).go_to(nog.Position.at(total_high, total_high))
    return traversal.distance


Day.do_day(day=15, year=2021, part_a=PartA, part_b=PartB)
