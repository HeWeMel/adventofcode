import re
from mylib.aoc_frame import Day


class PartA(Day):
    def parse(self, text, d):
        d.block_sums = [sum(int(i) for i in re.findall(r"[0-9]+", block))
                        for block in text.split("\n\n")]

    def compute(self, d):
        return max(d.block_sums)


class PartB(PartA):
    def compute(self, d):
        return sum(sorted(d.block_sums)[-3:])


Day.do_day(day=1, year=2022, part_a=PartA, part_b=PartB)
