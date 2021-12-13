import itertools  # itertools.count, itertools.permutations(it, size), itertools.combinations
import functools  # functools.reduce(lambda a, b: a + b, [1, 2, 3]), @functools.cache
import sys        # sys.exit(), sys.setrecursionlimit()
import math       # math.fabs, maths.floor, math.ceil, math.trunc, math.gcd, math.lcd (std: %, //)
from collections import defaultdict
import collections  # counter(iterable), c.keys, c.items, c.most_common(1). c.update(iter_2nd)
import re
import heapq      # h = [], heappush(h, v), v = heappop(h)
from aocd.models import Puzzle
from mylib.aoc_frame import submit, Day, Something,\
    print_dicts, mult_list, neighbors_udlr, neighbors_all
import mylib.no_graph_lib as nog


def do(dots, command):
    _1, _2, c = command.split(" ")
    orientation, location = c.split("=")
    location = int(location)

    if orientation == "x":
        return set((2*location-x, y) if x > location else (x, y) for x, y in dots)
    else:
        return set((x, 2*location-y) if y > location else (x, y) for x, y in dots)


class PartA(Day):
    def parse(self, text, d):  # store puzzle parsing result data into attributes of d
        dot_lines, commands = text.split("\n\n")
        d.dots = set(tuple(int(i) for i in line.split(",")) for line in dot_lines.splitlines())
        d.commands = commands.splitlines()

    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        dots = do(d.dots, d.commands[0])
        return len(dots)


class PartB(PartA):
    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        dots = d.dots
        for command in d.commands:
            dots = do(dots, command)
        for y in range(1+max(y for x, y in dots)):
            s = ""
            for x in range(1+max(x for x, y in dots)):
                s = s + ("#" if (x, y) in dots else " ")
            print(s)
        sys.exit()

    def tests(self):  # yield testcases as tuple: (input_text, result_value [, test_name])
        return ()


Day.do_day(day=13, year=2021, part_a=PartA, part_b=PartB)
