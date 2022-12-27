import functools

from aocd.models import Puzzle
from mylib.aoc_frame import Day

snafu_digit_for_int = dict(enumerate("=-012", -2))
int_for_snafu_digit = dict(map(reversed, snafu_digit_for_int.items()))


def snafu_to_int(s):
    return functools.reduce(lambda v, c: v * 5 + int_for_snafu_digit[c], s, 0)


def int_to_snafu(i):
    if not i:
        return ""
    i, d = divmod(i, 5)
    if d > 2:
        d -= 5
        i += 1
    return int_to_snafu(i) + snafu_digit_for_int[d]


class PartA(Day):
    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        example_mode = d.config is True

        res = 0
        for s in d.text.splitlines():
            n = snafu_to_int(s)
            res += n

            # test our function int_to_snafu (here, all available data can be used)
            if s != (s2 := int_to_snafu(n)):
                raise RuntimeError(s, n, s2)

        return res if example_mode else int_to_snafu(res)

    def tests(self):  # yield testcases as tuple: (test_result, correct_result [, test_name])
        yield self.test_solve(example, True), 4890, "example"


example = '''
1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122
'''


puzzle = Puzzle(day=25, year=2022)
PartA().do_part(puzzle)
