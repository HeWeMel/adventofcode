import itertools
import re
from mylib.aoc_frame2 import Day


class PartA(Day):
    backwards = False

    def predict(self, seq):
        if all(v == 0 for v in seq):
            return 0
        diff = [b - a for a, b in itertools.pairwise(seq)]
        predicted_delta = self.predict(diff)
        predicted = seq[0] - predicted_delta if self.backwards else seq[-1] + predicted_delta
        return predicted

    def compute(self, text, config):
        """ Return result for puzzle *text* and *config*"""
        lines = [[int(n)
                  for n in re.findall(r"[-0-9]+", line)]
                 for line in text.splitlines()]
        return sum(self.predict(line) for line in lines)

    def tests(self):
        """ Yield testcases as tuple: (test_result, correct_result [, test_name]) """
        yield self.test_solve(example1, None), 18, "example1"
        yield self.test_solve(example2, None), 114, "example2"


class PartB(PartA):
    backwards = True

    def tests(self):
        """ Yield testcases as tuple: (test_result, correct_result [, test_name]) """
        yield self.test_solve(example3, None), 5, "example3"


example1 = '''
0 3 6 9 12 15
'''

example2 = '''
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
'''

example3 = '''
10 13 16 21 30 45
'''


Day.do_day(day=9, year=2023, part_a=PartA, part_b=PartB)
