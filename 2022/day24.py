import functools
import itertools
from mylib.aoc_frame import Day
import nographs as nog


class PartA(Day):
    def parse(self, text, d):  # store puzzle parsing result data into attributes of d
        a = nog.Array(text.splitlines())
        moves = nog.Position.moves(zero_move=True)
        limits = a.limits()

        def blizzard_generator():
            blizzard_limits = [(1, dim_size - 1) for dim_size in a.size()]
            blizzard_vector = {">": (0, 1), "<": (0, -1), "^": (-1, 0), "v": (1, 0)}
            blizzard_start_and_vector = tuple((pos, blizzard_vector[c])
                                              for c in blizzard_vector
                                              for pos in a.findall(c))
            blizzards_pos = tuple(pos for pos, vector in blizzard_start_and_vector)
            blizzards_dir = [vector for pos, vector in blizzard_start_and_vector]
            while True:
                blizzards_pos = tuple(
                    (pos + direction).wrap_to_cuboid(blizzard_limits)
                    for pos, direction in zip(blizzards_pos, blizzards_dir))
                yield set(blizzards_pos)

        blizzard_iterator = iter(blizzard_generator())

        @functools.cache
        def blizzards(minute):
            return next(blizzard_iterator)

        def next_edges(state, _):
            me, minute = state
            next_minute = minute + 1
            next_blizzards = blizzards(minute)
            for next_me in me.neighbors(moves, limits):
                if a[next_me] != "#" and next_me not in next_blizzards:
                    yield (next_me, next_minute), 1

        d.my_start = nog.Position.at(0, 1)
        d.my_goal = nog.Position(a.size()) + (-1, -2)
        d.traversal = nog.TraversalAStar(next_edges)

    @staticmethod
    def distance_to(goal):
        def distance_to_goal(state):
            me, blizzards_pos = state
            return me.manhattan_distance(goal)
        return distance_to_goal

    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        for res_me, res_minute in d.traversal.start_from(
                self.distance_to(d.my_goal), (d.my_start, 0)):
            if res_me == d.my_goal:
                return d.traversal.depth

    def tests(self):  # yield testcases as tuple: (test_result, correct_result [, test_name])
        yield self.test_solve(example, None), 18, "example"


class PartB(PartA):
    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        travel_length = 0
        minute = 0
        for start, goal in itertools.pairwise([d.my_start, d.my_goal, d.my_start, d.my_goal]):
            for me, minute in d.traversal.start_from(self.distance_to(goal), (start, minute)):
                if me == goal:
                    travel_length += d.traversal.depth
                    break
        return travel_length

    def tests(self):  # yield testcases as tuple: (test_result, correct_result [, test_name])
        yield self.test_solve(example, None), 54, "example"


example = '''
#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#
'''

Day.do_day(day=24, year=2022, part_a=PartA, part_b=PartB)
