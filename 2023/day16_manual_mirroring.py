from typing import Iterable

from mylib.aoc_frame2 import Day
import nographs as nog


Direction = tuple[int, int]
Conf = tuple[nog.Position, Direction]


def mirror(c: str, d: Direction) -> list[Direction]:
    """ Mirror light direction vector *d* at mirror described by *c* """
    dy, dx = d
    match c:
        case "-":
            if dy == 0:
                return [d]
            elif dx == 0:
                return [(0, -1), (0, +1)]
            else:
                return [(-dy, dx)]
        case "|":
            if dx == 0:
                return [d]
            elif dy == 0:
                return [(-1, 0), (+1, 0)]
            else:
                return [(dy, -dx)]
        case "/":
            if dy * dx == -1:
                return [d]
            elif dy * dx == 1:
                return [(-1, +1), (+1, -1)]
            else:
                return [(-dx, -dy)]
        case "\\":
            if dy * dx == 1:
                return [d]
            elif dx * dy == -1:
                return [(-1, -1), (+1, +1)]
            else:
                return [(dx, dy)]
        case ".":
            return [d]
    raise RuntimeError()


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
