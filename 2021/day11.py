import itertools
from mylib.aoc_frame import Day


class PartA(Day):
    def parse(self, text, d):  # store puzzle parsing result data into attributes of d
        d.levels = [[int(o) for o in line] for line in text.splitlines()]  # 0\n 1\n 2\n
        d.size = len(d.levels)

    def simulate(self, d):
        flashes = 0
        for step in itertools.count(1):
            flashed = set()

            to_increase = [(y, x) for y, x in itertools.product(range(d.size), repeat=2)]
            while to_increase:
                y, x = to_increase.pop()
                d.levels[y][x] += 1
                if d.levels[y][x] > 9 and (y, x) not in flashed:
                    flashes += 1
                    flashed.add((y, x))

                    for yd, xd in itertools.product(range(-1, 2), repeat=2):
                        if (xd != 0 or yd != 0) and 0 <= y + yd < d.size and 0 <= x + xd < d.size:
                            to_increase.append((y + yd, x + xd))

            for yf, xf in flashed:
                d.levels[yf][xf] = 0

            yield step, len(flashed), flashes

    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        for step, flashed, all_flashes in self.simulate(d):
            if step == 100:
                return all_flashes


class PartB(PartA):
    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        for step, flashed, all_flashes in self.simulate(d):
            if flashed == d.size * d.size:
                return step


Day.do_day(day=11, year=2021, part_a=PartA, part_b=PartB)
