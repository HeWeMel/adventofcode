from mylib.aoc_frame import Day
import nographs as nog


class PartA(Day):
    start = "S"

    def compute(self, d):
        a = nog.Array(d.text.splitlines())
        limits = a.limits()
        moves = nog.Position.moves()

        def elevation(c):
            return ord({"S": "a", "E": "z"}.get(c, c))

        def next_vertex(p: nog.Position, _):
            for p2 in p.neighbors(moves, limits):
                if elevation(a[p2]) <= elevation(a[p]) + 1:
                    yield p2

        s = a.findall(self.start)
        e = a.findall("E")[0]

        t = nog.TraversalBreadthFirst(next_vertex).start_from(start_vertices=s)
        t.go_to(e)
        return t.depth

    def tests(self):
        yield self.test_solve(example), 31, "example"


class PartB(PartA):
    start = "a"

    def tests(self):
        yield self.test_solve(example), 29, "example"


example = '''
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
'''

Day.do_day(day=12, year=2022, part_a=PartA, part_b=PartB)
