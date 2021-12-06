from mylib.aoc_frame import Day
from collections import defaultdict
import collections


class PartA(Day):
    def parse(self, text, d):  # store puzzle parsing result data into attributes of d
        d.list = [int(n) for n in text.split(",")]

    @staticmethod
    def do(d, days):
        population = collections.Counter(d.list)
        for day in range(days):
            population_next = defaultdict(int)
            for f, c in population.items():
                f -= 1
                if f < 0:
                    f = 6
                    population_next[8] += c
                population_next[f] += c
            population = population_next
        r = sum(population.values())
        return r

    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        return self.do(d, 80)


class PartB(PartA):
    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        return self.do(d, 256)


Day.do_day(day=6, year=2021, part_a=PartA, part_b=PartB)
