import itertools
from mylib.aoc_frame2 import Day
import nographs as nog


class PartA(Day):
    def parse(self, text: str):
        for line in text.splitlines():
            d_str, l_str, c_str = line.split()
            yield nog.Position(v_of_c[d_str]), int(l_str)

    def compute(self, text, config):
        # Prepare a vertical sweep through the line from top to bottom, where
        # in each line, horizontal start and stop signals start/stop horizontal
        # filling.
        # From start and end points of vertical segments, compute the introduction /
        # removing of the horizontal start / stop signals in this line, with effect
        # on the line and subsequent lines (without new introductions / removing
        # of signals.
        changes = []  # of: (position, add/del of a signal, on/off signal type
        pos = nog.Position((0, 0))
        smallest_y = float("inf")
        direction_for_smallest_y = None
        data = list(self.parse(text))  # store in list, for look ahead and look back
        for i, dir_and_len in enumerate(data):
            d, l = dir_and_len
            dy, dx = d  # step direction of trench segment

            start = pos  # save pos as start point of the trench segment
            pos += d * l  # end-pos of trench segment

            if dy == 0:
                # Use horizontal trench segments to determine global trench orientation
                if start[0] < smallest_y:
                    direction_for_smallest_y = dx
                    smallest_y = start[0]
                continue

            prev_dx = data[(i-1) % len(data)][0][1]
            next_dx = data[(i+1) % len(data)][0][1]
            if dy < 0:
                # U, upper end, to R: start at pos (in y, pos is leftmost point)
                if next_dx == 1:
                    changes.append((pos, "add", "on"))
                # U, upper end, to L: start 1 lower (in y, left is more)
                else:
                    changes.append((pos + (1, 0), "add", "on"))
                # U, lower end, from L: stop here (in y, left is already more)
                if prev_dx == 1:
                    changes.append((start, "del", "on"))
                # U, lower end, from R: stop 1 lower (iny, pos is still leftmost point)
                else:
                    changes.append((start + (1, 0), "del", "on"))
            else:
                # D, upper end, from L: stop here (because start is rightmost point)
                if prev_dx == 1:
                    changes.append((start, "add", "off"))
                # D, upper end, from R: delay off by 1 y (because right is more...)
                else:
                    changes.append((start + (1, 0), "add", "off"))
                # D, lower end, to R: stop here (because right is already more...)
                if next_dx == 1:
                    changes.append((pos, "del", "off"))
                # D, lower end, to L: delay end of off by 1 y (pos is rightmost point)
                else:
                    changes.append((pos + (1, 0), "del", "off"))

        # Check, that trench sequence is really clockwise, as we assume
        assert direction_for_smallest_y == 1

        # Sweep from top to bottom. Keep and update horizontal active start/stop
        # signals from line to line. Jump over line blocks that have no signal changes
        # and re-use results from the previous line having a signal change.
        on = 0  # number of filled fields
        active_set = set()  # horizontal start/stop signals in the current line
        prev_y = None  # Start (top y coord.) of line block that we currently jump over
        on_in_line = 0  # Number of filled fields in the line before the jump
        changes.sort()  # Sort changes from top to bottom, and from left to right
        for y, changes in itertools.groupby(changes, lambda change: change[0][0]):
            if prev_y is not None:
                # end of a jump: duplicate prev. result by number of lines jumped over
                on += on_in_line * (y - prev_y)
            # store line in case we start a jump here
            prev_y = y
            # Update active set (horizontal on/off signals) by current signal changes
            for change in changes:
                (y, x), op, kind = change
                if op == "del":
                    active_set.remove((x, kind))
                else:
                    active_set.add((x, kind))
            # In current line, sweep on/off signals from left to right. Count
            # "on fields". Jump over columns without signals, repeating the
            # previous on/off state.
            prev_x = None
            on_in_line = 0
            for x, kind in sorted(active_set):
                if kind == "off":
                    on_in_line += x - prev_x + 1
                prev_x = x
        return on

    def tests(self):
        yield self.test_solve(example_a1, "config"), 62, "example1_1"


class PartB(PartA):
    def parse(self, text: str):
        for line in text.splitlines():
            d_str, l_str, c_str = line.split()
            c = c_str[2:-1]
            len_hex = c[:5]
            dir_hex = c[5]
            yield nog.Position(v_of_c["RDLU"[int(dir_hex)]]), int(len_hex, 16)

    def tests(self):
        yield self.test_solve(example_a1, "config"), 952408144115, "example2"


v_of_c = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}
example_a1 = '''
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3) 
'''
Day.do_day(day=18, year=2023, part_a=PartA, part_b=PartB)
