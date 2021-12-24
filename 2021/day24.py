import functools
import math
from mylib.aoc_frame import Day

values = []


def run(z, w, i):
    """ simulate a run of part i of the 14 parts of the program, giving a starting value
    for variable z and the input digit as w """
    v1, v2, v3 = values[i]
    x = z
    x = x - math.trunc(x / 26) * 26
    z = math.trunc(z / v1)
    x += v2
    x = 1 if x == w else 0
    x = 1 if x == 0 else 0
    y = 25
    y *= x
    y += 1
    z *= y
    y = w
    y += v3
    y *= x
    z += y
    return z


@functools.cache
def best(z, i, down):
    """ find best number (first possible downwards or upwards) that leads to z == zero at end"""
    for digit in (range(9, 0, -1) if down else range(1, 10, 1)):
        z_after = run(z, digit, i)
        if i == 13:  # at the end of the number, z must be zero
            if z_after == 0:
                return digit
        else:  # for other digit positions in the number, try to continue search recursively
            res = best(z_after, i + 1, down)  # z value resulting from my digit is start z for rest
            if res is None:
                continue
            return digit * 10 ** (13 - i) + res  # if recursion finds solution, add my digit
    return None


class PartA(Day):
    def parse(self, text, d):
        """ get variable values out of program, for each of the 14 parts """
        global values
        prg = text.splitlines()
        part_len = len(prg) // 14
        for part in range(14):
            v1 = int(prg[4].split(" ")[2])
            v2 = int(prg[5].split(" ")[2])
            v3 = int(prg[15].split(" ")[2])
            values.append((v1, v2, v3))
            prg = prg[part_len:]
        best.cache_clear()

    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        """ to find highest possible value, search for each digit downwards """
        return best(0, 0, down=True)


class PartB(PartA):
    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        """ to find lowest possible value, search for each digit upwards """
        return best(0, 0, down=False)


Day.do_day(day=24, year=2021, part_a=PartA, part_b=PartB)
