from mylib.aoc_frame import Day
import nographs as nog


class PartA(Day):
    def parse(self, text, d):  # store puzzle parsing result data into attributes of d
        d.cubes = set(nog.Position(int(w) for w in line.split(","))
                      for line in text.splitlines())
        d.moves = ((-1, 0, 0), (0, -1, 0), (0, 0, -1), (1, 0, 0), (0, 1, 0), (0, 0, 1))

    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        return sum(0 if neighbor in d.cubes else 1
                   for cube in d.cubes
                   for neighbor in cube.neighbors(d.moves))

    def tests(self):  # yield testcases as tuple: (test_result, correct_result [, test_name])
        yield self.test_solve(example, "config"), 64, example


class PartB(PartA):
    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        cubes: set[nog.Position] = d.cubes

        limits = [(min(c[coord_number] for c in cubes),
                   max(c[coord_number] for c in cubes)
                   ) for coord_number in range(3)]

        def next_vertices(v_from: nog.Position, _):
            return list(v_from.neighbors(d.moves))

        around_hull = set()
        for cube in cubes:
            around_hull.update(cube.neighbors(d.moves))
        around_hull.difference_update(cubes)

        t = nog.TraversalBreadthFirst(next_vertices)
        inner = set()

        for start in around_hull:
            test_inner = {start}
            for v in t.start_from(start, already_visited=set(cubes)):
                if not v.is_in_cuboid(limits):
                    break  # Search from start escaped cubes. Thus, it is "outside".
                test_inner.add(v)
            else:
                inner.update(test_inner)

        return sum(0 if neighbor in cubes or neighbor in inner else 1
                   for cube in cubes
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
