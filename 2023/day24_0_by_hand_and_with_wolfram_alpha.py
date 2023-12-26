from typing import Optional

from aocd.models import Puzzle
from mylib.aoc_frame2 import Day
import nographs as nog


def parse(text: str):
    for line in text.splitlines():
        pos_str, veloc_str = line.split(" @ ")
        pos = nog.Position((int(coord) for coord in pos_str.split(", ")))
        veloc = nog.Position((int(coord) for coord in veloc_str.split(", ")))
        yield pos, veloc


def compute_cross_xy1_time(hailstones: list[tuple[nog.Position, nog.Position]],
                           i1: int, i2: int) -> Optional[float]:
    (px1, py1, _), (vx1, vy1, _) = hailstones[i1]
    (px2, py2, _), (vx2, vy2, _) = hailstones[i2]

    """
    Paths intersect (not: stones collide):
    px1 + vx1 * t1 = px2 + vx2 * t2
    py1 + vy1 * t1 = px2 + vy2 * t2
    Solve first equation for t2. Replace this for t2 in second equation.
    Result: see formula below, here with t instead of t1.
    """
    try:
        t = (((px2 - px1)*vy2 + (py1-py2)*vx2)
             / (vx1*vy2 - vx2*vy1))
        return t
    except ZeroDivisionError:
        return None


def compute_future_pos(hailstones: list[tuple[nog.Position, nog.Position]],
                       i: int, t: float) -> nog.Position:
    (px, py, pz), (vx, vy, vz) = hailstones[i]
    xt = px + t * vx
    yt = py + t * vy
    zt = pz + t * vz
    return nog.Position((xt, yt, zt))


class PartA(Day):
    def compute(self, text, config):
        if config is None:
            config = [200000000000000, 400000000000000]
        print(f"{config=}")
        coord_min, coord_max = config

        hailstones = list(parse(text))
        stone_count = len(hailstones)

        r = 0
        path_intersections = []
        for i in range(stone_count - 1):
            for j in range(i + 1, stone_count):
                cross_xy1_time = compute_cross_xy1_time(hailstones, i, j)
                if cross_xy1_time is None:
                    continue
                cross_xy2_time = compute_cross_xy1_time(hailstones, j, i)
                if cross_xy1_time < 0 or cross_xy2_time < 0:
                    continue
                xt, yt, zt = compute_future_pos(hailstones, i, cross_xy1_time)
                if not(coord_min <= xt <= coord_max and coord_min <= yt <= coord_max):
                    continue
                path_intersections.append((xt, yt, zt, i, j))
                r += 1

        print("------------------")
        print("Equations for part 2:")
        some_stones = set()
        for path_intersection in path_intersections:
            _, _, _, i, j = path_intersection
            some_stones.add(hailstones[i])
            some_stones.add(hailstones[j])
        for i, stone in zip(range(4), some_stones):
            (px, py, pz), (vx, vy, vz) = stone
            ti = chr(ord("s") + i)
            print(f"x + a * {ti} = {px} + {vx} * {ti}, ")
            print(f"y + b * {ti} = {py} + {vy} * {ti}, ")
            print(f"z + c * {ti} = {pz} + {vz} * {ti}, ")
        print("For solving these, see day24_equations_wolfram_alpha_and_z3_online.txt")
        print("------------------")
        return r if r > 0 else None

    def tests(self):
        """ Yield testcases as tuple: (test_result, correct_result [, test_name]) """
        yield self.test_solve(example_a1, [7, 27]), 2, "example1_1"


example_a1 = '''
19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3
'''


puzzle = Puzzle(day=24, year=2023)
PartA().do_part(puzzle)
