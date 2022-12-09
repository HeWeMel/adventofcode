from mylib.aoc_frame import Day


class PartA(Day):
    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        head_x = head_y = tail_x = tail_y = 0
        positions = {(tail_x, tail_y)}  # of (x, y)
        for line in d.text.splitlines():
            direction, number_text = line.split()
            for i in range(int(number_text)):
                if direction == "R" or direction == "L":
                    head_x += 1 if direction == "R" else -1
                    if abs(head_x - tail_x) > 1:  # touch lost
                        if head_y != tail_y:  # same y
                            tail_y += +1 if head_y > tail_y else -1
                        tail_x += +1 if head_x - tail_x > 0 else -1
                else:
                    head_y += 1 if direction == "D" else -1
                    if abs(head_y - tail_y) > 1:  # touch lost
                        if head_x != tail_x:  # same y
                            tail_x += +1 if head_x > tail_x else -1
                        tail_y += +1 if head_y - tail_y > 0 else -1
                positions.add((tail_x, tail_y))

        return len(positions)

    def tests(self):  # yield testcases as tuple: (test_result, correct_result [, test_name])
        # if True is True:  # remove to activate
        #    return ()
        yield self.test_solve('''
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
'''), 13, "example"


class PartB(PartA):
    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        number_of_knots = 10
        knots = [[0, 0] for i in range(number_of_knots)]
        positions = {(0, 0)}  # (x, y) of first knot
        for line in d.text.splitlines():
            direction, number_text = line.split()
            for i in range(int(number_text)):
                head = knots[0]
                match direction:
                    case "R":
                        head[0] += 1
                    case "L":
                        head[0] -= 1
                    case "D":
                        head[1] += 1
                    case "U":
                        head[1] -= 1

                for k in range(1, number_of_knots):  # following knots
                    tail = knots[k]
                    for coordinate, other in ((0, 1), (1, 0)):
                        if abs(head[coordinate] - tail[coordinate]) > 1:  # touch lost
                            if head[other] != tail[other]:
                                tail[other] += 1 if head[other] > tail[other] else -1
                            tail[coordinate] += 1 if head[coordinate] - tail[coordinate] > 0 else -1
                    head = tail
                positions.add((head[0], head[1]))

        return len(positions)
    def tests(self):  # yield testcases as tuple: (test_result, correct_result [, test_name])
        # if True is True:  # remove to activate
        #    return ()
        yield self.test_solve('''
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
'''), 1, "example"
        yield self.test_solve('''
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
'''), 36, "example"


Day.do_day(day=9, year=2022, part_a=PartA, part_b=PartB)
