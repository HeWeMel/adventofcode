import re
from mylib.aoc_frame import Day


def cube_intersections(cube, cubes):
    """ For each cube in cubes, yield intersection with given cube, if this is not empty """
    cube_from, cube_to = cube
    for other in cubes:
        other_from, other_to = other
        intersection_from = tuple(map(max, zip(cube_from, other_from)))
        intersection_to = tuple(map(min, zip(cube_to, other_to)))
        if all(c_from <= c_to for c_from, c_to in zip(intersection_from, intersection_to)):
            yield intersection_from, intersection_to


def do(d, with_limit):  # return puzzle result, get parsing data from attributes of d
    cubes = []  # cubes, whose volume count positive for the result
    cubes_negative = []  # cubes, whose volume count negative for the result

    for cmd, cube in d.int_lines:
        cube_from, cube_to = cube
        if with_limit and (any(c < -50 for c in cube_from) or any(c > 50 for c in cube_to)):
            continue

        new_cubes_negative = list(cube_intersections(cube, cubes))
        new_cubes = list(cube_intersections(cube, cubes_negative))
        if cmd == "on ":
            new_cubes.append(cube)
        cubes.extend(new_cubes)
        cubes_negative.extend(new_cubes_negative)

    return (sum((xt - xf + 1) * (yt - yf + 1) * (zt - zf + 1)
                for (xf, yf, zf), (xt, yt, zt) in cubes)
            -
            sum((xt - xf + 1) * (yt - yf + 1) * (zt - zf + 1)
                for (xf, yf, zf), (xt, yt, zt) in cubes_negative))


class PartA(Day):
    def parse(self, text, d):  # store puzzle parsing result data into attributes of d
        d.int_lines = []
        for line in text.splitlines():
            cmd = line[0:3]
            xf, xt, yf, yt, zf, zt = (int(n) for n in re.findall(r"[0-9-]+", line))
            d.int_lines.append((cmd, ((xf, yf, zf), (xt, yt, zt))))

    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        return do(d, True)


class PartB(PartA):
    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        return do(d, False)


Day.do_day(day=22, year=2021, part_a=PartA, part_b=PartB)
