from typing import Iterable

from mylib.aoc_frame2 import Day, vector_angle_cos, mirror_vector_at_vector_2d
import nographs as nog


Direction = tuple[int, int]
Conf = tuple[nog.Position, Direction]


def mirror(c: str, d: Direction) -> list[Direction]:
    if c == ".":
        return [d]
    # An arbitrary one of the two directions shown by the character
    mirror_direction = {"-": (0, 1), "|": (1, 0), "/": (1, -1), "\\": (1, 1), }[c]
    # Heading and mirror are orthogonal?
    angle_cos = vector_angle_cos(d, mirror_direction)
    if round(angle_cos, 5) == 0:
        return [mirror_direction, nog.Position(mirror_direction) * -1]
    # Otherwise: Normal reflection. The light heading vector is mirrored at an
    # orthogonal vector of the mirror direction, and then its direction is negated.
    # Implementation: Instead, we mirror the light at the mirror direction, and do not
    # negate, this is equivalent.
    d_new = mirror_vector_at_vector_2d(d, mirror_direction)
    return [(round(d_new[0]), round(d_new[1]))]


def parse(text: str):
    a = nog.Array(text.splitlines())
    limits = a.limits()

    def next_vertices(conf: Conf, _) -> Iterable[Conf]:
        pos, heading = conf

        pos += heading
        if not pos.is_in_cuboid(limits):
            return []
        return ((pos, d) for d in mirror(a[pos], heading))
    return a, nog.TraversalDepthFirst(next_vertices)


def energized(start_conf, t: nog.TraversalDepthFirst):
    energized_positions = set()
    for pos, heading in t.start_from(start_conf):
        energized_positions.add(pos)
    return len(energized_positions)


class PartA(Day):
    def compute(self, text, config):
        a, t = parse(text)
        start_conf = (nog.Position((0, -1)), (0, 1))  # pos and heading vector
        return energized(start_conf, t)

    def tests(self):
        yield self.test_solve(example, None), 46, "example"


class PartB(PartA):
    def compute(self, text, config):
        a, t = parse(text)
        size_y, size_x = a.size()
        return max([
            max(energized((nog.Position((-1, x)), (1, 0)), t)
                for x in range(size_x)),
            max(energized((nog.Position((size_y, x)), (-1, 0)), t)
                for x in range(size_x)),
            max(energized((nog.Position((y, -1)), (1, 0)), t)
                for y in range(size_x)),
            max(energized((nog.Position((y, size_x)), (1, 0)), t)
                for y in range(size_x))])

    def tests(self):
        yield self.test_solve(example, None), 51, "example"


example = '''
.|...\\....
|.-.\\.....
.....|-...
........|.
..........
.........\\
..../.\\\\..
.-.-/..|..
.|....-|.\\
..//.|....
'''

Day.do_day(day=16, year=2023, part_a=PartA, part_b=PartB)
