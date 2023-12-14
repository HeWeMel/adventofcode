from mylib.aoc_frame2 import Day
import nographs as nog


def tilt(a: nog.Array,
         primary: list[nog.Position],
         secondary: list[nog.Position]):
    """ The reflector dish is tilted towards low coordinates of the secondary axis,
    e.g., if *primary* lists the coordinates along the first (north) row, and
    *secondary* lists the coordinates of the first column from north to south,
    the dish is tilted to the north. """
    # Example: for *tilt north*, the following means: x in range(len_x)
    for coord_0 in primary:
        # Free positions in the "column" of *coord_0*, sorted along the secondary axis
        free = []
        # Example: for *tilt north*, the following means: y in range(len_y)
        for coord_1 in secondary:
            pos = coord_0 + coord_1
            c = a[pos]
            if c == "O":
                if free:
                    # We have a rounded rock and free places to roll: roll to the end
                    first_free = free.pop(0)
                    a[first_free] = c
                    # Previous position of our rounded rock has gotten empty
                    a[pos] = "."
                    free.append(pos)
            elif c == "#":
                # Free positions "behind" this cube-shaped rock are now unreachable
                free = []
            else:
                # A further, free position for rounded rocks to roll
                free.append(pos)


def weight_to_the_north(a: nog.Array) -> int:
    size_y, size_x = a.size()
    return sum(size_y - pos[0] if c == "O" else 0
               for pos, c in a.items())


class PartA(Day):
    def compute(self, text, config):
        a = nog.Array(text.splitlines()).mutable_copy()
        size_y, size_x = a.size()
        tilt(a,
             [nog.Position((0, x)) for x in range(size_x)],
             [nog.Position((y, 0)) for y in range(size_y)])
        return weight_to_the_north(a)

    def tests(self):
        yield self.test_solve(example_a1, "config"), 136, "example1_1"


class PartB(PartA):
    def compute(self, text, config):
        a = nog.Array(text.splitlines()).mutable_copy()
        size_y, size_x = a.size()

        round_of_layout = dict()
        modulo = None
        round = 0
        real_goal = 1000000000
        virtual_goal = -1
        while round != virtual_goal:
            # tilt dish to the north, west, south, and east
            tilt(a,
                 [nog.Position((0, x)) for x in range(size_x)],
                 [nog.Position((y, 0)) for y in range(size_y)])
            tilt(a,
                 [nog.Position((y, 0)) for y in range(size_y)],
                 [nog.Position((0, x)) for x in range(size_x)])
            tilt(a,
                 [nog.Position((0, x)) for x in range(size_x)],
                 [nog.Position((y, 0)) for y in range(size_y-1, -1, -1)])
            tilt(a,
                 [nog.Position((y, 0)) for y in range(size_y)],
                 [nog.Position((0, x)) for x in range(size_x-1, -1, -1)])
            round += 1

            # If we haven't already found a loop in the past...
            if modulo is None:
                # Create a fingerprint of the current rock layout
                layout = tuple((pos, c) for pos, c in a.items())
                # Did we already have this in previous rounds?
                if layout in round_of_layout:
                    first_found = round_of_layout[layout]
                    modulo = round - first_found
                    print(f"Loop found at {round=}, {first_found=}, {modulo=}")
                    # We leave out repeating rounds as far as we stay below *real_goal*,
                    # and do just the rest (modulo the modulo) to the real goal.
                    virtual_goal = round + (real_goal - round) % modulo
                else:
                    round_of_layout[layout] = round
        return weight_to_the_north(a)

    def tests(self):
        yield self.test_solve(example_a1, "config"), 64, "example2"


example_a1 = '''
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
'''

Day.do_day(day=14, year=2023, part_a=PartA, part_b=PartB)
