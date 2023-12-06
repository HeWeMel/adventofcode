import math
import re
from mylib.aoc_frame2 import Day


def winning_waiting_times(d, t):
    for w in range(t+1):
        if (t - w) * w > d:
            yield w


class PartA(Day):
    def compute(self, text, config):
        times = [int(n) for n in re.findall(r"[0-9]+", text.splitlines()[0])]
        distances = [int(n) for n in re.findall(r"[0-9]+", text.splitlines()[1])]

        result = 1
        for time, distance in zip(times, distances):
            result *= sum(1 for w in winning_waiting_times(distance, time))
        return result

    def tests(self):
        """ Yield testcases as tuple: (test_result, correct_result [, test_name]) """
        yield self.test_solve(example1, "config"), 288, "example1"


class PartB(PartA):
    def compute(self, text, config):
        """
        d distance, t time, w waiting_time
        d(w) = (t - w) * w = tw - w^2
        d(w)´ = t - 2w -> At w t/2, d(w) is zero -> d(w) = -(w - t/2)^2 + t^2 / 4
        For d(w) = w: (w - t/2)^2 = t^2 / 4 - d
        -> w = +-sqrt(t^2 / 4 - d) + t/2
        """
        time = int("".join(re.findall(r"[0-9]+", text.splitlines()[0])))
        distance = int("".join(re.findall(r"[0-9]+", text.splitlines()[1])))
        low = math.ceil(-math.sqrt(time*time / 4 - distance) + time / 2)
        high = math.floor(math.sqrt(time*time / 4 - distance) + time / 2)
        return high - low + 1

    def tests(self):
        """ Yield testcases as tuple: (test_result, correct_result [, test_name]) """
        yield self.test_solve(example1, "config"), 71503, "example2"


example1 = '''
Time:      7  15   30
Distance:  9  40  200
'''


Day.do_day(day=6, year=2023, part_a=PartA, part_b=PartB)

