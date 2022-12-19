import itertools
from mylib.aoc_frame import Day


class PartA(Day):
    def parse(self, text, d):  # store puzzle parsing result data into attributes of d
        d.jets = [-1 if c == "<" else 1 for c in text]

        rock_input = '''
####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##
'''[1:-1]
        d.rocks = []
        d.rock_height = []
        d.rock_width = []
        for rock in rock_input.split("\n\n"):
            rock_lines = rock.splitlines()
            pos = set()
            d.rock_height.append(len(rock_lines))
            width = 0
            for y, rock_line in enumerate(reversed(rock_lines)):
                for x, c in enumerate(rock_line):
                    if c == "#":
                        pos.add((y, x))
                        width = max(width, x+1)
            d.rocks.append(pos)
            d.rock_width.append(width)

        d.iter_rocks = itertools.cycle(tuple(zip(d.rocks, d.rock_height, d.rock_width)))
        d.iter_jets = itertools.cycle(enumerate(d.jets))

        d.tower = set()
        d.tower_height = 0

    def fall(self, d, rock):
        tower = d.tower
        # print(rock)
        rock_pos, rock_height, rock_width = rock
        y, x = d.tower_height + 3, 2
        while True:
            nj, xn = next(d.iter_jets)
            xn += x
            if (0 <= xn <= 7 - rock_width and
                    all((y + yr, xn + xr) not in tower for yr, xr in rock_pos)):
                x = xn

            yn = y - 1
            if yn >= 0 and all((yn+yr, x+xr) not in tower for yr, xr in rock_pos):
                y = yn
            else:
                tower.update((y+yr, x+xr) for yr, xr in rock_pos)
                d.tower_height = max(d.tower_height, y + rock_height)
                return nj

    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        for number in range(2022):
            self.fall(d, next(d.iter_rocks))
        return d.tower_height

    def tests(self):  # yield testcases as tuple: (test_result, correct_result [, test_name])
        yield self.test_solve(example, 2022), 3068, example


class PartB(PartA):
    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        prev = 0
        modulo_basis = len(d.rocks)
        round_no = 0
        complete_rounds = 0
        jet_seen = set()
        for round_no in itertools.count(1):
            jet_no = self.fall(d, next(d.iter_rocks))
            if round_no % modulo_basis == 0:
                # print(f"rocks modulo {round_no=} {jet_no=}")
                if jet_no in jet_seen:
                    jet_seen = {jet_no}
                    complete_rounds += 1
                    if complete_rounds == 2:
                        height_prefix = d.tower_height
                        round_prefix = round_no
                    elif complete_rounds == 3:
                        break
                elif complete_rounds == 0:
                    jet_seen.add(jet_no)

        height_modulo = d.tower_height - height_prefix
        round_modulo = round_no - round_prefix

        rounds = 1000000000000

        part1_rounds = round_no

        modulo_repeats = (rounds - part1_rounds) // round_modulo
        part2_rounds = modulo_repeats * round_modulo
        part2_height = height_modulo * modulo_repeats

        part3_rounds = rounds - part1_rounds - part2_rounds

        for k in range(1, part3_rounds+1):
            self.fall(d, next(d.iter_rocks))

        return d.tower_height + part2_height

    def tests(self):  # yield testcases as tuple: (test_result, correct_result [, test_name])
        yield self.test_solve(example, 1000000000000), 1514285714288, example


example = '''>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>'''

Day.do_day(day=17, year=2022, part_a=PartA, part_b=PartB)
