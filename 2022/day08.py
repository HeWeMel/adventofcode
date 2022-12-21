from mylib.aoc_frame import Day


class PartA(Day):
    def parse(self, text, d):  # store puzzle parsing result data into attributes of d
        d.array = text.splitlines()
        d.size_y = len(d.array)
        d.size_x = len(d.array[0])

    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        a = d.array

        visible = 0
        for y in range(d.size_y):
            for x in range(d.size_x):
                h = a[y][x]
                if (
                        any(a[ty][x] >= h for ty in range(0, y)) and
                        any(a[ty][x] >= h for ty in range(y+1, d.size_y)) and
                        any(a[y][tx] >= h for tx in range(0, x)) and
                        any(a[y][tx] >= h for tx in range(x+1, d.size_x))
                ):
                    continue
                visible += 1
        return visible

    def tests(self):  # yield testcases as tuple: (test_result, correct_result [, test_name])
        yield self.test_solve(example), 21, "example"


class PartB(PartA):
    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        a = d.array

        def viewing_distance_for_trees(trees):
            distance = 0
            for y, x, h in trees:
                distance += 1
                if a[y][x] >= h:
                    break
            return distance

        highest_score = 0
        for y in range(d.size_y):
            for x in range(d.size_x):
                h = a[y][x]
                score = (
                    viewing_distance_for_trees((ty, x, h) for ty in range(y-1, -1, -1)) *
                    viewing_distance_for_trees((ty, x, h) for ty in range(y+1, d.size_y)) *
                    viewing_distance_for_trees((y, tx, h) for tx in range(x-1, -1, -1)) *
                    viewing_distance_for_trees((y, tx, h) for tx in range(x+1, d.size_x))
                )
                highest_score = max(highest_score, score)
        return highest_score

    def tests(self):  # yield testcases as tuple: (test_result, correct_result [, test_name])
        yield self.test_solve(example), 8, "example"


example = '''
30373
25512
65332
33549
35390
'''

Day.do_day(day=8, year=2022, part_a=PartA, part_b=PartB)
