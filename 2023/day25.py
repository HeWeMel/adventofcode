from collections import defaultdict
from typing import Iterable
from aocd.models import Puzzle
from mylib.aoc_frame2 import Day
import nographs as nog


class PartA(Day):
    def compute(self, text, config):
        edges_from_vertex = defaultdict(list)
        edges = []
        nodes = set()
        for line in text.splitlines():
            node_left, right = line.split(": ")
            nodes.add(node_left)
            for node_right in right.split():
                edge_i = len(edges)
                edges.append((node_left, node_right))
                edges_from_vertex[node_left].append((edge_i, node_right))
                edges_from_vertex[node_right].append((edge_i, node_left))
                nodes.add(node_right)

        def solve(edges_to_remove: Iterable[int],
                  forbidden_edges: set[int] = frozenset(),
                  level: int = 0):
            for edge_i in edges_to_remove:
                def next_edges(v, _):
                    for edge_i, next_node in edges_from_vertex[v]:
                        if edge_i in next_forbidden_edges:
                            continue
                        yield next_node, edge_i

                next_forbidden_edges = forbidden_edges.union([edge_i])
                v1, v2 = edges[edge_i]
                t = nog.TraversalBreadthFirst(next_labeled_edges=next_edges)
                if level <= 1:
                    t.start_from(v1, build_paths=True).go_to(v2)
                    edges2 = set(edge_i2 for vf2, vt2, edge_i2
                                 in t.paths.iter_labeled_edges_to_start(v2)
                                 if level > 0 or edge_i2 > edge_i)
                    r = solve(edges2, next_forbidden_edges, level + 1)
                    if r is not None:
                        return r
                else:
                    if t.start_from(v1).go_to(v2, fail_silently=True) is None:
                        group1 = list(t.start_from(v1))
                        group2 = list(t.start_from(v2))
                        return (len(group1) + 1) * (len(group2) + 1)
            return None
        return solve(range(len(edges)))

    def tests(self):
        yield self.test_solve(example_a1, "config"), 54, "example1_1"


example_a1 = '''
jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr
'''
puzzle = Puzzle(day=25, year=2023)
PartA().do_part(puzzle)
