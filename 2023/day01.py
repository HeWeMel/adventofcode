import re
from mylib.aoc_frame2 import Day


class PartA(Day):
    def compute(self, text, config):
        """ Return result for puzzle *text* and *config*"""
        result = 0
        for line in text.splitlines():
            nums = re.findall(r"[0-9]", line)
            result += int(nums[0] + nums[-1])
        return result

    def tests(self):
        """ Yield testcases as tuple: (test_result, correct_result [, test_name]) """
        yield self.test_solve(example1, "config"), 142, "example1"


example1 = '''\
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
'''


def find_first_digit(s: str, r: range) -> int:
    for i in r:
        if '0' <= s[i] <= '9':
            return int(s[i])
        for repl_i, repl_s in enumerate(['zero', 'one', 'two', 'three', 'four', 'five',
                                         'six', 'seven', 'eight', 'nine']):
            if s[i:].startswith(repl_s):
                return repl_i
    raise RuntimeError


class PartB(PartA):
    def compute(self, text, config):
        """ Return result for puzzle *text* and *config*"""
        result = 0
        for line in text.splitlines():
            first = find_first_digit(line, range(len(line)))
            last = find_first_digit(line, range(len(line)-1, -1, -1))
            result += first * 10 + last
        return result

    def tests(self):
        """ Yield testcases as tuple: (test_result, correct_result [, test_name]) """
        yield self.test_solve(example2, "config"), 281, "example2"


example2 = '''\
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
'''


Day.do_day(day=1, year=2023, part_a=PartA, part_b=PartB)
