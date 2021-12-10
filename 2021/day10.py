from mylib.aoc_frame import Day


class PartA(Day):
    def parse(self, text, d):  # store puzzle parsing result data into attributes of d
        lines = text.splitlines()
        d.closing = {'(': ')', '[': ']', '{': '}', '<': '>'}
        scores = {')': 3, ']': 57, '}': 1197, '>': 25137}

        d.r1 = 0
        d.incomplete = []
        for line in lines:
            s = []
            ok = True
            for c in line:
                if c in ('(', '[', '{', '<'):
                    s.append(c)
                else:
                    co = s.pop()
                    if c != d.closing[co]:
                        d.r1 += scores[c]
                        ok = False
                        continue
            if ok:
                d.incomplete.append(s)

    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        return d.r1


class PartB(PartA):
    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        scores2 = {')': 1, ']': 2, '}': 3, '>': 4}
        r2 = []
        for i in d.incomplete:
            r2t = 0
            for c in reversed(i):
                r2t = r2t * 5 + scores2[d.closing[c]]
            r2.append(r2t)

        r2 = sorted(r2)
        r3 = r2[(len(r2)-1)//2]
        return r3


Day.do_day(day=10, year=2021, part_a=PartA, part_b=PartB)
