from collections import defaultdict
from mylib.aoc_frame2 import Day
import nographs as nog


class PartA(Day):
    def compute(self, text, config):
        if config is None:
            config = 64
        print(f"{config=}")

        a = nog.Array(text.splitlines())
        limits = a.limits()
        moves = nog.Position.moves()
        s = a.findall("S")[0]

        positions = {s}
        for i in range(config):
            next_positions = set()
            for position in positions:
                for move in moves:
                    n_pos = position + move
                    if a[n_pos] != "#":
                        if n_pos.is_in_cuboid(limits):
                            next_positions.add(n_pos)
            positions = next_positions
        return len(positions)

    def tests(self):
        yield self.test_solve(example_a1, 6), 16, "example"


class PartB(PartA):
    def compute(self, text, config):
        if config is None:
            config = 26501365
        print(f"{config=}")

        a = nog.Array(text.splitlines())
        size_y, size_x = a.size()
        moves = nog.Position.moves()
        s = a.findall("S")[0]

        # Precompute moves for non-rock positions in a single tile
        moves_at_position = defaultdict(list)
        for position in a.findall(".S"):
            for move in moves:
                n_pos = position + move
                n_pos_y, n_pos_x = n_pos
                n_pos_wrapped = nog.Position((n_pos_y % size_y, n_pos_x % size_x))
                if a[n_pos_wrapped] != "#":
                    moves_at_position[position].append(move)

        positions = {s}
        for i in range(config):
            # Positions reachable from *positions* in one step
            new_positions = set()
            for position in positions:
                pos_y, pos_x = position
                pos_wrapped = nog.Position((pos_y % size_y, pos_x % size_x))
                for move in moves_at_position[pos_wrapped]:
                    new_positions.add(position + move)
            positions = new_positions

            if config == 26501365 and i % 131 == 0 and i // 131 in range(3, 6):
                print("Positions:", len(positions))
                print("Position by tile:")
                positions_per_tile = defaultdict(int)
                for pos in positions:
                    pos_y, pos_x = pos
                    tile = (pos_y // size_y, pos_x // size_x)
                    positions_per_tile[tile] += 1

                for tile in sorted(positions_per_tile):
                    print(tile, ":", positions_per_tile[tile])
                print()
                if i // 131 == 5:
                    return None

        return len(positions)

    def tests(self):
        return []  # tests temporarily switched off
        yield self.test_solve(example_a1, 6), 16, "example with 6"
        yield self.test_solve(example_a1, 10), 50, "example with 10"
        yield self.test_solve(example_a1, 50), 1594, "example with 50"
        yield self.test_solve(example_a1, 100), 6536, "example with 100"
        yield self.test_solve(example_a1, 1000), 668697, "example with 1000"
        yield self.test_solve(example_a1, 5000), 16733044, "example with 5000"


example_a1 = '''
...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
'''
Day.do_day(day=21, year=2023, part_a=PartA, part_b=PartB)

# ------ Output for part 2 for n*131+65 steps, with n in (3, 4, 5) ----------
"""
Positions: 140476
Position by tile:
(-3, -1) : 1
(-3, 0) : 2056
(-3, 1) : 1
(-2, -2) : 1
(-2, -1) : 3984
(-2, 0) : 7734
(-2, 1) : 3990
(-2, 2) : 1
(-1, -3) : 1
(-1, -2) : 3984
(-1, -1) : 7734
(-1, 0) : 7719
(-1, 1) : 7734
(-1, 2) : 3990
(-1, 3) : 1
(0, -3) : 2039
(0, -2) : 7734
(0, -1) : 7719
(0, 0) : 7734
(0, 1) : 7719
(0, 2) : 7734
(0, 3) : 2055
(1, -3) : 1
(1, -2) : 3955
(1, -1) : 7734
(1, 0) : 7719
(1, 1) : 7734
(1, 2) : 3970
(1, 3) : 1
(2, -2) : 1
(2, -1) : 3955
(2, 0) : 7734
(2, 1) : 3970
(2, 2) : 1
(3, -1) : 1
(3, 0) : 2034
(3, 1) : 1

Positions: 249112
Position by tile:
(-4, -1) : 1
(-4, 0) : 2056
(-4, 1) : 1
(-3, -2) : 1
(-3, -1) : 3984
(-3, 0) : 7734
(-3, 1) : 3990
(-3, 2) : 1
(-2, -3) : 1
(-2, -2) : 3984
(-2, -1) : 7734
(-2, 0) : 7719
(-2, 1) : 7734
(-2, 2) : 3990
(-2, 3) : 1
(-1, -4) : 1
(-1, -3) : 3984
(-1, -2) : 7734
(-1, -1) : 7719
(-1, 0) : 7734
(-1, 1) : 7719
(-1, 2) : 7734
(-1, 3) : 3990
(-1, 4) : 1
(0, -4) : 2039
(0, -3) : 7734
(0, -2) : 7719
(0, -1) : 7734
(0, 0) : 7719
(0, 1) : 7734
(0, 2) : 7719
(0, 3) : 7734
(0, 4) : 2055
(1, -4) : 1
(1, -3) : 3955
(1, -2) : 7734
(1, -1) : 7719
(1, 0) : 7734
(1, 1) : 7719
(1, 2) : 7734
(1, 3) : 3970
(1, 4) : 1
(2, -3) : 1
(2, -2) : 3955
(2, -1) : 7734
(2, 0) : 7719
(2, 1) : 7734
(2, 2) : 3970
(2, 3) : 1
(3, -2) : 1
(3, -1) : 3955
(3, 0) : 7734
(3, 1) : 3970
(3, 2) : 1
(4, -1) : 1
(4, 0) : 2034
(4, 1) : 1

Positions: 388654
Position by tile:
(-5, -1) : 1
(-5, 0) : 2056
(-5, 1) : 1
(-4, -2) : 1
(-4, -1) : 3984
(-4, 0) : 7734
(-4, 1) : 3990
(-4, 2) : 1
(-3, -3) : 1
(-3, -2) : 3984
(-3, -1) : 7734
(-3, 0) : 7719
(-3, 1) : 7734
(-3, 2) : 3990
(-3, 3) : 1
(-2, -4) : 1
(-2, -3) : 3984
(-2, -2) : 7734
(-2, -1) : 7719
(-2, 0) : 7734
(-2, 1) : 7719
(-2, 2) : 7734
(-2, 3) : 3990
(-2, 4) : 1
(-1, -5) : 1
(-1, -4) : 3984
(-1, -3) : 7734
(-1, -2) : 7719
(-1, -1) : 7734
(-1, 0) : 7719
(-1, 1) : 7734
(-1, 2) : 7719
(-1, 3) : 7734
(-1, 4) : 3990
(-1, 5) : 1
(0, -5) : 2039
(0, -4) : 7734
(0, -3) : 7719
(0, -2) : 7734
(0, -1) : 7719
(0, 0) : 7734
(0, 1) : 7719
(0, 2) : 7734
(0, 3) : 7719
(0, 4) : 7734
(0, 5) : 2055
(1, -5) : 1
(1, -4) : 3955
(1, -3) : 7734
(1, -2) : 7719
(1, -1) : 7734
(1, 0) : 7719
(1, 1) : 7734
(1, 2) : 7719
(1, 3) : 7734
(1, 4) : 3970
(1, 5) : 1
(2, -4) : 1
(2, -3) : 3955
(2, -2) : 7734
(2, -1) : 7719
(2, 0) : 7734
(2, 1) : 7719
(2, 2) : 7734
(2, 3) : 3970
(2, 4) : 1
(3, -3) : 1
(3, -2) : 3955
(3, -1) : 7734
(3, 0) : 7719
(3, 1) : 7734
(3, 2) : 3970
(3, 3) : 1
(4, -2) : 1
(4, -1) : 3955
(4, 0) : 7734
(4, 1) : 3970
(4, 2) : 1
(5, -1) : 1
(5, 0) : 2034
(5, 1) : 1
"""