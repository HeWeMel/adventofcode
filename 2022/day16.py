import itertools
from mylib.aoc_frame import Day, CStream
import nographs as nog


class PartA(Day):
    def parse(self, text, d):  # store puzzle parsing result data into attributes of d
        d.rate = dict()
        d.tunnels = dict()
        for line in text.splitlines():
            s = CStream(line)
            s.alphanum()
            valve = s.letters()
            d.rate[valve] = s.int()
            s.string("valve")
            s.string(" ")
            d.tunnels[valve] = list(s.loop(s.letters, separator_needed=", ")())
        d.all_relevant_valves = frozenset(valve for valve, rate in d.rate.items() if rate != 0)
        d.max_release = sum(rate for valve, rate in d.rate.items())
        max_release = d.max_release

        def next_edges(state: tuple[str, frozenset, int], _):
            valve, closed, releasing = state
            if valve in closed:
                yield (valve, closed.difference([valve]), releasing + d.rate[valve]
                       ), max_release - releasing
            for to_valve in d.tunnels[valve]:
                yield (to_valve, closed, releasing), max_release - releasing

        d.next_edges = next_edges

    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        minutes_limit = 30
        t = nog.TraversalShortestPaths(d.next_edges)
        for state in t.start_from(("AA", d.all_relevant_valves, 0)):
            valve, closed, releasing = state
            if t.depth == minutes_limit or not closed:
                return d.max_release * minutes_limit - t.distance

    def tests(self):  # yield testcases as tuple: (test_result, correct_result [, test_name])
        yield self.test_solve(example, None), 1651, "example"


class PartB(PartA):
    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        def next_edges_we(state: tuple[str, str, frozenset, int], _):
            me, elephant, closed, releasing = state
            for me_next, elephant_next in itertools.product(
                    next_edges((me, closed, releasing), _),
                    next_edges((elephant, closed, releasing), _)
            ):
                (me_to, me_closed, me_releasing), weight = me_next
                (el_to, el_closed, el_releasing), weight = elephant_next
                if not(me_closed == el_closed and me_closed != closed):  # open the same is forbidden
                    yield (me_to, el_to, me_closed.intersection(el_closed),
                           releasing + (me_releasing-releasing) + (el_releasing-releasing)
                           ), weight

        minutes_limit = 26
        next_edges = d.next_edges
        t = nog.TraversalShortestPaths(next_edges_we)
        for state in t.start_from(("AA", "AA", d.all_relevant_valves, 0)):
            valve, valve_elephant, closed, releasing = state
            if t.depth == minutes_limit or not closed:
                return d.max_release * minutes_limit - t.distance

    def tests(self):  # yield testcases as tuple: (test_result, correct_result [, test_name])
        yield self.test_solve(example, None), 1707, "example"


example = '''
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
'''

Day.do_day(day=16, year=2022, part_a=PartA, part_b=PartB)
