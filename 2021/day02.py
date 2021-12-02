from mylib.aoc_frame import Day


class PartA(Day):
    def parse(self, text, d):  # store puzzle parsing result data into attributes of d
        d.lines = text.splitlines()

    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        pos = depth = 0
        for line in d.lines:  # iterate lines
            c, n = line.split(" ")
            n = int(n)
            if c == "forward":
                pos += n
            elif c == "down":
                depth += n
            else:  # up
                depth -= n
        return pos * depth


class PartB(PartA):
    def compute(self, d):  # return puzzle part result, get parsing data from attributes of d
        pos = depth = aim = 0
        for line in d.lines:  # iterate lines
            c, n = line.split(" ")
            n = int(n)
            if c == "forward":
                pos += n
                depth += aim * n
            elif c == "down":
                aim += n
            else:  # up
                aim -= n
        return pos * depth


Day.do_day(day=2, year=2021, part_a=PartA, part_b=PartB)
