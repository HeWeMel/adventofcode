import functools
from mylib.aoc_frame import Day, aoc_div_round_to_zero, aoc_div_remainder


def run(z, w, i, values):
    """ simulate a run of part i of the 14 parts of the program, given a starting value
    for variable z and the input digit as w """
    v1, v2, v3 = values[i]
    x = aoc_div_remainder(z, 26) + v2
    z = aoc_div_round_to_zero(z, v1)
    if x != w:
        z = 26*z + w + v3
    return z


@functools.cache
def best(z, i, down, values):
    """ find best number (first possible downwards or upwards) that leads to z == zero at end"""
    for digit in (range(9, 0, -1) if down else range(1, 10, 1)):
        z_after = run(z, digit, i, values)
        if i == 13:  # at the end of the number, z must be zero
            if z_after == 0:
                return digit
        else:  # for other digit positions in the number, try to continue search recursively
            # z value resulting from my digit when start with my new z for rest of program
            res = best(z_after, i + 1, down, values)
            if res is not None:   # if recursion found solution, add my digit
                return digit * 10 ** (13 - i) + res
    return None


class PartA(Day):
    def parse(self, text, d):
        """ get variable values out of program, for each of the 14 parts """
        prg = text.splitlines()
        part_len = len(prg) // 14
        d.values = tuple(
            tuple(int(prg[part + line].split(" ")[2]) for line in (4, 5, 15))
            for part in range(0, 14 * part_len, part_len)
        )

    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        """ to find highest possible value, search for each digit downwards """
        return best(z=0, i=0, down=True, values=d.values)


class PartB(PartA):
    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        """ to find lowest possible value, search for each digit upwards """
        best.cache_clear()
        return best(z=0, i=0, down=False, values=d.values)


Day.do_day(day=24, year=2021, part_a=PartA, part_b=PartB)
