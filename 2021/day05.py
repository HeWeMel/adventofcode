from mylib.aoc_frame import Day
import re


class PartA(Day):
    def parse(self, text, d):  # store puzzle parsing result data into attributes of d
        lines = text.splitlines()
        d.int_lines = [[int(n) for n in re.findall(r"[0-9]+", line)] for line in lines]

    def do(self, d, diagonals):  # return puzzle result, get parsing data from attributes of d
        points = set()
        overlap = set()
        for line in d.int_lines:
            x, y, xt, yt = line
            xd = 0 if xt == x else (1 if xt > x else -1)
            yd = 0 if yt == y else (1 if yt > y else -1)
            if not diagonals and xd != 0 and yd != 0:
                continue
            while True:
                if (x, y) in points:
                    overlap.add((x, y))
                else:
                    points.add((x, y))
                if (x, y) == (xt, yt):
                    break
                x, y = x + xd, y + yd
        return len(overlap)

    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        return self.do(d, False)


class PartB(PartA):
    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        return self.do(d, True)


Day.do_day(day=5, year=2021, part_a=PartA, part_b=PartB)
