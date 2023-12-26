import itertools

import numpy as np
from z3 import IntVector, Solver

from mylib.aoc_frame2 import Day


def parse(text: str):
    for line in text.splitlines():
        pos_str, veloc_str = line.split(" @ ")
        position = [int(coord) for coord in pos_str.split(", ")]
        velocity = [int(coord) for coord in veloc_str.split(", ")]
        yield position, velocity


class PartA(Day):
    def compute(self, text, config):
        if config is None:
            config = [200000000000000, 400000000000000]
        coord_min, coord_max = config

        hailstones = list(parse(text))
        r = 0
        for stone1, stone2 in itertools.combinations(hailstones, 2):
            (p1x, p1y, _), (v1x, v1y, _) = stone1
            (p2x, p2y, _), (v2x, v2y, _) = stone2
            if v1y / v1x == v2y / v2x:
                # Same velocity slope: no intersection
                continue
            # p1x + v1x * t1 = p2x + vx2 * t2
            # p1y + v1y * t1 = p2y + vy2 * t2
            t1, t2 = np.linalg.solve(((v1x, -v2x),
                                      (v1y, -v2y)), (p2x-p1x,
                                                     p2y-p1y))
            if t1 < 0 or t2 < 0:
                continue
            x, y = p1x + t1 * v1x, p1y + t1 * v1y
            if coord_min <= x <= coord_max and coord_min <= y <= coord_max:
                r += 1
        return r

    def tests(self):
        yield self.test_solve(example_a1, [7, 27]), 2, "example1_1"


class PartB(PartA):
    def compute(self, text, config):
        hailstones = list(parse(text))

        px, py, pz, vx, vy, vz = IntVector("p and v", 6)
        t_variables = IntVector("t per stone t", 3)  # just use three hailstones

        s = Solver()
        for t, ((pxi, pyi, pzi), (vxi, vyi, vzi)) in zip(t_variables, hailstones):
            s.add(px + t * vx == pxi + t * vxi)
            s.add(py + t * vy == pyi + t * vyi)
            s.add(pz + t * vz == pzi + t * vzi)

        s.check()
        m = s.model()

        return sum(m[v].as_long() for v in (px, py, pz))

    def tests(self):
        return ()


example_a1 = '''
19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3
'''
Day.do_day(day=24, year=2023, part_a=PartA, part_b=PartB)
