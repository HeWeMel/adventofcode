import itertools
from mylib.aoc_frame import Day, min_max_corner_pos
import nographs as nog


class PartA(Day):
    def parse(self, text, d):  # store puzzle parsing result data into attributes of d
        a = nog.Array(text.splitlines())
        d.pos = set(a.findall("#"))
        d.directions = [
            ((-1, -1), (-1, +0), (-1, +1)),
            ((+1, -1), (+1, +0), (+1, +1)),
            ((-1, -1), (+0, -1), (+1, -1)),
            ((-1, +1), (+0, +1), (+1, +1)),
        ]

    @staticmethod
    def do_round(pos, directions):
        propositions = dict()
        for elf in pos:
            if all(elf + direction not in pos
                   for direction_list in directions for direction in direction_list):
                continue
            for direction_list in directions:
                if all(elf + direction not in pos for direction in direction_list):
                    if (new_pos := elf + direction_list[1]) in propositions:
                        propositions[new_pos] = None
                    else:
                        propositions[new_pos] = elf
                    break
        moved = False
        for proposition, elf in propositions.items():
            if elf is not None:
                pos.discard(elf)
                pos.add(proposition)
                moved = True
        d1 = directions.pop(0)
        directions.append(d1)
        return moved

    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        for round_no in range(10):
            _ = self.do_round(d.pos, d.directions)
        (min_y, min_x), (max_y, max_x) = min_max_corner_pos(d.pos)
        return (max_y - min_y + 1) * (max_x - min_x + 1) - len(d.pos)

    def tests(self):  # yield testcases as tuple: (test_result, correct_result [, test_name])
        yield self.test_solve(example, "config"), 110, "example"


class PartB(PartA):
    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        for round_no in itertools.count(1):
            moved = self.do_round(d.pos, d.directions)
            if not moved:
                return round_no

    def tests(self):  # yield testcases as tuple: (test_result, correct_result [, test_name])
        yield self.test_solve(example, "config"), 20, "example"


example = '''
....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#..
'''

Day.do_day(day=23, year=2022, part_a=PartA, part_b=PartB)
