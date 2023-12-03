import functools
import operator
from collections import defaultdict
import re
from mylib.aoc_frame2 import Day


def numbers(lines):
    for line_nr, line in enumerate(lines):
        for match in re.finditer(r"[0-9]+", line):
            s = match[0]
            start, end = match.span(0)
            yield line_nr, start, end, s


def neighbors(lines, line_nr, start, end):
    for y in range(line_nr - 1, line_nr + 1 + 1):
        for x in range(start - 1, end + 1):
            # Only coordinates of the elements "around" the number, and
            # only within the character array
            if (0 <= y < len(lines) and 0 <= x < len(lines[0])
                and (y != line_nr or x < start or x >= end)
            ):
                yield y, x


class PartA(Day):
    def compute(self, text, config):
        """ Return result for puzzle *text* and *config*"""
        lines = text.splitlines()
        result = 0
        for line_nr, start, end, s in numbers(lines):
            if any(lines[y][x] != "."
                   for y, x in neighbors(lines, line_nr, start, end)
                   ):
                result += int(s)
        return result

    def tests(self):
        """ Yield testcases as tuple: (test_result, correct_result [, test_name]) """
        yield self.test_solve(example1, "config"), 4361, "example1"


class PartB(PartA):
    def compute(self, text, config):
        """ Return result for puzzle *text* and *config*"""
        lines = text.splitlines()
        # Mapping from y/x position of "*" to (line_nr, start_x, end_x) of number
        gear_candidates = defaultdict(set)
        for line_nr, start, end, s in numbers(lines):
            for y, x in neighbors(lines, line_nr, start, end):
                if lines[y][x] == "*":
                    gear_candidates[(y, x)].add((line_nr, start, end))
        result = 0
        for pos, number_specs in gear_candidates.items():
            if len(number_specs) != 2:
                continue
            ratio = functools.reduce(operator.mul,
                                     (int(lines[line_nr][start:end])
                                      for line_nr, start, end in number_specs))
            result += ratio
        return result

    def tests(self):
        """ Yield testcases as tuple: (test_result, correct_result [, test_name]) """
        yield self.test_solve(example1, "config"), 467835, "example2"


example1 = '''
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
'''


Day.do_day(day=3, year=2023, part_a=PartA, part_b=PartB)
