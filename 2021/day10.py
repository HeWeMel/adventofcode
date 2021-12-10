from mylib.aoc_frame import Day
import functools


class PartA(Day):
    def parse(self, text, d):  # store puzzle parsing result data into attributes of d
        closing = {'(': ')', '[': ']', '{': '}', '<': '>'}
        d.first_wrong = []
        d.not_closed = []
        for line in text.splitlines():
            needed_closing_brackets = []
            for c in line:
                if c in closing.keys():
                    needed_closing_brackets.append(closing[c])
                else:
                    co = needed_closing_brackets.pop()
                    if c != co:
                        d.first_wrong.append(c)
                        break
            else:
                d.not_closed.append(needed_closing_brackets)

    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        scores = {')': 3, ']': 57, '}': 1197, '>': 25137}
        return sum(scores[c] for c in d.first_wrong)


class PartB(PartA):
    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        scores2 = {')': 1, ']': 2, '}': 3, '>': 4}
        score = [functools.reduce(lambda a, b: a*5+b, (scores2[c] for c in reversed(i)))
                 for i in d.not_closed]
        return sorted(score)[len(score)//2]


Day.do_day(day=10, year=2021, part_a=PartA, part_b=PartB)
