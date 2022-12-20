import collections
from mylib.aoc_frame import Day, CStream


class PartA(Day):
    def parse(self, text, d):  # store puzzle parsing result data into attributes of d
        s = CStream(text)
        d.ints = list(s.loop(s.int)())

    def part_config(self, d):  # add configuration for this part of the day
        d.multiplier = d.rounds = 1

    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        zero_id = d.ints.index(0)
        int_orig = list(enumerate(d.multiplier * i for i in d.ints))
        state = collections.deque(int_orig)
        for round_no in range(d.rounds):
            for i in int_orig:
                i_id, i_int = i
                i_index = state.index(i)
                state.rotate(-i_index)
                _ = state.popleft()
                state.rotate(-i_int)
                state.appendleft(i)
        i_index = state.index((zero_id, 0))
        return (state[(i_index + 1000) % len(state)][1]
                + state[(i_index + 2000) % len(state)][1]
                + state[(i_index + 3000) % len(state)][1])

    def tests(self):  # yield testcases as tuple: (test_result, correct_result [, test_name])
        yield self.test_solve(example, "config"), 3, example


class PartB(PartA):
    def part_config(self, d):  # add configuration for this part of the day
        d.multiplier = 811589153
        d.rounds = 10

    def tests(self):  # yield testcases as tuple: (test_result, correct_result [, test_name])
        yield self.test_solve(example, "config"), 1623178306, example


example = '''
1
2
-3
3
-2
0
4
'''

Day.do_day(day=20, year=2022, part_a=PartA, part_b=PartB)
