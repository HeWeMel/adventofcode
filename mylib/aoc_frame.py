import sys
import functools
import operator
import itertools
import collections.abc
import string
import math
import timeit
from collections.abc import Iterable
from typing import Optional, cast
from aocd.models import Puzzle


def submit(puzzle, answer, value):
    """ answer: answer_a or answer_b """
    print()
    print("--->", answer, ":", value)
    if answer not in ("answer_a", "answer_b"):
        print("(Answer ignored, name neither answer_a nor answer_b)")
        return

    if type(value) == str:
        print("Warning: Answer is type 'str'")
        value_str = value
    elif type(value) == int:
        value_str = str(value)
    else:
        print("Answer ignored, value is neither int nor str, but", type(value))
        return

    if answer == "answer_a" and puzzle.answered_a:
        if value_str == puzzle.answer_a:
            print("---> Ok (already answered, new answer is the same)")
        else:
            print("---> Differs from prev answer:", puzzle.answer_a)
        return

    if answer == "answer_b" and puzzle.answered_b:
        if value_str == puzzle.answer_b:
            print("---> Ok (already answered, new answer is the same)")
        else:
            print("---> Differs from prev answer:", puzzle.answer_b)
        return

    print("Submit? (y)")
    f = sys.stdin
    # line = f.readline().rstrip('\n\r')
    line = f.read(1)
    if line == "y":
        setattr(puzzle, answer, value_str)
        print("Submitted")


class Something:
    """ Instance of this class can be used to dynamically set attributes and get them back """
    pass


class Day:
    """ Subclass this for day 1 solution and then this for day 2 solution"""

    def answer_name(self):  # compute answer name from part class name
        relevant_part = type(self).__name__[:5]
        if relevant_part not in ("PartA", "PartB"):
            raise RuntimeError("Class name must start with PartA or PartB")
        return "answer_" + relevant_part[-1].lower()

    def parse(self, text, d):  # from puzzle string to dict of parsing results
        d.text = text  # override in concrete class

    def part_config(self, d):  # add configuration for this part of the day
        pass

    def compute(self, d):  # from parsed puzzle data to result value or None
        return None if True else 0  # override in concrete class

    @staticmethod
    def check(r, r_ok):  # compares result values, can be adapted
        return r == r_ok

    def tests(self):  # yield testcases as tuple: (input_text, result_value [, test_name])
        return []  # override in concrete class if tests are needed

    def test_solve(self, puzzle_text, config=None):  # combines parse and compute, eases test definition
        d = Something()
        d.config = config
        print("Parse")
        self.parse(puzzle_text.strip("\n"), d)
        print("Config")
        self.part_config(d)
        print("Compute")
        r = self.compute(d)
        return r

    def test(self):  # performs tests, reports puzzle and check results, returns True if all ok
        print("Starting to test...")
        t = timeit.default_timer()
        all_ok = True
        for r, r_ok, *more in self.tests():
            test_name = "" if len(more) == 0 else "'" + more[0] + "' "
            if self.check(r, r_ok):
                print("---> Test " + test_name + "result ok:", r)
            else:
                print("---> Test " + test_name + "result wrong:", r)
                print("---! Expected:", r_ok)
                print()
                all_ok = False
        print(f"Testing finished ({timeit.default_timer() - t:.4f}s)")
        return all_ok

    def do_solve(self, puzzle_text):  # solve by using parse and compute, override if necessary
        print("Starting to solve...")
        t = timeit.default_timer()
        d = Something()
        d.config = None
        print("Parse")
        self.parse(puzzle_text, d)
        print("Config")
        self.part_config(d)
        print("Compute")
        r = self.compute(d)
        print(f"Solving finished ({timeit.default_timer() - t:.4f}s)")
        return r

    def do_part(self, puzzle):
        print("---------- starting for", self.answer_name(), "-----------")
        if self.test():
            text = puzzle.input_data
            r = self.do_solve(text)
            submit(puzzle, self.answer_name(), r)
        print()

    @staticmethod
    def do_day(day, year, part_a, part_b):
        puzzle = Puzzle(day=day, year=year)
        part_a().do_part(puzzle)
        part_b().do_part(puzzle)


# === Useful functions ===
def aoc_div_round_to_zero(a, b):
    return math.trunc(a / b)


def aoc_div_remainder(a, b):
    return a - aoc_div_round_to_zero(a, b) * b


def print_dicts(*dicts):
    """ Print contents of each of the given dicts.
    Example: print_dicts(locals(), d.__dict__) """
    for d in dicts:
        for e in d.items():
            print(e)


def multiply_list(lst):
    """ Multiply the elements that are in the list """
    return functools.reduce(operator.mul, lst)


def wrap_add(i, plus, high_limit, low_limit=0):
    """ Add plus to i, stay within interval [low_limit, high_limit) by wrapping """
    i += plus
    if plus >= 0:
        while i >= high_limit:
            i -= (high_limit - low_limit)
    else:
        while i < low_limit:
            i += (high_limit - low_limit)
    return i


def min_max_corner_pos(positions: Iterable[tuple[float, float]]
                ) -> Optional[tuple[tuple[float, float], tuple[float, float]]]:
    """ Return left upper and right lower corner of the smallest rectangular
    containing all positions, and Null of the positions are empty. """
    try:
        next(iter(positions))
    except StopIteration:
        return None
    y_min = cast(float, min(y for (y, x) in positions))
    y_max = cast(float, max(y for (y, x) in positions))
    x_min = cast(float, min(x for (y, x) in positions))
    x_max = cast(float, max(x for (y, x) in positions))
    return (y_min, x_min), (y_max, x_max)


