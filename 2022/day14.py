import itertools
from mylib.aoc_frame import Day


class PartA(Day):
    def parse(self, text, d):  # store puzzle parsing result data into attributes of d
        d.rock = set()
        d.max_y = -float("inf")
        for line in text.splitlines():
            for pos1, pos2 in itertools.pairwise(line.split(" -> ")):
                x1, y1 = (int(i) for i in pos1.split(","))
                x2, y2 = (int(i) for i in pos2.split(","))

                d.max_y = max(y1, y2, d.max_y)

                xd = (x2 - x1) // abs(x2 - x1) if x2 != x1 else 0
                yd = (y2 - y1) // abs(y2 - y1) if y2 != y1 else 0
                while True:
                    d.rock.add((x1, y1))
                    if (x1, y1) == (x2, y2):
                        break
                    x1 += xd
                    y1 += yd

    def path(self, d):
        x, y = (500, 0)
        while y <= d.max_y:
            for xn, yn in ((x, y+1), (x-1, y+1), (x+1, y+1)):
                if (xn, yn) not in d.rock:
                    x, y = xn, yn
                    break
            else:
                d.rock.add((x, y))
                break
        return x, y

    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        to_rest = 0
        while True:
            x, y = self.path(d)
            if y > d.max_y:
                break
            to_rest += 1
        return to_rest

    def tests(self):  # yield testcases as tuple: (test_result, correct_result [, test_name])
        yield self.test_solve(example), 24, "example"


class PartB(PartA):
    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        to_rest = 0
        while True:
            x, y = self.path(d)
            if y > d.max_y:
                d.rock.add((x, y))
            to_rest += 1
            if y == 0:
                break
        return to_rest

    def tests(self):  # yield testcases as tuple: (test_result, correct_result [, test_name])
        yield self.test_solve(example), 93, "example"


example = '''
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
'''

Day.do_day(day=14, year=2022, part_a=PartA, part_b=PartB)
