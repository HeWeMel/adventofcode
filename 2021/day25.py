import itertools
from aocd.models import Puzzle
from mylib.aoc_frame import Day
import nographs as nog


def move(us, them, step, limits):
    new_us = set()
    for pos in us:
        new_pos = (pos + step).wrap_to_cuboid(limits)
        if new_pos not in us and new_pos not in them:
            pos = new_pos
        new_us.add(pos)
    return new_us, (us != new_us)


class PartA(Day):
    def parse(self, text, d):  # store puzzle parsing result data into attributes of d
        lines = nog.Array(text.splitlines())
        d.limits = lines.limits()
        d.right, d.down = (lines.findall(c) for c in ">v")

    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        for step in itertools.count(1):
            d.right, moved1 = move(d.right, d.down, (0, 1), d.limits)
            d.down, moved2 = move(d.down, d.right, (1, 0), d.limits)
            if not (moved1 or moved2):
                return step


puzzle = Puzzle(day=25, year=2021)
PartA().do_part(puzzle)
