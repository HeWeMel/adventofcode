import itertools
import re
from mylib.aoc_frame import Day


class PartA(Day):
    def parse(self, text, d):  # store puzzle parsing result data into attributes of d
        lines = text.splitlines()
        d.int_lines = [(line[0:3],
                        tuple(int(n) for n in re.findall(r"[0-9-]+", line))) for line in lines]

    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        cubes = set()
        for cmd, (xf, xt, yf, yt, zf, zt) in d.int_lines:
            if xf < -50 or yf < -50 or zf < -50 or xt > 50 or yt > 50 or zt > 50:
                continue
            for y in range(yf, yt+1):
                for x in range(xf, xt+1):
                    for z in range(zf, zt+1):
                        if cmd == "on ":
                            cubes.add((x, y, z))
                        else:
                            cubes.discard((x, y, z))
        return len(cubes)


def lays_in(a, b):
    """ Does cube a completely lay in cube b? """
    a_from, a_to = a
    b_from, b_to = b
    return (all(b <= a for a, b in zip(a_from, b_from)) and
            all(a <= b for a, b in zip(a_to, b_to)))


def intervals(af, at, bf, bt):
    """ Intervals a and b. When b is shortened to range of a,
    what interval ranges with different occupation by a and b exist? """
    # 1. Reduce interval b to limits of a
    bt = at if bt > at else bt
    bf = af if bf < af else bf
    if af < bf:
        yield af, bf-1  # range where a started, b not yet
    yield bf, bt  # range of a and b
    if bt < at:
        yield bt+1, at  # range where b ended, but a not yet


def reduce_one(a, b):
    """ Calculate cube a minus cube b (result as list of cubes)"""
    a_from, a_to = a
    b_from, b_to = b
    # If a and b do not intersect, return a
    if (any(at < bf for at, bf in zip(a_to, b_from)) or
            any(bt < af for bt, af in zip(b_to, a_from))):
        yield a
    else:
        # Per coordinate: Parts of interval of a, where occupation by b
        # differs (parts with: "a without b" or "a with b")
        xs, ys, zs = (list(intervals(a_from[i], a_to[i], b_from[i], b_to[i]))
                      for i in range(3))
        for (xf, xt), (yf, yt), (zf, zt) in itertools.product(xs, ys, zs):
            # Iterate combinations or those relevant interval parts
            s = (xf, yf, zf), (xt, yt, zt)
            # If cube of the intervals lays within a, but not b: yield it
            if lays_in(s, a) and not lays_in(s, b):
                yield s


def reduce(cubes, cube):
    """ Cubes minus cube """
    result = []
    for current in cubes:
        tmp = list(reduce_one(current, cube))
        result.extend(tmp)
    return result


class PartB(PartA):
    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        cubes = set()
        cubes_seen = set()

        for cmd, cube in reversed(d.int_lines):
            xf, xt, yf, yt, zf, zt = cube
            cube = ((xf, yf, zf), (xt, yt, zt))

            if cmd == "on ":
                cubes_not_hidden = (cube,)
                for other in cubes_seen:
                    cubes_not_hidden = reduce(cubes_not_hidden, other)
                cubes.update(cubes_not_hidden)
            cubes_seen.add(cube)

        return sum((xt - xf + 1) * (yt - yf + 1) * (zt - zf + 1)
                   for ((xf, yf, zf), (xt, yt, zt)) in cubes)

Day.do_day(day=22, year=2021, part_a=PartA, part_b=PartB)
