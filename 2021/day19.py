import itertools
import collections
from mylib.aoc_frame import Day
import operator


def v_sub(v1, v2):  # vector minus vector
    return tuple(map(operator.sub, v1, v2))


def manhattan(a, b):  # manhattan distance of to positions
    return sum(abs(c) for c in v_sub(a, b))


def rotate_z(pos):  # rotate position
    x, y, z = pos
    x, y = y, -x
    return (x, y, z)


def rotate_x(pos):  # rotate position
    x, y, z = pos
    y, z = z, -y
    return (x, y, z)


def rotate_y(pos):  # rotate position
    x, y, z = pos
    x, z = z, -x
    return (x, y, z)


def rotated(scanner):  # rotate the beacon coordinates of the scanner in all 24 viewing directions
    for zr in range(4):
        for xr in range(4):
            yield scanner
            scanner = [rotate_x(p) for p in scanner]
        scanner = [rotate_y(p) for p in scanner]
        yield scanner
        scanner = [rotate_y(p) for p in scanner]
        scanner = [rotate_y(p) for p in scanner]
        yield scanner
        scanner = [rotate_y(p) for p in scanner]

        scanner = [rotate_z(p) for p in scanner]


def do(d):  # return puzzle result, get parsing data from attributes of d
    # parse scanner input
    unmatched_scanners = set()
    for block in d.text.split("\n\n"):
        lines = block.splitlines()[1:]
        scanner = frozenset(  # a scanner is the frozenset of its beacon positions
            tuple(int(i) for i in line.split(","))  # beacon: tuple of three coordinates
            for line in lines
        )
        unmatched_scanners.add(scanner)

    # choose first scanner randomly
    scanner = unmatched_scanners.pop()
    integrated_scanners = {scanner}
    beacons = set(scanner)  # mutable set of the beacons of the first scanner
    scanner_positions = []

    # precompute all rotations for each scanner output
    rotations = {scanner: [frozenset(r) for r in rotated(scanner)]
                 for scanner in unmatched_scanners}

    while len(unmatched_scanners) > 0:
        used_scanner = integrated_scanners.pop()  # try to match with this integrated scanner
        for scanner in unmatched_scanners.copy():  # try to match this scanner
            for scanner_rot in rotations[scanner]:  # in any of its rotation variants
                # pairwise combine positions of the two scanners and compute difference vector
                c = collections.Counter((v_sub(a, b) for (a, b)
                                         in itertools.product(scanner_rot, used_scanner)))
                diff, count = c.most_common(1)[0]
                if count >= 12:  # if at least 12 pairs with the same difference vector are found:
                    adapted_scanner = frozenset(v_sub(b, diff) for b in scanner_rot)
                    unmatched_scanners -= {scanner}
                    integrated_scanners |= {adapted_scanner}
                    beacons.update(adapted_scanner)
                    scanner_positions.append(diff)
    return beacons, scanner_positions


class PartA(Day):
    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        beacons, positions = do(d)
        return len(beacons)


class PartB(PartA):
    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        beacons, positions = do(d)
        return max(manhattan(a, b) for a, b in itertools.combinations(positions, 2))


Day.do_day(day=19, year=2021, part_a=PartA, part_b=PartB)
