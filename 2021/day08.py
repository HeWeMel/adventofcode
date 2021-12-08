from mylib.aoc_frame import Day
import itertools


class PartA(Day):
    def parse(self, text, d):  # store puzzle parsing result data into attributes of d
        d.input = [[part.split(" ") for part in line.split(" | ")] for line in text.splitlines()]

    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        r = 0
        for example_patterns, output_patterns in d.input:
            r += sum(1 for pattern in output_patterns
                     if len(pattern) in [2, 3, 4, 7])
        return r


class PartB(PartA):
    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        segments = "abcdefg"
        correct_patterns = ("abcefg", "cf", "acdeg", "acdfg", "bcdf", "abdfg", "abdefg",
                            "acf", "abcdefg", "abcdfg")
        correct_values = {correct_patterns[i]: str(i) for i in range(len(correct_patterns))}
        def sort_str(s): return "".join(sorted(s))

        r = 0
        for example_patterns, output_patterns in d.input:
            patterns = example_patterns + output_patterns

            perms = itertools.permutations(segments, 7)
            for perm in perms:
                table = str.maketrans("".join(perm), segments)
                if all((sort_str(p.translate(table)) in correct_patterns) for p in patterns):
                    break

            r += int("".join(correct_values[sort_str(p.translate(table))] for p in output_patterns))
        return r


Day.do_day(day=8, year=2021, part_a=PartA, part_b=PartB)
