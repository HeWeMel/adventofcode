import collections
from mylib.aoc_frame import Day, multiply_list, CStream
import nographs as nog


class PartA(Day):
    def parse(self, text, d):  # store puzzle parsing result data into attributes of d
        d.materials = ("geode", "obsidian", "clay", "ore")
        d.blueprints = []
        for blueprint_text in text.splitlines():
            s = CStream(blueprint_text)
            blueprint_no = s.int()
            elements = dict()
            while s.lookahead is not None:
                s.string("Each ")
                robot = s.letters()
                s.string("costs ")
                costs = collections.Counter()
                for cost_text in list(s.loop(s.alphanum)(" ", stop_on=".")):
                    for cost_element in cost_text.split(" and "):
                        cost, material = cost_element.split(" ")
                        costs[material] = int(cost)
                costs_tupel = tuple(costs[material] for material in d.materials)
                elements[d.materials.index(robot)] = costs_tupel
            d.blueprints.append((blueprint_no, elements))

    def go(self, d, minute_limit, blueprint_limit):
        results = []
        for blueprint_no, elements in d.blueprints[:blueprint_limit]:
            print(f"{blueprint_no=}")

            max_needed = [max(elements[robot][product] for robot in range(4))
                          for product in range(4)]

            def next_edges(state, t):
                minutes_left = minute_limit - t.depth
                if minutes_left == 1:  # Stop generation options/edges when last minute starts
                    return
                produces, production = state
                next_produces = tuple(a + b for a, b in zip(produces, production))
                blocked_robots_needs = []
                number_of_buying_options = 0
                for robot in range(4):  # Report buying this robot, if possible, as option
                    # Having this robot in future rounds helps to enable buying options?
                    if robot > 0 and max_needed[robot] <= production[robot]:
                        continue  # No? Do not buy it
                    costs = elements[robot]
                    if any(c > p for c, p in zip(costs, produces)):  # not possible
                        blocked_robots_needs.append(costs)  # store the costs it would need
                        continue
                    # Edge weight: Buying a geode robot is "no problem", everything else "costs"
                    # as much as not buying one looses for the rest of the minutes)
                    yield (tuple(n - c for n, c in zip(next_produces, costs)),  # produces-costs
                           tuple(v + 1 if k == robot else v
                                 for k, v in enumerate(production))   # production[robot] += 1
                           ), 0 if robot == 0 else minutes_left
                    number_of_buying_options += 1
                if number_of_buying_options > 0:  # No robot can be bought: waiting makes sense
                    # Otherwise, waiting is only allowed if this unlocks robots in the future.
                    for needs in blocked_robots_needs:
                        if all(a + (minutes_left - 1) * b >= n
                               for a, b, n in zip(produces, production, needs)):
                            break  # Robot will be unlocked in the future -> Waiting can make sense
                    else:
                        return  # No: waiting is no option
                # Report waiting as option/edge. For weight see above.
                yield (next_produces, production), minutes_left

            start = ((0, 0, 0, 0), (0, 0, 0, 1))
            t = nog.TraversalShortestPaths(next_edges)
            for state in t.start_from(start):
                if t.depth == minute_limit - 1:
                    produces, production = state
                    geodes = produces[0] + production[
                        0]  # last minute is just waiting/producing
                    break
            else:
                raise RuntimeError("No best path of required length found")

            results.append((blueprint_no, geodes))
        return results

    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        results = self.go(d, 24, 100)
        return sum(blueprint_no * max_geodes for blueprint_no, max_geodes in results)

    def tests(self):  # yield testcases as tuple: (test_result, correct_result [, test_name])
        yield self.test_solve(example, "config"), 33, example


example = '''
Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.
'''


class PartB(PartA):
    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        results = self.go(d, 32, 3)
        return multiply_list([max_geodes for blueprint_no, max_geodes in results])

    def tests(self):  # yield testcases as tuple: (test_result, correct_result [, test_name])
        yield self.test_solve(example, "config"), 56*62, example


Day.do_day(day=19, year=2022, part_a=PartA, part_b=PartB)
