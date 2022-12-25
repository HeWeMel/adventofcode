from aocd.models import Puzzle
from mylib.aoc_frame import Day


class PartA(Day):
    @staticmethod
    def int_to_snafu(i, snafu):
        res = ""
        o = 0
        while i + o:
            i, d = divmod(i+o, 5)
            if d > 2:
                o = 1
                d -= 5
            else:
                o = 0
            res = snafu[d] + res
        return res

    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        test_mode = d.config is True

        snafu = dict(enumerate("=-012", -2))
        digits = {k: v for v, k in snafu.items()}

        res = 0
        for s in d.text.splitlines():
            n = 0
            for c in s:
                n = n * 5 + digits[c]
            res += n

            # test function int_to_snafu (here, all available data can be used)
            s2 = self.int_to_snafu(n, snafu)
            if s != s2:
                raise RuntimeError(s, n, s2)

        if test_mode:
            return res
        else:
            return self.int_to_snafu(res, snafu)

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
