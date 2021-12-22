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


class PartB(PartA):
    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        cubes = set()

        for cmd, cube in d.int_lines:
            if cmd == "on ":
                if len(cubes) == 0:
                    cubes.add(cube)
                else:
                    # Calculate what parts of the new cube add up without overlap to existing ones
                    cubes_to_add = [cube, ]
                    cubes_to_remove = []
                    for other in cubes:
                        # An existing cube lays within the new: Discard the existing one
                        if lays_in(other, cube):
                            cubes_to_remove.append(other)
                            continue
                        # The new cube lays withing an existing one: nothing to do, abort
                        if lays_in(cube, other):
                            cubes_to_add = []
                            cubes_to_remove = []
                            break

                        cubes_to_add = reduce(cubes_to_add, other)
                    cubes.difference_update(cubes_to_remove)
                    cubes.update(cubes_to_add)
            else:
                cubes = set(reduce(cubes, cube))
        return sum((xt - xf + 1) * (yt - yf + 1) * (zt - zf + 1)
                   for (xf, xt, yf, yt, zf, zt) in cubes)


def lays_in(a, b):
    """ Lays cube a completely in cube b? """
    axf, axt, ayf, ayt, azf, azt = a
    bxf, bxt, byf, byt, bzf, bzt = b
    return(
            bxf <= axf <= axt <= bxt and
            byf <= ayf <= ayt <= byt and
            bzf <= azf <= azt <= bzt)


def reduce(cubes, cube):
    """ Cubes minus cube """
    result = []
    for current in cubes:
        tmp = list(reduce_one(current, cube))
        result.extend(tmp)
    return result


def intervals(af, at, bf, bt):
    """ Intervals a and b. When b is shortened to range of a,
    that interval ranges with different occupation by a and b exist? """
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
    axf, axt, ayf, ayt, azf, azt = a
    bxf, bxt, byf, byt, bzf, bzt = b
    if (
            axt < bxf or bxt < axf or
            ayt < byf or byt < ayf or
            azt < bzf or bzt < azf):
        yield a  # a and b do not intersect, return a as a - b
    else:
        # Iterate relevant intervals along all axes
        # (Within each interval, the intersection situation is everywhere the same)
        xs = list(intervals(axf, axt, bxf, bxt))
        ys = list(intervals(ayf, ayt, byf, byt))
        zs = list(intervals(azf, azt, bzf, bzt))
        for xf, xt in xs:
            for yf, yt in ys:
                for zf, zt in zs:
                    s = xf, xt, yf, yt, zf, zt
                    # If cube of the intervals lays within a, but not b: yield it
                    if lays_in(s, a) and not lays_in(s, b):
                        yield s


Day.do_day(day=22, year=2021, part_a=PartA, part_b=PartB)
