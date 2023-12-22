from mylib.aoc_frame2 import Day
import nographs as nog


def parse(text: str):
    """ Describe the bricks as (start_pos, end_pos, delta_step). delta can be used to
    come from start_pos to end_pos. start_pos < end_pos. brick[i] < brick[i+1]. """
    bricks = []
    for brick_str in text.splitlines():
        brick_from_str, brick_to_str = brick_str.split("~")
        brick_from = nog.Position(list(reversed(
            [int(c) for c in brick_from_str.split(",")])))
        brick_to = nog.Position(list(reversed(
            [int(c) for c in brick_to_str.split(",")])))
        brick_ends = sorted([brick_from, brick_to])
        brick_extend = brick_ends[1] - brick_ends[0]
        brick_delta = nog.Position(
            [1 if coord > 0 else (-1 if coord < 0 else 0)
             for coord in brick_extend])
        brick_ends.append(brick_delta)
        bricks.append(brick_ends)
    return sorted(bricks)


def iterate_brick(brick):
    """ Iterate the positions occupied by the brick """
    brick_from, brick_to, brick_delta = brick
    while True:
        yield brick_from
        if brick_from == brick_to:
            return
        brick_from += brick_delta


def compute_supported(brick, other_bricks):
    """ Index of bricks from other_bricks that support brick. Other_bricks
    need to be a prefix of all bricks, i.e., next(other_bricks) needs to be brick 0.
    """
    supported = set()
    brick_fallen = set(pos - (1, 0, 0) for pos in iterate_brick(brick))
    for i_other, other in enumerate(other_bricks):
        other_volume = set(iterate_brick(other))
        if not brick_fallen.isdisjoint(other_volume):
            supported.add(i_other)
    return supported


def do_stacking(bricks):
    """ Make each brick fall as far as possible. Then, for each brick, compute
    the bricks that support it in its final position. Bricks need to fulfil the
    guarantees as described for *parse*. """
    upper_limits = dict()
    for brick in bricks:
        for pos in iterate_brick(brick):
            pos_z, pos_y, pos_x = pos
            stack = nog.Position((pos_y, pos_x))
            upper_limits[stack] = 0

    supporter = dict()
    for i, brick in enumerate(bricks):
        if brick[0][0] == 1:
            supporter[i] = {-1}  # ground
        else:
            # How far can each element of brick fall? What is the minimum of all?
            falling = 9999999
            for pos in iterate_brick(brick):
                pos_z, pos_y, pos_x = pos
                stack = nog.Position((pos_y, pos_x))
                stack_z = upper_limits[stack]
                falling_pos = pos_z - stack_z - 1
                if falling_pos < falling:
                    falling = falling_pos
            # Brick falls that far
            brick[0] -= (falling, 0, 0)
            brick[1] -= (falling, 0, 0)

            # Compute bricks that support the brick in ins new position
            if brick[0][0] == 1:
                supporter[i] = {-1}  # ground
            else:
                supporter[i] = compute_supported(brick, bricks[:i])

        # Update the support height for each (y, x) stack
        for pos in iterate_brick(brick):
            pos_z, pos_y, pos_x = pos
            stack = nog.Position((pos_y, pos_x))
            if upper_limits[stack] < pos_z:
                upper_limits[stack] = pos_z
    return supporter


class PartA(Day):
    def compute(self, text, config):
        bricks = parse(text)
        supporter = do_stacking(bricks)

        # Brick is important, if there is another brick that is only supported by brick
        important_bricks = set()
        for supported, supported_by in supporter.items():
            if len(supported_by) == 1:
                important_bricks.add(next(iter(supported_by)))
        important_bricks.remove(-1)

        return len(bricks) - len(important_bricks)

    def tests(self):
        yield self.test_solve(example_a1, None), 5, "example"


class PartB(PartA):
    def compute(self, text, config):
        bricks = parse(text)
        supporter = do_stacking(bricks)

        total_fallen = 0
        for brick_i, brick in enumerate(bricks):
            # Starting with the ground as the only "supported brick", extend them
            # successively by bricks supported by already supported bricks.
            all_supported = {-1}
            prev_all_supported = set()
            while len(prev_all_supported) < len(all_supported):
                prev_all_supported = set(all_supported)
                for supported_i, supported_by in supporter.items():
                    if supported_i == brick_i:
                        continue
                    if supported_i in all_supported:
                        continue
                    if not supported_by.isdisjoint(all_supported):
                        all_supported.add(supported_i)
            # (All bricks minus the one we remove)
            # - (number of supported bricks minus the ground)
            others_fallen = (len(bricks) - 1) - (len(all_supported) - 1)

            total_fallen += others_fallen
        return total_fallen

    def tests(self):
        yield self.test_solve(example_a1, None), 7, "example"


example_a1 = '''
1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9
'''
Day.do_day(day=22, year=2023, part_a=PartA, part_b=PartB)
