from mylib.aoc_frame import Day


class PartA(Day):
    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        for i in range(4-1, len(d.text)):  # all indices that have at least 4-1 lower indices
            if len(set(d.text[i-(4-1):i+1])) == 4:  # 4-1 indices backwards till current
                return i + 1  # official positions count from 0

    def tests(self):  # yield testcases as tuple: (test_input, correct_result [, test_name])
        yield self.test_solve('mjqjpqmgbljsphdztnvjfqwrcgsmlb'), 7, "example 0"
        yield self.test_solve('bvwbjplbgvbhsrlpgdmjqwftvncz'), 5, "example 1"
        yield self.test_solve('nppdvjthqldpwncqszvftbrmjlhg'), 6, "example 2"
        yield self.test_solve('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg'), 10, "example 3"
        yield self.test_solve('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw'), 11, "example 4"


class PartB(PartA):
    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        for i in range(14-1, len(d.text)):  # all indices that have at least 14-1 lower indices
            if len(set(d.text[i-(14-1):i+1])) == 14:  # 14-1 indices backwards till current
                return i + 1  # official positions count from 0!

    def tests(self):  # yield testcases as tuple: (test_result, correct_result [, test_name])
        yield self.test_solve('mjqjpqmgbljsphdztnvjfqwrcgsmlb'), 19, "example 0"
        yield self.test_solve('bvwbjplbgvbhsrlpgdmjqwftvncz'), 23, "example 1"
        yield self.test_solve('nppdvjthqldpwncqszvftbrmjlhg'), 23, "example 2"
        yield self.test_solve('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg'), 29, "example 3"
        yield self.test_solve('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw'), 26, "example 4"


Day.do_day(day=6, year=2022, part_a=PartA, part_b=PartB)
