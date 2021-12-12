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
        return go(d, True)


class PartB(PartA):
    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        return go(d, False)


def go(d, one_vertex_reused):
    visited = set()
    paths = 0

    def do(f):
        nonlocal visited, paths, one_vertex_reused
        used_here = False
        if f in visited:
            if f in ("start", "end"):
                return
            if one_vertex_reused:
                return
            else:
                one_vertex_reused = True
                used_here = True

        if f.lower() == f:
            visited.add(f)

        if f == "end":
            paths += 1
        else:
            for t in d.edges[f]:
                do(t)

        if used_here:
            one_vertex_reused = False
        else:
            visited -= {f}

    do("start")
    return paths


Day.do_day(day=12, year=2021, part_a=PartA, part_b=PartB)
