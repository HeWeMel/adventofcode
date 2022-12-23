import itertools
from mylib.aoc_frame import Day, CStream
import nographs as nog


class PartA(Day):
    def parse(self, text, d):  # store puzzle parsing result data into attributes of d
        board_text, d.path = text.split("\n\n")
        board_lines = board_text.splitlines()
        max_x = max(len(line) for line in board_lines)
        d.board = [" " + line + " " + (" " * (max_x - len(line)))
                   for line in board_lines]
        empty_row = " " * (max_x+2)
        d.board = [empty_row] + d.board + [empty_row]
        d.array = nog.Array(d.board)

    def part_config(self, d):  # from puzzle string to dict of parsing results
        pass

    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        a: nog.Array = d.array
        moves = ((0, 1), (1, 0), (0, -1), (-1, 0))
        row = 1
        for column in itertools.count(1):
            if a[(row, column)] == ".":
                break
        pos = nog.Position.at(row, column)
        facing = 0

        cs = CStream(d.path)
        while cs.lookahead is not None:
            if "0" <= cs.lookahead <= "9":
                steps = cs.int()
                for step in range(steps):
                    move = moves[facing]
                    next_pos = pos + move
                    next_c = a[next_pos]
                    if next_c == " ":
                        move_back = [-c for c in move]
                        next_pos = pos
                        while a[next_pos+move_back] != " ":
                            next_pos += move_back
                    if next_c == "#":
                        break
                    pos = next_pos
            else:
                match next(cs):
                    case "R":
                        facing = (facing + 1) % 4
                    case "L":
                        facing = 3- ((3-facing) + 1) % 4
                    case _:
                        raise RuntimeError("Illegal direction")

        return 1000 * pos[0] + 4 * pos[1] + facing

    def tests(self):  # yield testcases as tuple: (test_result, correct_result [, test_name])
        yield self.test_solve(example, "config"), 6032, "example"


example = '''
        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5
'''


class PartB(PartA):
    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        a: nog.Array = d.array

        #         R,      D,      L,       U
        moves = ((0, 1), (1, 0), (0, -1), (-1, 0))

        # map_y, map_x, facing -> map_y, map_x, facing, swap_xy, mirror_y, mirror_x
        wrapping = {
            (0, 1, 3): (3, 0, 0, True, False, False),
            (3, 0, 2): (0, 1, 1, True, False, False),

            (0, 2, 3): (3, 0, 3, False, True, False),
            (3, 0, 1): (0, 2, 1, False, True, False),

            (0, 2, 0): (2, 1, 2, False, True, False),
            (2, 1, 0): (0, 2, 2, False, True, False),

            (0, 2, 1): (1, 1, 2, True, False, False),
            (1, 1, 0): (0, 2, 3, True, False, False),

            (2, 1, 1): (3, 0, 2, True, False, False),
            (3, 0, 0): (2, 1, 3, True, False, False),

            (2, 0, 2): (0, 1, 0, False, True, False),
            (0, 1, 2): (2, 0, 0, False, True, False),

            (2, 0, 3): (1, 1, 0, True, False, False),
            (1, 1, 2): (2, 0, 1, True, False, False),
        }

        edge_len = (len(d.board)-2) // 4

        row = 1
        for column in itertools.count(1):
            if a[(row, column)] == ".":
                break
        pos = nog.Position.at(row, column)
        facing = 0

        cs = CStream(d.path)
        while cs.lookahead is not None:
            if "0" <= cs.lookahead <= "9":
                steps = cs.int()
                for step in range(steps):
                    move = moves[facing]
                    next_pos = pos + move
                    next_facing = facing
                    next_c = a[next_pos]
                    if next_c == " ":
                        map_y, co_y = divmod(pos[0]-1, edge_len)
                        map_x, co_x = divmod(pos[1]-1, edge_len)
                        map_y, map_x, next_facing, swap_xy, mirror_y, mirror_x = (
                            wrapping[(map_y, map_x, facing)])

                        if swap_xy:
                            co_y, co_x = co_x, co_y
                        if mirror_x:
                            co_x = edge_len-1 - co_x
                        if mirror_y:
                            co_y = edge_len-1 - co_y
                        next_pos = nog.Position.at((map_y*edge_len+co_y+1),
                                                   (map_x*edge_len+co_x+1))
                        next_c = a[next_pos]
                    if next_c == "#":
                        break
                    elif next_c != ".":
                        raise RuntimeError("Illegal case")
                    pos, facing = next_pos, next_facing
                    # a[pos] = str(facing)
            else:
                match next(cs):
                    case "R":
                        facing = (facing + 1) % 4
                    case "L":
                        facing = 3 - ((3-facing) + 1) % 4
                    case _:
                        raise RuntimeError("Illegal direction")

        return 1000 * pos[0] + 4 * pos[1] + facing

    def tests(self):  # yield testcases as tuple: (test_result, correct_result [, test_name])
        return ()


Day.do_day(day=22, year=2022, part_a=PartA, part_b=PartB)
