from mylib.aoc_frame import Day
import mylib.no_graph_lib as nog


class PartA(Day):
    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        return do(d, 1)


class PartB(PartA):
    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        return do(d, 5)


def do(d, size_factor):
    levels = d.text.splitlines()
    size = len(levels)
    high = size * size_factor - 1

    def next_edges(p, _):
        for neighbor in nog.matrix_neighbors(p, ((0, high), (0, high)), no_diagonals=True):
            x, y = neighbor
            level = int(levels[y % size][x % size]) + y // size + x // size
            while level > 9:
                level -= 9
            yield neighbor, level

    traversal = nog.TraversalShortestPaths(next_edges)
    traversal.start_from((0, 0)).go_to((high, high))
    return traversal.distance


Day.do_day(day=15, year=2021, part_a=PartA, part_b=PartB)
