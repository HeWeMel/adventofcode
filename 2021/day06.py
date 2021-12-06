from mylib.aoc_frame import Day
from collections import defaultdict
import collections


class PartA(Day):
    def parse(self, text, d):  # store puzzle parsing result data into attributes of d
        d.list = [int(n) for n in text.split(",")]  # 0,1,2,3

    def do(self, d, days):
        s = collections.Counter(d.list)

        for day in range(days):
            fnew = 0
            fup = defaultdict(int)
            for fs in s.items():
                f, c = fs
                f -= 1
                if f < 0:
                    f = 6
                    fnew += c
                fup[f] += c
            fup[8] += fnew
            s = fup
        r = sum(s.values())
        return r

    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        return self.do(d, 80)


class PartB(PartA):
    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        return self.do(d, 256)


Day.do_day(day=6, year=2021, part_a=PartA, part_b=PartB)
