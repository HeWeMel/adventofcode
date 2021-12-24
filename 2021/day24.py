import functools
import math
from mylib.aoc_frame import Day


def run(z, w, i):
    values1 = (1, 1, 1, 1, 26, 26, 26, 1, 1, 26, 26, 26, 1, 26)
    values2 = (13, 15, 15, 11, -16, -11, -6, 11, 10, -10, -8, -11, 12, -15)
    values3 = (5, 14, 15, 16, 8, 9, 2, 13, 16, 6, 6, 9, 11, 5)

    x = z
    x = x - math.trunc(x / 26) * 26
    z = math.trunc(z / values1[i])  # z // values1[i]
    x += values2[i]
    x = 1 if x == w else 0
    x = 1 if x == 0 else 0
    y = 25
    y *= x
    y += 1
    z *= y
    y = w
    y += values3[i]
    y *= x
    z += y
    return z


@functools.cache
def best(z, i, down):
    for digit in (range(9, 0, -1) if down else range(1, 10, 1)):
        z_after = run(z, digit, i)
        if i == 13:
            if z_after == 0:
                return digit
        else:
            res = best(z_after, i + 1, down)
            if res is None:
                continue
            return digit * 10 ** (13 - i) + res
    return None


class PartA(Day):
    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        res = best(0, 0, down=True)
        best.cache_clear()
        return res


class PartB(PartA):
    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        res = best(0, 0, down=False)
        best.cache_clear()
        return res


Day.do_day(day=24, year=2021, part_a=PartA, part_b=PartB)
