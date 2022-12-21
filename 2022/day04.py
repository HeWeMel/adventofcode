import re
from mylib.aoc_frame import Day


class PartA(Day):
    def parse(self, text, d):  # store puzzle parsing result data into attributes of d
        lines = text.splitlines()
        d.int_lines = [[int(n) for n in re.findall(r"[0-9]+", line)] for line in lines]

    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        return sum(1 if (a_from <= b_from and b_to <= a_to or
                         b_from <= a_from and a_to <= b_to)
                   else 0
                   for a_from, a_to, b_from, b_to in d.int_lines)

    def tests(self):  # yield testcases as tuple: (test_input, correct_result [, test_name])
        yield self.test_solve(example), 2, "example"


class PartB(PartA):
    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        return sum(0 if a_to < b_from or b_to < a_from
                   else 1
                   for a_from, a_to, b_from, b_to in d.int_lines)

    def tests(self):  # yield testcases as tuple: (test_input, correct_result [, test_name])
        yield self.test_solve(example), 4, "example"


example = '''
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
'''

Day.do_day(day=4, year=2022, part_a=PartA, part_b=PartB)
