from collections import defaultdict
from mylib.aoc_frame import Day
import operator


class PartA(Day):
    def parse(self, text, d):  # store puzzle parsing result data into attributes of d
        d.rules = dict()
        for line in text.splitlines():
            name, expr = line.split(": ")
            if "0" <= expr[0] <= "9":
                d.rules[name] = ("val", int(expr))
            else:
                m1, op, m2 = expr.split()
                d.rules[name] = ("expr", (m1, op, m2))

    def part_config(self, d):  # from puzzle string to dict of parsing results
        d.result_monkey = "root"

    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        # helper functions for missing operators
        def argument2(res, m):
            return m

        def inv_div(res, m):
            return m // res

        def inv_sub(res, m):
            return m - res

        # -- operators for opcodes, expressions: res = m1 op m2
        # res = op[opc](m1, m2)
        op_for_opc = {"+": operator.add, "*": operator.mul, "/": operator.floordiv,
                      "-": operator.sub, "=": operator.eq}
        # m2 = op[opc](res, m1)
        op_for_opc_m2 = {"+": operator.sub, "*": operator.floordiv, "/": inv_div,
                         "-": inv_sub, "=": argument2}
        # m1 = op[opc](res, m2)
        op_for_opc_m1 = {"+": operator.sub, "*": operator.floordiv, "/": operator.mul,
                         "-": operator.add, "=": argument2}

        waiting = defaultdict(list)
        expressions = dict()
        expr_wait_count = dict()
        val = dict()
        for name, body in d.rules.items():
            match body:
                case ["ignore", expr]:
                    continue
                case ["val", value]:
                    val[name] = value
                    known = waiting[name]
                case ["expr", [m1, op, m2]]:
                    if op == "=":
                        val[name] = True
                    expressions[name] = (m1, op, m2)
                    need_count = 0
                    for m in (name, m1, m2):
                        if m not in val:
                            waiting[m].append(name)
                            need_count += 1
                    expr_wait_count[name] = need_count
                    known = [name] if need_count == 1 else []
                case _:
                    raise RuntimeError("Rule type not found")
            while known:
                name = known.pop()
                if expr_wait_count[name] == 3:
                    expr_wait_count[name] = 2
                else:
                    m1, op, m2, = expressions[name]
                    match (m1 in val, m2 in val, name in val):
                        case (True, True, False):
                            val[name] = op_for_opc[op](val[m1], val[m2])
                            known.extend(waiting[name])
                        case (True, False, True):
                            val[m2] = op_for_opc_m2[op](val[name], val[m1])
                            known.extend(waiting[m2])
                        case (False, True, True):
                            val[m1] = op_for_opc_m1[op](val[name], val[m2])
                            known.extend(waiting[m1])

            if d.result_monkey in val:
                return val[d.result_monkey]

    def tests(self):  # yield testcases as tuple: (test_result, correct_result [, test_name])
        yield self.test_solve(example, "config"), 152, "example"


class PartB(PartA):
    def part_config(self, d):  # from puzzle string to dict of parsing results
        d.result_monkey = "humn"
        m_type, (m1, op, m2) = d.rules["root"]
        d.rules["root"] = (m_type, (m1, "=", m2))
        d.rules["humn"] = ("ignore", ())

    def tests(self):  # yield testcases as tuple: (test_result, correct_result [, test_name])
        yield self.test_solve(example, None), 301, "example"


example = '''
root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32
'''

Day.do_day(day=21, year=2022, part_a=PartA, part_b=PartB)
