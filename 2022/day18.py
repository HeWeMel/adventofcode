from mylib.aoc_frame import Day
import nographs as nog


class PartA(Day):
    def parse(self, text, d):  # store puzzle parsing result data into attributes of d
        d.cubes = set(nog.Position(int(w) for w in line.split(","))
                      for line in text.splitlines())
        d.moves = nog.Position.moves(3)

    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        return sum(0 if neighbor in d.cubes else 1
                   for cube in d.cubes
                   for neighbor in cube.neighbors(d.moves))

    def tests(self):  # yield testcases as tuple: (test_result, correct_result [, test_name])
        yield self.test_solve(example, "config"), 64, example


class PartB(PartA):
    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        cubes: set[nog.Position] = d.cubes

        # bounding box, not touching, upper limits are ment exclusively
        limits = [(min(c[coord_number] - 1 for c in cubes),
                   max(c[coord_number] + 1 + 1 for c in cubes)
                   ) for coord_number in range(3)]

        # positions outside the cubes, reachable by orthogonal moves
        t = nog.TraversalBreadthFirst(lambda v, _: v.neighbors(d.moves, limits))
        low_corner = nog.Position(limit[0] for limit in limits)
        outer = set(t.start_from(low_corner, already_visited=set(cubes)))

        # count faces to neighbor positions that are in outer area
        return sum(1 if neighbor in outer else 0
                   for cube in d.cubes
                   for neighbor in cube.neighbors(d.moves))

    def tests(self):  # yield testcases as tuple: (test_result, correct_result [, test_name])
        yield self.test_solve(example, "config"), 58, example


example = '''
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
'''

Day.do_day(day=18, year=2022, part_a=PartA, part_b=PartB)
