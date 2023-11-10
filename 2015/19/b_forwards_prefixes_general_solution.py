import re
from collections import defaultdict
from mylib.aoc_frame import Day
from collections.abc import Iterator
from typing import Iterable
import functools


class PartA(Day):

    @staticmethod
    def replace_two_character_pairs(text: str) -> str:
        """
        Replace two-character strings like [A-Z][a-z] by a (new) single character.

        Here, they are replaced just by characters 0 to 9, so it works only up to 10
        distinct two-character strings. Could be changed if necessary.
        """
        distinct_pairs = set(re.findall(r"[A-Z][a-z]", text))
        i = 0
        for pair in distinct_pairs:
            if i > 9:
                raise RuntimeError("More than 10 two-character tokens")
            text = text.replace(pair, str(i))
            i += 1
        return text

    @staticmethod
    def text_to_medicine_and_rules(text: str) -> tuple[str, dict[str, list[str]]]:
        """
        Parse text into the medicine string and the rules. Report the rules as
        dictionary from the left-side string to a list of right-side strings.
        """
        lines = text.splitlines()

        medicine = lines[-1]

        rules = defaultdict(list)
        right_strings = set()
        for line in lines[0:-2]:
            left, right = line.split(" => ")
            rules[left].append(right)
            right_strings.add(right)

        return medicine, rules

    def parse(self, text, d):
        """ Simplify the input, parse it, and store medicine and rules in *d* """
        text = self.replace_two_character_pairs(text)
        d.medicine, d.rules = self.text_to_medicine_and_rules(text)

    @staticmethod
    def apply_rules_at_position(
            s: str, i: int, rules: dict[str, list[str]]
    ) -> Iterator[str]:
        """
        Apply each matching rule on the one-character string s[i] and yield the
        results
        """
        c_from = s[i]
        for to_c in rules[c_from]:
            medicine_variant_list = list(s)
            medicine_variant_list[i] = to_c
            medicine_variant = "".join(medicine_variant_list)
            yield medicine_variant

    def compute(self, d):
        """
        For each character in the medicine string, apply all matching rules.
        Collect the results and return their number.
        """
        variants = set()
        for i in range(len(d.medicine)):
            variants.update(self.apply_rules_at_position(d.medicine, i, d.rules))
        return len(variants)

    def tests(self):
        """ Yield testcases as tuple: (test_result, correct_result [, test_name]) """
        yield self.test_solve(example1, None), 4, "example1"
        yield self.test_solve(example2, None), 7, "example2"
        yield self.test_solve(example3, None), 7, "example3"


example1 = '''
H => HO
H => OH
O => HH

HOH
'''

example2 = '''
H => HO
H => OH
O => HH

HOHOHO
'''

example3 = '''
Ho => HoO
Ho => OHo
O => HoHo

HoOHoOHoO
'''


class PartB(PartA):

    def compute(self, d):
        """
        For a rising limit of allowed rule application steps, compute
        all prefixes of the medicine string that can be computed.
        When the goal itself is generates as prefix, report the reached step limit.
        """
        medicine = d.medicine
        medicine_len = len(medicine)
        rules = d.rules

        @functools.cache
        def possible_prefixes(start: str, goal: str, depth: int) -> Iterable[str]:
            """
            Report all prefixes of goal that can be generated in exactly
            depth_limit steps of rule application starting from string start.

            Cache results in an unlimited cache. This cache, together with the special
            signature and purpose of this function, is the main point of the solution.
            """
            if depth == 0:
                # We are not allowed to do any steps:
                # If start directly is a prefix of goal, report it, otherwise nothing
                if goal.startswith(start):
                    return [start]
                else:
                    return []

            results = set()

            if len(start) == 1:
                # We are allowed to do some steps and have to start with just one
                # character: For each rule for this character, we apply the rule (this
                # costs us one step) and ask for possible prefixes that can be
                # generated from there on with the remaining steps. Collect the results
                # (without duplicates).
                for to_c in rules[start]:
                    results.update(possible_prefixes(to_c, goal, depth-1))
                return results

            # We are allowed to do some steps and have to start with more than one
            # character. We try out all possible distributions of the allowed steps
            # between the first character of the start string and all others of it.
            start_left_part, start_right_part = start[0], start[1:]
            for depth_left in range(0, depth+1):
                # For each case, we search for possible prefixes of the goal that we
                # can get with the steps allowed for the first character
                depth_right = depth - depth_left
                for possible_left in possible_prefixes(
                        start_left_part, goal, depth_left
                ):
                    # For each prefix, we ask for prefixes of the rest of the goal
                    # string that can be reached with the remaining steps.
                    for possible_right in possible_prefixes(
                        start_right_part, goal[len(possible_left):], depth_right
                    ):
                        # Each combination of the prefixes is a prefix of the
                        # original problem
                        results.add(possible_left+possible_right)
            return results

        for depth in range(0, 999):
            for prefix in possible_prefixes("e", medicine, depth):
                if len(prefix) == medicine_len:
                    print(depth, possible_prefixes.cache_info())
                    return depth
        return None

    def tests(self):
        """ Yield testcases as tuple: (test_result, correct_result [, test_name]) """
        yield self.test_solve(example4, None), 3, "example4"
        yield self.test_solve(example5, None), 6, "example5"


example4 = '''
e => H
e => O
H => HO
H => OH
O => HH

HOH
'''

example5 = '''
e => H
e => O
H => HO
H => OH
O => HH

HOHOHO
'''

Day.do_day(day=19, year=2015, part_a=PartA, part_b=PartB)
