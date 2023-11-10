import re
import functools
import itertools
from collections import defaultdict
from typing import Iterable
import timeit


def normalize_input(text: str) -> str:
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


def normalized_input_to_medicine_and_rules(
        text: str
) -> tuple[str, dict[str, list[str]]]:
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


def solve(problem: str) -> None:
    """
    For a rising limit of allowed rule application steps, compute
    all prefixes of the medicine string that can be computed.
    When the goal itself is generates as prefix, report the reached step limit.
    """
    medicine, rules = normalized_input_to_medicine_and_rules(normalize_input(problem))

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

        prefixes = set()

        if len(start) == 1:
            # We are allowed to do some steps and have to start with just one character:
            # For each rule for this character, we apply the rule (this costs us one
            # step) and ask for possible prefixes that can be generated from there on
            # with the remaining steps. Collect the results (without duplicates).
            for to_c in rules[start]:
                prefixes.update(possible_prefixes(to_c, goal, depth - 1))
            return prefixes

        # We are allowed to do some steps and have to start with more than one
        # character. We try out all possible distributions of the allowed steps
        # between the first character of the start string and all others of it.
        start_left_part, start_right_part = start[0], start[1:]
        for depth_left in range(0, depth + 1):
            # For each case, we search for possible prefixes of the goal that we
            # can get with the steps allowed for the first character
            depth_right = depth - depth_left
            for prefix_left in possible_prefixes(start_left_part, goal, depth_left):
                # For each prefix, we ask for prefixes of the rest of the goal
                # string that can be reached with the remaining steps.
                for prefix_right in possible_prefixes(
                        start_right_part, goal[len(prefix_left):], depth_right
                ):
                    # Each combination of the prefixes is a prefix of the
                    # original problem
                    prefixes.add(prefix_left + prefix_right)
        return prefixes

    medicine_len = len(medicine)
    for depth in itertools.count():
        for prefix in possible_prefixes("e", medicine, depth):
            if len(prefix) == medicine_len:
                print("Solution:", depth)
                print("Cache Info:", possible_prefixes.cache_info())
                return
    raise RuntimeError()


with open('day19_other_input.txt') as f:
    text = f.read()
    print(f"Runtime: {timeit.timeit(lambda: solve(text), number=1):.3f}")
