import functools
import operator
from mylib.aoc_frame import Day


class PartA(Day):
    def parse(self, text, d):  # store puzzle parsing result data into attributes of d
        d.starting_items = []
        d.operations = []
        d.divisors = []
        d.true_throws_to = []
        d.false_throws_to = []

        for block in text.split("\n\n"):
            lines = iter(line.split() for line in block.splitlines())
            _ = next(lines)
            items = next(lines)[2:]
            value_items = "".join(items).split(",")
            d.starting_items.append(list(map(int, value_items)))
            operation, value = next(lines)[4:6]
            d.operations.append((operation, value))
            divisor = next(lines)[3]
            d.divisors.append(int(divisor))
            to_monkey = next(lines)[5]
            d.true_throws_to.append(int(to_monkey))
            to_monkey = next(lines)[5]
            d.false_throws_to.append(int(to_monkey))

    @staticmethod
    def run(d, rounds, handle_worry_level):
        monkeys = len(d.starting_items)
        activities = [0] * monkeys
        items = d.starting_items
        for round_no in range(rounds):
            for monkey in range(monkeys):
                current_items = items[monkey]
                items[monkey] = []
                for worry_level in current_items:
                    activities[monkey] += 1
                    operation, value_text = d.operations[monkey]
                    value = worry_level if value_text == "old" else int(value_text)
                    match operation:
                        case "+":
                            worry_level = worry_level + value
                        case "-":
                            worry_level = worry_level - value
                        case "*":
                            worry_level = worry_level * value
                        case "/":
                            worry_level = worry_level / value
                    worry_level = handle_worry_level(worry_level)
                    if worry_level % d.divisors[monkey] == 0:
                        to_monkey = d.true_throws_to[monkey]
                    else:
                        to_monkey = d.false_throws_to[monkey]
                    items[to_monkey].append(worry_level)
        i = reversed(sorted(activities))
        return next(i) * next(i)

    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        return self.run(d, 20, lambda l: l // 3)

    def tests(self):  # yield testcases as tuple: (test_result, correct_result [, test_name])
        yield self.test_solve(example), 10605, "example"


class PartB(PartA):
    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        worry_level_modulo = functools.reduce(operator.mul, d.divisors)
        return self.run(d, 10000, lambda l: l % worry_level_modulo)

    def tests(self):  # yield testcases as tuple: (test_result, correct_result [, test_name])
        yield self.test_solve(example), 2713310158, "example"


example = '''
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
'''

Day.do_day(day=11, year=2022, part_a=PartA, part_b=PartB)
