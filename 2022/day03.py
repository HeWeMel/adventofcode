from mylib.aoc_frame import Day


class PartA(Day):
    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        priority_sum = 0
        for line in d.text.splitlines():
            line_len = len(line) // 2
            left, right = set(line[:line_len]), set(line[-line_len:])
            common_element = left.intersection(right).pop()
            priority = (1+ord(common_element)-ord("a") if "a" <= common_element <= "z"
                        else 27+ord(common_element)-ord("A"))
            priority_sum += priority
        return priority_sum

    def tests(self):  # yield testcases as tuple: (test_input, correct_result [, test_name])
        yield self.test_solve('''
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
'''), 157, "example"


class PartB(PartA):
    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        lines = d.text.splitlines()

        priority_sum = 0
        for group in range(len(lines) // 3):
            line1 = set(lines[group*3+0])
            line2 = set(lines[group*3+1])
            line3 = set(lines[group*3+2])
            common_element = line1.intersection(line2).intersection(line3).pop()
            priority = (1 + ord(common_element) - ord("a") if "a" <= common_element <= "z"
                        else 27 + ord(common_element) - ord("A"))
            priority_sum += priority
        return priority_sum

    def tests(self):  # yield testcases as tuple: (test_input, correct_result [, test_name])
        yield self.test_solve('''
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
'''), 70, "example"


Day.do_day(day=3, year=2022, part_a=PartA, part_b=PartB)
