from collections import defaultdict
from mylib.aoc_frame import Day


class PartA(Day):
    def parse(self, text, d):  # store puzzle parsing result data into attributes of d
        d.edges = defaultdict(list)
        for line in text.splitlines():
            f, t = line.split("-")
            d.edges[f].append(t)
            d.edges[t].append(f)

    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        return do(d, vertex="start", visited=set(), one_vertex_reusable=False)


class PartB(PartA):
    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        return do(d, vertex="start", visited=set(), one_vertex_reusable=True)


def do(d, vertex, visited, one_vertex_reusable):
    if vertex == "end":
        return 1

    if vertex in visited:
        if vertex == "start" or not one_vertex_reusable:
            return 0
        one_vertex_reusable = False

    if vertex.lower() == vertex:
        visited = visited | {vertex}

    return sum(do(d, t, visited, one_vertex_reusable) for t in d.edges[vertex])


Day.do_day(day=12, year=2021, part_a=PartA, part_b=PartB)
