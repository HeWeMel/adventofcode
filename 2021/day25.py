import itertools
from aocd.models import Puzzle
from mylib.aoc_frame import Day, wrap_add


def move(us, them, to_the_right, lx, ly):
    new_us = set()
    for x, y in us:
        (nx, ny) = (wrap_add(x, 1, lx), y) if to_the_right else (x, wrap_add(y, 1, ly))
        if (nx, ny) not in us and (nx, ny) not in them:
            x, y = nx, ny
        new_us.add((x, y))
    return new_us, (us != new_us)


class PartA(Day):
    def parse(self, text, d):  # store puzzle parsing result data into attributes of d
        lines = text.splitlines()
        d.len_y = len(lines)
        d.len_x = len(lines[0])
        d.right = {(x, y) for y, line in enumerate(lines) for x, c in enumerate(line) if c == ">"}
        d.down = {(x, y) for y, line in enumerate(lines) for x, c in enumerate(line) if c == "v"}

    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        for step in itertools.count(1):
            d.right, moved1 = move(d.right, d.down, True, d.len_x, d.len_y)
            d.down, moved2 = move(d.down, d.right, False, d.len_x, d.len_y)
            if not (moved1 or moved2):
                return step


puzzle = Puzzle(day=25, year=2021)
PartA().do_part(puzzle)
