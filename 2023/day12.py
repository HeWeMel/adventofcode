import functools
import re
from mylib.aoc_frame2 import Day


@functools.cache
def possibilities(conditions, counts, is_start=True):
    r = 0
    for ok in range(0 if is_start else 1, len(conditions)+1 - counts[0]):
        my_condition = "w" * ok
        if re.match(conditions[0:len(my_condition)], my_condition) is None:
            break
        my_condition += ("#" * counts[0])
        if re.match(conditions[0:len(my_condition)], my_condition) is None:
            continue
        if len(counts) == 1:
            my_condition += ("w" * (len(conditions) - len(my_condition)))
            if re.match(conditions, my_condition) is None:
                continue
            r += 1
        else:
            r += possibilities(conditions[len(my_condition):], counts[1:], False)
    return r


class PartA(Day):
    def manipulate_input(self, conditions, counts_str):
        return conditions, counts_str

    def compute(self, text, config):
        r = 0
        for row_str in text.splitlines():
            conditions, counts_str = row_str.split()
            conditions, counts_str = self.manipulate_input(conditions, counts_str)
            counts = tuple(int(n) for n in counts_str.split(","))
            conditions = conditions.replace(".", "w").replace("?", ".")
            r += possibilities(conditions, counts)
        return r

    def tests(self):
        yield self.test_solve("???.### 1,1,3", "config"), 1, "example_a1"
        yield self.test_solve(".??..??...?##. 1,1,3", "config"), 4, "example_a2"
        yield self.test_solve("?#?#?#?#?#?#?#? 1,3,1,6", "config"), 1, "example_a3"
        yield self.test_solve("????.#...#... 4,1,1", "config"), 1, "example_a4"
        yield self.test_solve("????.######..#####. 1,6,5", "config"), 4, "example_a5"
        yield self.test_solve("?###???????? 3,2,1", "config"), 10, "example_a6"


class PartB(PartA):
    def manipulate_input(self, conditions, counts_str):
        return "?".join([conditions] * 5), ",".join([counts_str] * 5)

    def tests(self):
        yield self.test_solve("???.### 1,1,3", "config"), 1, "example_b1"
        yield self.test_solve(".??..??...?##. 1,1,3", "config"), 16384, "example_b2"
        yield self.test_solve("?#?#?#?#?#?#?#? 1,3,1,6", "config"), 1, "example_b3"
        yield self.test_solve("????.#...#... 4,1,1", "config"), 16, "example_b4"
        yield self.test_solve("????.######..#####. 1,6,5", "config"), 2500, "example_b5"
        yield self.test_solve("?###???????? 3,2,1", "config"), 506250, "example_b6"


Day.do_day(day=12, year=2023, part_a=PartA, part_b=PartB)
