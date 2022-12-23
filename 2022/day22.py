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
        wrapping_number = 1 if d.config is not None else 0  # a

        #         0:R,    1:D,    2:L,     3:U
        moves = ((0, 1), (1, 0), (0, -1), (-1, 0))

        # Wrapping per move from one "open" edge to the other.
        # Symmetric pair are left out, they will be generated afterwards.
        # Elements: map_y, map_x, facing -> map_y, map_x, facing
        wrapping = ({
            # wrapping definition for input data
            # left / right turns
            (0, 1, 3): [3, 0, 0],
            (2, 0, 3): [1, 1, 0],
            (0, 2, 1): [1, 1, 2],
            (2, 1, 1): [3, 0, 2],
            # 0 degrees
            (0, 2, 3): [3, 0, 3],
            # 180 degrees
            (2, 0, 2): [0, 1, 0],
            (0, 2, 0): [2, 1, 2],
        }, {
            # wrapping definition for example data
            # left / right turns
            (1, 2, 0): [2, 3, 1],
            (0, 2, 2): [1, 1, 1],
            (2, 3, 1): [1, 0, 0],
            (1, 1, 1): [2, 2, 0],
            # 0 degrees
            # 180 degrees
            (0, 2, 3): [1, 0, 1],
            (0, 2, 0): [2, 3, 2],
            (2, 2, 1): [1, 0, 3],
        })[wrapping_number]
        wrapping_items = list(wrapping.items())
        wrapping.update(  # add symmetric edge change, with reversed directions
            ((to_map_y, to_map_x, (to_dir + 2) % 4), (from_map_y, from_map_x, (from_dir + 2) % 4))
            for (from_map_y, from_map_x, from_dir), (to_map_y, to_map_x, to_dir)
            in wrapping_items)

        dir_change_to_coo_change = {
            # left / right
            (3, 0): (True, False, False),  # next is same backwards
            (2, 1): (True, False, False),
            (1, 2): (True, False, False),  # next is same backwards
            (0, 3): (True, False, False),
            (0, 1): (True, True, True),  # next is same backwards
            (3, 2): (True, True, True),
            (1, 0): (True, True, True),  # next is same backwards
            (2, 3): (True, True, True),
            (3, 1): (False, False, True),  # back is itself
            (1, 3): (False, False, True),  # back is itself
            # -- 180 degree
            (3, 3): (False, True, False),  # next is same backwards
            (1, 1): (False, True, False),
            (2, 0): (False, True, False),  # back is itself
            (0, 2): (False, True, False),  # back is itself
            (2, 2): (False, False, True),  # next is same backwards
            (0, 0): (False, False, True),
        }

        a: nog.Array = d.array
        max_map_len = max(upper for lower, upper in a.limits()) - 2
        edge_len = max_map_len // 4

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
                        map_y, map_x, next_facing = wrapping[(map_y, map_x, facing)]
                        swap_xy, mirror_y, mirror_x = dir_change_to_coo_change[
                            facing, next_facing]
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
        yield self.test_solve(example, True), 5031, "example"


Day.do_day(day=22, year=2022, part_a=PartA, part_b=PartB)
