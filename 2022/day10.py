from mylib.aoc_frame import Day


class PartA(Day):
    def parse(self, text, d):
        def run(program):
            x = 1
            for line in program.splitlines():
                match line.split():
                    case ["noop"]:
                        yield x
                    case ["addx", value_text]:
                        yield x
                        yield x
                        x += int(value_text)

        d.iterator = run(text)

    def compute(self, d):
        signal_sum = 0
        for cycle, value in enumerate(d.iterator, 1):
            if cycle in {20, 60, 100, 140, 180, 220}:
                signal_sum += cycle * value
        return signal_sum

    example = '''
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
'''

    def tests(self):
        yield self.test_solve(self.example), 13140, "example"


class PartB(PartA):
    def compute(self, d):
        for screen_y in range(6):
            for screen_x in range(40):
                x_register = next(d.iterator)
                print("#" if x_register-1 <= screen_x <= x_register+1 else ".", end="")
            print()
        return None

    def tests(self):
        yield self.test_solve(self.example), None, "example"


Day.do_day(day=10, year=2022, part_a=PartA, part_b=PartB)
