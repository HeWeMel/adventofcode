import functools
import itertools

from mylib.aoc_frame import Day
import nographs as nog


class PartA(Day):
    def parse(self, text, d):  # store puzzle parsing result data into attributes of d
        a = nog.Array(text.splitlines())
        moves = nog.Position.moves(zero_move=True)

        limits = a.limits()
        v_mirror = limits[0][1] - 1
        h_mirror = limits[1][1] - 1

        d.my_start = nog.Position.at(0, 1)
        d.my_goal = nog.Position(nog.Position(a.size())+(-1, -2))

        blizzard_vector = {">": (0, 1), "<": (0, -1), "^": (-1, 0), "v": (1, 0)}
        blizzard_start_and_vector = tuple((pos, blizzard_vector[c])
                                          for c in blizzard_vector
                                          for pos in a.findall(c))
        d.blizzards_start_pos = tuple(pos for pos, vector in blizzard_start_and_vector)
        blizzards_dir = [vector for pos, vector in blizzard_start_and_vector]

        @functools.cache
        def next_blizzards(blizzards_pos):
            next_blizzards_pos = []
            for pos, direction in zip(blizzards_pos, blizzards_dir):
                next_pos = pos + direction
                if a[next_pos] == "#":
                    if direction[0]:  # vertically moving blizzard
                        next_pos = nog.Position.at(v_mirror - pos[0], pos[1])
                    else:  # horizontally moving blizzard
                        next_pos = nog.Position.at(pos[0], h_mirror - pos[1])
                next_blizzards_pos.append(next_pos)
            return tuple(next_blizzards_pos), set(next_blizzards_pos)

        def next_vertices(state, _):
            me, blizzards_pos = state
            next_blizzard_pos, next_blizzard_pos_set = next_blizzards(blizzards_pos)
            for next_me in me.neighbors(moves, limits):
                if a[next_me] != "#" and next_me not in next_blizzard_pos_set:
                    yield (next_me, next_blizzard_pos), 1

        d.traversal = nog.TraversalAStar(next_vertices)

    @staticmethod
    def distance_to(goal):
        def distance_to_goal(state):
            me, blizzards_pos = state
            return me.manhattan_distance(goal)
        return distance_to_goal

    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        for res_me, res_blizzards_pos in d.traversal.start_from(
                self.distance_to(d.my_goal), (d.my_start, d.blizzards_start_pos)):
            if res_me == d.my_goal:
                return d.traversal.depth  # part 1: 242

    def tests(self):  # yield testcases as tuple: (test_result, correct_result [, test_name])
        yield self.test_solve(example, None), 18, "example"


class PartB(PartA):
    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        blizzards = d.blizzards_start_pos
        travel_length = 0
        for start, goal in itertools.pairwise([d.my_start, d.my_goal, d.my_start, d.my_goal]):
            for me, blizzards in d.traversal.start_from(
                    self.distance_to(goal), (start, blizzards)):
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
