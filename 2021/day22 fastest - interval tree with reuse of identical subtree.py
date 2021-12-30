import functools
import re
import sys
from mylib.aoc_frame import Day


# 0 represents the empty cell set, 1 represents one cell with content 1.
# Other cell sets are described as a sorted tuple of intervals in the first coordinate,
# and their cell sets in all the following coordinates. An interval and its sub cells form
# a cell slice with identical geometry along the interval. Cell sets can have different
# dimensions.

# A cell set is represented (in the sense of an id) by the address of the data structure that
# described it when it first occurred during the computation. If the same set occurs again
# later on, this is recognized and the existing id (address) is reused.

def do(d, with_limit):
    id_empty = id(0)  # describes empty world (of any dimension)
    id_full = id(1)  # describes one cell (slice of dimension 0)

    geometry_to_id = {0: id_empty, 1: id_full}
    id_to_geometry = {id_empty: 0, id_full: 1}

    @functools.lru_cache(maxsize=32)
    def set_cells_in_cube(cell_slices_id, cube, value_id):
        """ In a n-dimensional matrix of cells, manage a (very large) subset that stems from
        a sequence of operations of adding or removing cubes of cells. set_cells_in_cube add
        the cells defined by cube (specified by n intervals of integer) if value is
        id_full or remove them if value is id_empty.
        To make cache faster, cell slices are identified with a unique id, and this id is used
        as parameter here.
        """
        if len(cube) == 0:
            # no dimension with cube interval left, we are at the "deepest" dimension
            return value_id  # accordingly to value, return full/empty world (i.e.: one cell)

        (cube_from, cube_to), cube_intervals = cube[0], cube[1:]  # get interval of first dimension

        if cell_slices_id == id_empty:
            # Replace zero value by infinite interval with zero value.
            # Interval boundaries must stay within some limits. This allows for representing the
            # infinite interval by these limits. Here, we use the minimal and maximal values that
            # can be represented by a word value in the given architecture. But you can choose
            # arbitrary limits.
            cell_slices = ((-sys.maxsize-1, sys.maxsize, id_empty),)
        else:
            cell_slices = id_to_geometry[cell_slices_id]  # tuple of ((from, to), content)

        new_cell_slices = []
        # Keep slices with an interval that start before cube starts, but limit to part before cube
        new_cell_slices.extend([(i_from, min(i_to, cube_from), i_content)
                                for (i_from, i_to, i_content) in cell_slices
                                if i_from < cube_from]
                               )
        # For slices with intervals overlapping the cube interval, take the overlapping part,
        # and for this, set the required value in the sub dimensions
        new_cell_slices.extend([(max(i_from, cube_from), min(i_to, cube_to),
                                 set_cells_in_cube(i_content, cube_intervals, value_id))
                                for (i_from, i_to, i_content) in cell_slices
                                if not (i_to <= cube_from or cube_to <= i_from)]
                               )
        # Keep slices with intervals then end after the cube ends, but limit to part after cube
        new_cell_slices.extend([(max(i_from, cube_to), i_to, i_content)
                                for (i_from, i_to, i_content) in cell_slices
                                if cube_to < i_to]
                               )
        # Optimization: Merge neighbor slides if they have the same geometry
        new_cell_slices_merged = []
        for slice in new_cell_slices:
            i_from, i_to, i_content = slice
            if len(new_cell_slices_merged) == 0:
                new_cell_slices_merged.append(slice)
            else:
                prev_i_from, prev_i_to, prev_i_content = new_cell_slices_merged[-1]
                if i_content != prev_i_content:
                    new_cell_slices_merged.append(slice)
                else:
                    prev_i_to = i_to
                    new_cell_slices_merged[-1] = (prev_i_from, prev_i_to, prev_i_content)
        result = tuple(new_cell_slices_merged)
        # Optimization: Return id of resulting geometry instead of the geometry itself
        if result in geometry_to_id:
            geometry_id = geometry_to_id[result]
        else:
            geometry_id = id(result)
            geometry_to_id[result] = geometry_id
            id_to_geometry[geometry_id] = result
        return geometry_id

    @functools.cache
    def cubes_count(cell_slices_id):
        if cell_slices_id is id_full:  # Can only occur in lowest dimension
            return 1  # So, it describes just one filled cell
        if cell_slices_id is id_empty:  # empty world
            return 0  # contains no filled cells, no matter how deep following dimensions go
        # Slice cube count multiplied with slice "thickness"
        return sum(cubes_count(sub_cubes_id) * (i_to - i_from)
                   for i_from, i_to, sub_cubes_id in id_to_geometry[cell_slices_id])

    # Execute cube commands
    cubes_id = id_empty
    for cmd, (xf, xt, yf, yt, zf, zt) in d.int_lines:
        if with_limit and (xf < -50 or yf < -50 or zf < -50 or xt > 50 or yt > 50 or zt > 50):
            continue
        # print(cmd, (xf, xt, yf, yt, zf, zt))
        cubes_id = set_cells_in_cube(cubes_id, ((xf, xt+1), (yf, yt+1), (zf, zt+1)),
                                     id_full if cmd == "on " else id_empty)
    return cubes_count(cubes_id)


class PartA(Day):
    def parse(self, text, d):  # store puzzle parsing result data into attributes of d
        lines = text.splitlines()
        d.int_lines = [(line[0:3],
                        tuple(int(n) for n in re.findall(r"[0-9-]+", line))) for line in lines]

    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        return do(d, True)


class PartB(PartA):
    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        return do(d, False)


Day.do_day(day=22, year=2021, part_a=PartA, part_b=PartB)
