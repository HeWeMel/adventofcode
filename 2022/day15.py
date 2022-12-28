import re
from mylib.aoc_frame import Day, Puzzle


def dist(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


class PartA(Day):
    def parse(self, text, d):  # store puzzle parsing result data into attributes of d
        d.sensors = [[int(n) for n in re.findall(r"[0-9]+", line)] for line in text.splitlines()]

        for line in d.sensors:
            sx, sy, bx, by = line
            line.append(dist(sx, sy, bx, by))

    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        y = 2000000 if d.config is None else d.config

        min_x = min(sx - di for sx, sy, bx, by, di in d.sensors)
        max_x = max(sx + di for sx, sy, bx, by, di in d.sensors)

        not_possible = 0
        for x in range(min_x, max_x + 1):
            for sx, sy, bx, by, di in d.sensors:
                if dist(x, y, sx, sy) <= di and (x != bx or y != by):
                    not_possible += 1
                    break
        return not_possible

    def tests(self):  # yield testcases as tuple: (test_result, correct_result [, test_name])
        yield self.test_solve(example, 10), 26, "example"


class PartB(PartA):
    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        limit = 4000000 if d.config is None else d.config
        for y in range(limit+1):
            intervals = []
            for sx, sy, bx, by, di in d.sensors:
                diameter = di - abs(sy - y)  # diameter in row y
                start, end = sx - diameter, sx + diameter
                if diameter > 0 and end >= 0 and start <= limit:
                    intervals.append((max(0, start), min(limit, end)))
            intervals.sort()  # upwards, first by "from", then by "to"
            next_possible_hole = 0
            for x_from, x_to in intervals:
                if next_possible_hole < x_from:
                    break
                next_possible_hole = max(next_possible_hole, x_to + 1)
            if next_possible_hole <= limit:
                return next_possible_hole * 4000000 + y

    def tests(self):  # yield testcases as tuple: (test_result, correct_result [, test_name])
        yield self.test_solve(example, 20), 56000011, "example"


example = '''
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
'''

Day.do_day(day=15, year=2022, part_a=PartA, part_b=PartB)
