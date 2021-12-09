import functools
import operator
from mylib.aoc_frame import Day
import mylib.no_graph_lib as nog


class PartA(Day):
    def parse(self, text, d):  # store puzzle parsing result data into attributes of d
        d.depth = [[int(n) for n in line] for line in text.splitlines()]
        d.len_y, d.len_x = len(d.depth), len(d.depth[0])

    def neighbors(self, p, d):
        py, px = p
        for my, mx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            y, x = py + my, px + mx
            if 0 <= y < d.len_y and 0 <= x < d.len_x:
                yield y, x

    def lows(self, d):
        for yp in range(d.len_y):
            for xp in range(d.len_x):
                if all(d.depth[yp][xp] < d.depth[y][x] for y, x in self.neighbors((yp, xp), d)):
                    yield (yp, xp)

    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        return sum(d.depth[y][x] + 1 for (y, x) in self.lows(d))


class PartB(PartA):
    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        sizes = []
        for (yl, xl) in self.lows(d):
            def next_p(p, _):
                (yp, xp) = p
                for (y, x) in self.neighbors((yp, xp), d):
                    if d.depth[y][x] != 9 and d.depth[y][x] > d.depth[yp][xp]:
                        yield (y, x)

            traversal = nog.TraversalDepthFirst(next_p)
            size = sum(1 for p in traversal.start_from((yl, xl)).go()) + 1
            sizes.append(size)
        return functools.reduce(operator.mul, sorted(sizes)[-3:])


Day.do_day(day=9, year=2021, part_a=PartA, part_b=PartB)
