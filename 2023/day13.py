from mylib.aoc_frame2 import Day


def find_x_mirror(a: list[str], smudge_count: int):
    size_y = len(a)
    size_x = len(a[0])
    for column in range(1, size_x):  # mirror left of this column?
        if smudge_count == sum(
                1 if a[row][column - width - 1] != a[row][column + width] else 0
                for width in range(min(column, size_x - column))
                for row in range(0, size_y)
        ):
            return column
    return 0


class PartA(Day):
    smudge_count = 0

    def compute(self, text, config):
        """ Return result for puzzle *text* and *config*"""
        r = 0
        for block in text.split("\n\n"):
            array = block.splitlines()
            column = find_x_mirror(array, smudge_count=self.smudge_count)
            transposed = ["".join(array[y][x] for y in range(len(array)))
                          for x in range(len(array[0]))]
            row = find_x_mirror(transposed, smudge_count=self.smudge_count)
            r += column + 100 * row
        return r

    def tests(self):
        """ Yield testcases as tuple: (test_result, correct_result [, test_name]) """
        yield self.test_solve(example1, "config"), 405, "example1"


class PartB(PartA):
    smudge_count = 1

    def tests(self):
        """ Yield testcases as tuple: (test_result, correct_result [, test_name]) """
        yield self.test_solve(example1, "config"), 400, "example1"


example1 = '''
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
'''

Day.do_day(day=13, year=2023, part_a=PartA, part_b=PartB)
