from mylib.aoc_frame import Day


class PartA(Day):
    def parse(self, text, d):  # store puzzle parsing result data into attributes of d
        d.ints = [int(line) for line in text.splitlines()]

    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        return sum(d.ints[i] > d.ints[i-1] for i in range(1, len(d.ints)))


class PartB(PartA):
    def compute(self, d):  # return puzzle part result, get parsing data from attributes of d
        return sum(d.ints[i] > d.ints[i-3] for i in range(3, len(d.ints)))


Day.do_day(day=1, year=2021, part_a=PartA, part_b=PartB)
