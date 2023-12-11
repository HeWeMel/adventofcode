import itertools
from mylib.aoc_frame2 import Day
import nographs as nog


class PartA(Day):
    additional_distance = 1

    def compute(self, text, config):
        a = nog.Array(text.splitlines())

        galaxies = a.findall("#")
        galaxies_y = set(y for y, x in galaxies)
        galaxies_x = set(x for y, x in galaxies)

        r = 0
        for g1, g2 in itertools.combinations(galaxies, 2):
            min_x, max_x = min(g1[1], g2[1]), max(g1[1], g2[1])
            min_y, max_y = min(g1[0], g2[0]), max(g1[0], g2[0])
            r += (max_x - min_x +
                  sum(self.additional_distance
                      for x in range(min_x+1, max_x) if x not in galaxies_x) +
                  max_y - min_y +
                  sum(self.additional_distance
                      for y in range(min_y+1, max_y) if y not in galaxies_y))
        return r

    def tests(self):
        yield self.test_solve(example1_1, "config"), 374, "example1_1"


class PartB(PartA):
    additional_distance = 999999

    def tests(self):
        return []


example1_1 = '''
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
'''

Day.do_day(day=11, year=2023, part_a=PartA, part_b=PartB)