def print_pos_set(positions: set[tuple[float, float]]):
    min_max_corners = min_max_corner_pos(positions)
    if min_max_corners is None:
        print("-- Positions are empty set --")
        return
    (y_min, x_min), (y_max, x_max) = min_max_corner_pos(positions)
    print(f"-- Positions from ({y_min}, {x_min}) to ({y_max}, {x_max}) --")
    for y in range(y_min, y_max + 1):
        for x in range(x_min, x_max + 1):
            print("#" if (y, x) in positions else ".", end="")
        print()
    print()


class IteratorWithLookahead(collections.abc.Iterator):
    def __init__(self, it: collections.abc.Iterable):
        self.it, self.next_it = itertools.tee(iter(it))
        self._advance()

    def __next__(self):
        self._advance()
        return next(self.it)

    def _advance(self):
        self.lookahead = next(self.next_it, None)


# class Lookahead:
#     def __init__(self, iter):
#         self.iter = iter
#         self.buffer = []
#
#     def __iter__(self):
#         return self
#
#     def next(self):
#         if self.buffer:
#             return self.buffer.pop(0)
#         else:
#             return self.iter.next()
#
#     def lookahead(self, n):
#         """Return an item n entries ahead in the iteration."""
#         while n >= len(self.buffer):
#             try:
#                 self.buffer.append(self.iter.next())
#             except StopIteration:
#                 return None
#         return self.buffer[n]


class CStream(IteratorWithLookahead):
    """An extremely basic lexer / tokenizer for the special purpose, that the next
    kind of token to be read is known in advance or can be determined by a one character
    lookahead by the application, and that other kinds of characters are simply to be
    skipped until the token starts.

    Examples: Get the next integer (and skip characters till then), get the next
    word consisting of just letters (and skip everything till then), then get a list
    of integers connected by one or more of the given separators, then get a list
    of words till the next line break.

    Stream of characters initialized from an Iterable. Offers methods for finding
    and reading tokens (groups of characters) of specific types one by one, while
    skipping all characters that do not belong to the token requested next (optionally,
    stop the search if a stop character occurs). Additionally, a looping function for
    reading lists of tokens of the same kind is offered."""
    def is_end(self):
        return self.lookahead is None

    def from_list(self, first: str, stop_on: str = "", rest: Optional[str] = None):
        """Read over characters that are not in first, and raise StopIteration if either the end
        of the stream is reached or the read character is in stop_on.
        When found, read one character that is within first. Then, if rest is not the
        empty string, read zero or more characters that are in rest. If rest is not given,
        first is used as rest.
        """
        if rest is None:
            rest = first
        while True:
            c = next(self)
            if c in stop_on:
                raise StopIteration()
            if c in first:
                break
        s = c
        while self.lookahead is not None and self.lookahead in rest:
            s = s + next(self)
        return s

    def digits(self, more="", stop_on=""):
        """Like from_list, but for string.digits and *more*."""
        return int(self.from_list(string.digits+more, stop_on))

    def int(self, more="", stop_on=""):
        """Like from_list, but for string.digits, "-" and *more*."""
        return self.digits(more="-" + more, stop_on=stop_on)

    def one_op(self, more="", stop_on=""):
        """Like from_list, but for "+-*/" and *more*."""
        return self.from_list("+-*/"+more, stop_on, "")

    def letters(self, more="", stop_on=""):
        """Like from_list, but for string.ascii_letters and *more*."""
        return self.from_list(string.ascii_letters+more, stop_on)

    def alphanum(self, more="", stop_on=""):
        """Like from_list, but for string.digits, ascii_letters, and *more*."""
        return self.letters(more=string.digits + more, stop_on=stop_on)

    def alphanum_underscore(self, more="", stop_on=""):
        """Like from_list, but for string.digits, ascii_letters, underscore,
        and *more*."""
        return self.alphanum(more="_" + more, stop_on=stop_on)

    def loop(self, func, separator_needed: str = ""):
        """Return a function that can be called like func, but call func
        repeatedly and yield its results until StopIteration occurs.
        If separator_needed is given, stop reading if, after the function call,
        the lookahead is not in seperator_needed, and otherwise, reads over all
        separators in seperator_needed.
        Examples:

        - list(s.loop(s.int)() - Reads and yields integers and reads over
          anything else, till the end of the stream.

        - list(s.loop(s.int)(stop_on="\n")) - Reads and yields integers and reads over
          anything else, till, while searching for the start of an integer,
          a return is reached.

        - list(s.loop(s.int, separator_needed=", ")()) - Reads and yields integers and
          reads over anything else, till, after having read an integer, no separators
          follow. If separators follow, all are read over before starting to read the
          next int.

        - list((s := CStream(text)).loop(s.int)())
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            while True:
                try:
                    result = func(*args, **kwargs)
                except StopIteration:
                    break
                yield result
                if separator_needed != "":
                    if self.lookahead is None or self.lookahead not in separator_needed:
                        break
                    while self.lookahead in separator_needed:
                        next(self)
        return wrapper

    def string(self, text):
        """Skip anything till *text* comes. Then consume the letters of text."""
        window = "".join(next(self) for i in range(len(text)))
        while window != text:
            window = window[1:] + next(self)
