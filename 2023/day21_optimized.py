import functools
import sys
from mylib.aoc_frame2 import Day
import nographs as nog


class PartA(Day):
    def compute(self, text, config):
        """ Iterate states the trivial way """
        if config is None:
            config = 64
        print(f"{config=}")

        a = nog.Array(text.splitlines())
        limits = a.limits()
        moves = nog.Position.moves()
        s = a.findall("S")[0]

        positions = {s}
        for i in range(config):
            # Positions reachable from *positions* in one step
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
        yield self.test_solve(example_a1, 6), 16, "example2"


class PartB(PartA):
    def compute(self, text, config):
        """ Iterate states for repeated maps. Find and use loops in behaviour
        of single tiles."""
        if config is None:
            config = 26501365

        a = nog.Array(text.splitlines())
        limits = a.limits()
        size_y, size_x = a.size()
        max_y, max_x = size_y - 1, size_x - 1
        moves = nog.Position.moves()
        s = a.findall("S")[0]

        # Tiles with manual computation: tile -> (step -> state)
        tiles_state = {
            nog.Position((0, 0)): {0: frozenset((s,))},
            nog.Position((-1, 0)): {},
            nog.Position((0, -1)): {},
            nog.Position((0, 1)): {},
            nog.Position((1, 0)): {},
        }

        # Tiles with found loops: tile -> from_i, state_0, state_1
        tiles_loop = dict()

        @functools.cache
        def tile_step(tile_u, tile_l, tile, tile_r, tile_d):
            """ Compute next tile state for tile based on the states of the
             direct neighbor tiles. Use memoization. """
            my_positions = set(tile)

            for pos in tile_u:
                if pos[0] == max_y:
                    my_positions.add(pos - (size_y, 0))
            for pos in tile_l:
                if pos[1] == max_x:
                    my_positions.add(pos - (0, size_x))
            for pos in tile_r:
                if pos[1] == 0:
                    my_positions.add(pos + (0, size_x))
            for pos in tile_d:
                if pos[0] == 0:
                    my_positions.add(pos + (size_y, 0))

            next_positions = set()
            for position in my_positions:
                for move in moves:
                    n_pos = position + move
                    n_pos_y, n_pos_x = n_pos
                    if n_pos.is_in_cuboid(limits):
                        if a[nog.Position((n_pos_y % size_y,
                                           n_pos_x % size_x))] != "#":
                            next_positions.add(n_pos)
            return frozenset(next_positions)

        def get_tile_state(tile, i):
            """ If the tile is already looping, compute its state from there.
            Otherwise, if it is active, get its manual state. Otherwise,
            it has neven been touched to far, and then, remove the empty state. """
            tile_loop = tiles_loop.get(tile, None)
            if tile_loop is not None:
                from_i, state_0, state_1 = tile_loop
                return state_0 if (i - from_i) % 2 == 0 else state_1
            tile_states = tiles_state.get(tile, None)
            if tile_states is not None:
                tile_state = tile_states.get(i, None)
                if tile_state is not None:
                    return tile_state
            return frozenset()

        for i in range(1, config+1):
            # Compute the next state tile by tile
            for tile in list(tiles_state):
                tile_y, tile_x = tile
                new_state = tile_step(
                    get_tile_state((tile_y - 1, tile_x), i - 1),
                    get_tile_state((tile_y, tile_x - 1), i - 1),
                    get_tile_state(tile, i - 1),
                    get_tile_state((tile_y, tile_x + 1), i - 1),
                    get_tile_state((tile_y + 1, tile_x), i - 1),
                )
                if not new_state:
                    # Ignore tiles that are still empty
                    continue

                # Add new state to the states of the tile. Find loops.
                tile_states = tiles_state[tile]
                if (
                        len(tile_states) >= 3 and
                        new_state == tile_states[i-2] and
                        tile_states[i-1] == tile_states[i-3]
                ):
                    # We found a loop. Store it, and stop computing manually.
                    tiles_loop[tile] = (i-3, tile_states[i-3], tile_states[i-2])
                    del tiles_state[tile]
                else:
                    # Save new state
                    tile_states[i] = new_state
                    # It this is the first state of the tile, start computing each
                    # neighbor, if this is untouched so far
                    if i-1 not in tile_states:
                        for neighbor_tile in nog.Position(tile).neighbors(moves):
                            if neighbor_tile not in tiles_state:
                                tiles_state[neighbor_tile] = dict()

            # Derive tile fill data for relevant iterations
            if config == 26501365 and i % 131 == 0 and i // 131 in range(3, 6):
                print("Results for macro step", i // 131, ":")
                print("Loops of looping tiles:")
                for tile, tile_loop in sorted(tiles_loop.items()):
                    from_i, state_0, state_1 = tile_loop
                    print(tile,
                          len(state_0) if (i - from_i) % 2 == 0 else len(state_1)
                          )
                print()
                print("States no (so far) non-looping tiles:")
                for tile in sorted(tiles_state.keys()):
                    states = tiles_state[tile]
                    if i in states:
                        print(tile, len(states[i]))
                print()

                r = sum(len(states[i]) if i in states else 0
                        for tile, states in tiles_state.items())
                for tile, tile_loop in tiles_loop.items():
                    from_i, state_0, state_1 = tile_loop
                    r += len(state_0) if (i - from_i) % 2 == 0 else len(state_1)
                print("Position count:", r)
                print()
                if i // 131 == 5:
                    sys.exit()

        # Add fill counts of active tiles and of already looping tiles
        r = sum(len(states[config]) if config in states else 0
                for tile, states in tiles_state.items())
        for tile, tile_loop in tiles_loop.items():
            from_i, state_0, state_1 = tile_loop
            r += len(state_0) if (config - from_i) % 2 == 0 else len(state_1)

        return r

    """
    Goal: 26_501_365 = 131 * 202300 + 65
    131 = 2 * 65 + 1
    Results:
    - After the last step, the horizontally first + last tile will be
      exactly filled
    - horizontally, 202300 + 1 + 202300 tiles will be build
    """

    def tests(self):
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


"""
Results for macro step 3 :
Loops of looping tiles:
(-1, 0) 7734
(0, -1) 7734
(0, 0) 7719
(0, 1) 7734
(1, 0) 7734

States no (so far) non-looping tiles:
(-3, 0) 2005
(-2, -1) 3948
(-2, 0) 7719
(-2, 1) 3917
(-1, -2) 3948
(-1, -1) 7719
(-1, 1) 7719
(-1, 2) 3917
(0, -3) 2000
(0, -2) 7719
(0, 2) 7719
(0, 3) 1969
(1, -2) 3929
(1, -1) 7719
(1, 1) 7719
(1, 2) 3900
(2, -1) 3929
(2, 0) 7719
(2, 1) 3900
(3, 0) 1987

Position count: 139756

Results for macro step 4 :
Loops of looping tiles:
(-2, 0) 7734
(-1, -1) 7734
(-1, 0) 7719
(-1, 1) 7734
(0, -2) 7734
(0, -1) 7719
(0, 0) 7734
(0, 1) 7719
(0, 2) 7734
(1, -1) 7734
(1, 0) 7719
(1, 1) 7734
(2, 0) 7734

States no (so far) non-looping tiles:
(-4, 0) 2005
(-3, -1) 3948
(-3, 0) 7719
(-3, 1) 3917
(-2, -2) 3948
(-2, -1) 7719
(-2, 1) 7719
(-2, 2) 3917
(-1, -3) 3948
(-1, -2) 7719
(-1, 2) 7719
(-1, 3) 3917
(0, -4) 2000
(0, -3) 7719
(0, 3) 7719
(0, 4) 1969
(1, -3) 3929
(1, -2) 7719
(1, 2) 7719
(1, 3) 3900
(2, -2) 3929
(2, -1) 7719
(2, 1) 7719
(2, 2) 3900
(3, -1) 3929
(3, 0) 7719
(3, 1) 3900
(4, 0) 1987

Position count: 248153

Results for macro step 5 :
Loops of looping tiles:
(-3, 0) 7734
(-2, -1) 7734
(-2, 0) 7719
(-2, 1) 7734
(-1, -2) 7734
(-1, -1) 7719
(-1, 0) 7734
(-1, 1) 7719
(-1, 2) 7734
(0, -3) 7734
(0, -2) 7719
(0, -1) 7734
(0, 0) 7719
(0, 1) 7734
(0, 2) 7719
(0, 3) 7734
(1, -2) 7734
(1, -1) 7719
(1, 0) 7734
(1, 1) 7719
(1, 2) 7734
(2, -1) 7734
(2, 0) 7719
(2, 1) 7734
(3, 0) 7734

States no (so far) non-looping tiles:
(-5, 0) 2005
(-4, -1) 3948
(-4, 0) 7719
(-4, 1) 3917
(-3, -2) 3948
(-3, -1) 7719
(-3, 1) 7719
(-3, 2) 3917
(-2, -3) 3948
(-2, -2) 7719
(-2, 2) 7719
(-2, 3) 3917
(-1, -4) 3948
(-1, -3) 7719
(-1, 3) 7719
(-1, 4) 3917
(0, -5) 2000
(0, -4) 7719
(0, 4) 7719
(0, 5) 1969
(1, -4) 3929
(1, -3) 7719
(1, 3) 7719
(1, 4) 3900
(2, -3) 3929
(2, -2) 7719
(2, 2) 7719
(2, 3) 3900
(3, -2) 3929
(3, -1) 7719
(3, 1) 7719
(3, 2) 3900
(4, -1) 3929
(4, 0) 7719
(4, 1) 3900
(5, 0) 1987

Position count: 387456
"""