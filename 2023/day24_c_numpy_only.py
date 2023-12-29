import itertools
import numpy as np

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
            # noinspection PyTypeChecker
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
        # Copy data to lists per data value, for easier addressing of the values
        px, py, pz, vx, vy, vz = ([] for i in range(6))
        for stone in itertools.islice(parse(text), 3):
            values = itertools.chain.from_iterable(stone)
            for lst in [px, py, pz, vx, vy, vz]:
                lst.append(next(values))
        """
        Hailstone i hits rock:
            p + v * t = p_i + v_i * t
        <=> (p - p_i) = (v_i - v) * t
        Since t is scalar, the two bracketed expressions need to stand perpendicular on each other.
        <=> (p - p_i) x (v_i - v) = (0, 0, 0)
        <=> For x: (py - py_i) * (vz_i - vz)
            - (pz - pz_i) * (vy_i - vy) = 0  - the same for y and z
        <=> py * vz_i - py * vz - py_i * vz_i + py_i * vz
            - pz * vy_i + pz * vy + pz_i * vy_i - pz_i * vy = 0
        Take this for hailstones i and j, and subtract expression for i from this for j:
        <=> py * (vz_j - vz_i) + (py_i * vz_i - py_j * vz_j) + (py_j - py_i) * vz
            + pz * (vy_i - vy_j) + (pz_j * vy_j - pz_i * vy_i) + vy * (pz_i - pz_j) = 0
        <=>   0 * px
            + (vz_j - vz_i) * py
            + (vy_i - vy_j) * pz
            + 0 * vx
            + (pz_i - pz_j) * vy
            + (py_j - py_i) * vz
            = (pz_i * vy_i - pz_j * vy_j) + (py_j * vz_j - py_i * vz_i)
        We use the first three hailstones of the list and hope that their velocity vectors
        #re linearly independent.
        This gives line 5 in the matrix/vector below. And for yx / zx lines
        1 and 3. And the same for hailstones 2/1 instead of 1/0 gives the other 3 equations.
        """
        array = np.array([
            # Lines: yx/zx/zy, stone 0 vs 1/2
            [vy[1] - vy[0], vx[0] - vx[1], 0, py[0] - py[1], px[1] - px[0], 0],
            [vy[2] - vy[0], vx[0] - vx[2], 0, py[0] - py[2], px[2] - px[0], 0],
            [vz[1] - vz[0], 0, vx[0] - vx[1], pz[0] - pz[1], 0, px[1] - px[0]],
            [vz[2] - vz[0], 0, vx[0] - vx[2], pz[0] - pz[2], 0, px[2] - px[0]],
            [0, vz[1] - vz[0], vy[0] - vy[1], 0, pz[0] - pz[1], py[1] - py[0]],
            [0, vz[2] - vz[0], vy[0] - vy[2], 0, pz[0] - pz[2], py[2] - py[0]],
        ])
        values = [
            # Lines: yx/zx/zv, stone 0 vs 1/2
            (py[0] * vx[0] - py[1] * vx[1]) - (px[0] * vy[0] - px[1] * vy[1]),
            (py[0] * vx[0] - py[2] * vx[2]) - (px[0] * vy[0] - px[2] * vy[2]),
            (pz[0] * vx[0] - pz[1] * vx[1]) - (px[0] * vz[0] - px[1] * vz[1]),
            (pz[0] * vx[0] - pz[2] * vx[2]) - (px[0] * vz[0] - px[2] * vz[2]),
            (pz[0] * vy[0] - pz[1] * vy[1]) - (py[0] * vz[0] - py[1] * vz[1]),
            (pz[0] * vy[0] - pz[2] * vy[2]) - (py[0] * vz[0] - py[2] * vz[2]),
        ]
        solution = np.linalg.solve(array, values)
        return round(solution[0] + solution[1] + solution[2])

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
