from mylib.aoc_frame import Day, CStream


def tokens(t):
    s = CStream(t)
    r = []
    while s.lookahead is not None:
        match s.lookahead:
            case "[" | "]" | ",":
                r.append(next(s))
            case _:
                r.append(s.int())
    return r


def check(l, r):
    match l[0], r[0]:
        case ["[", "["]:
            result, rest_l, rest_r = check(l[1:], r[1:])
            if result is not None:
                return result, "", ""
            return check(rest_l, rest_r)
        case ["]", "]"]:
            return None, l[1:], r[1:]
        case [",", ","]:
            return check(l[1:], r[1:])
        case ["]", other]:
            return True, "", ""
        case [other, "]"]:
            return False, "", ""
        case ["[", rv]:
            return check(l, ["[", r[0], "]"] + r[1:])
        case [lv, "["]:
            return check(["[", l[0], "]"] + l[1:], r)
        case [lv, rv]:
            if lv < rv:
                return True, "", ""
            elif rv < lv:
                return False, "", ""
            else:
                return check(l[1:], r[1:])


class PartA(Day):
    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        total = 0
        for pair, block in enumerate(d.text.split("\n\n"), 1):
            l, r = block.splitlines()
            result, _, _ = check(tokens(l), tokens(r))
            if result:
                total += pair
        return total

    def tests(self):  # yield testcases as tuple: (test_result, correct_result [, test_name])
        # if True is True:  # remove to activate
        #    return ()
        yield self.test_solve(example), 13, "example"


class PartB(PartA):
    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        divider = '''\
[[2]]
[[6]]
'''.splitlines()
        lines = divider.copy()
        lines.extend(line for line in d.text.splitlines() if line != "")

        class Packet(str):
            def __lt__(self, other):
                return check(tokens(self), tokens(other))[0]

        packets = [Packet(line) for line in lines]
        packets_sorted = sorted(packets)

        total = 1
        for i in range(len(packets_sorted)):
            if packets_sorted[i] in divider:
                total *= i + 1
        return total

    def tests(self):  # yield testcases as tuple: (test_result, correct_result [, test_name])
        yield self.test_solve(example), 140, "example"


example = '''
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
'''

Day.do_day(day=13, year=2022, part_a=PartA, part_b=PartB)
