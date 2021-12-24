from mylib.aoc_frame import Day
import mylib.no_graph_lib as nog


class PartA(Day):
    def parse(self, text, d):  # store puzzle parsing result data into attributes of d
        d.area = text.splitlines()
        d.group_size = 2
        d.energy_for_pod = (1, 1, 10, 10, 100, 100, 1000, 1000)
        d.pods = 8

    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        # start_state: positions of the pods sorted by ascending pod name
        start_pos = []
        for y in range(len(d.area)):
            for x in range(13):
                if x >= len(d.area[y]):
                    continue
                c = d.area[y][x]
                if "A" <= c <= "Z":
                    start_pos.append((ord(c) - ord("A"), (y, x)))
        start_state = tuple(pos for pod, pos in sorted(start_pos))
        # print(start_state)

        def walk_fields(hall, room):
            """ Enumerate fields on way from position in hall to position in room """
            hy, hx = hall
            ry, rx = room
            for x in range(hx, rx, 1 if hx < rx else -1):
                yield (hy, x)
            for y in range(hy, ry + 1):
                yield (y, rx)

        def walk(from_pos, to_pos, pod_positions):
            """ Check if way is free or occupied by some other pod """
            # print("walk", from_pos, to_pos, pod_positions)
            # Calculate fields from from_pos to to_pos (leave out from_pos)
            if from_pos[0] == 1:  # y == 1 means hall
                fields = tuple(walk_fields(from_pos, to_pos))[1:]
            else:
                fields = tuple(walk_fields(to_pos, from_pos))[:-1]
            return len(fields) if len(set(fields).intersection(pod_positions)) == 0 else 0

        def next_edge(positions, _):
            """ How can the situation go on? """
            # From hall to room
            for room in range(4):
                room_x = 3 + 2 * room
                # If all pods are not in room or are room mates:
                if all(x != room_x or y < 2 or pod // d.group_size == room
                       for pod, (y, x) in zip(range(d.pods), positions)):
                    first_in_group = room * d.group_size
                    for pod in range(first_in_group, first_in_group + d.group_size):
                        y, x = positions[pod]
                        if y == 1:  # from hall to my room
                            for destination_room_y in range(d.group_size+1, 1, -1):
                                destination_room_pos = destination_room_y, room_x
                                distance = walk((y, x), destination_room_pos, positions)
                                if distance > 0:  # the way is free
                                    new_pos = list(positions)
                                    new_pos[pod] = destination_room_pos
                                    energy = distance * d.energy_for_pod[pod]
                                    # print("move", pod, "from", (y, x), "to",
                                    #       destination_room_pos, "energy", energy)
                                    yield tuple(new_pos), energy
                                    # If we can enter our room deeply, do not try entering less deep
                                    # If we can go to a final position with a pod, only do that
                                    return
            for pod, (y, x) in zip(range(d.pods), positions):
                # print("test pod", pod, "at", (y, x))
                if y >= 2:  # from room to hall
                    if x == 3 + 2 * (pod // d.group_size):  # I am in my room
                        if y == len(d.area) - 2:  # lowest y coordinate
                            continue  # Never leave optimal place
                        if not any(xo == x and yo > y and 3 + 2 * (other // d.group_size) != xo
                                   for other, (yo, xo) in zip(range(d.pods), positions)):
                            continue  # I block nobody: Do not leave room position
                    for destination_hall_x in (1, 2, 4, 6, 8, 10, 11):  # hall stop positions
                        hall_pos = (1, destination_hall_x)
                        distance = walk((y, x), hall_pos, positions)
                        if distance > 0:  # the way is free
                            new_pos = list(positions)
                            new_pos[pod] = hall_pos
                            energy = distance * d.energy_for_pod[pod]
                            # print("move", pod, "from", (y, x), "to", hall_pos, "energy", energy)
                            yield tuple(new_pos), energy

        def state_to_id(positions):
            """ Within each roommate pairs, sort (avoid search effort for "symmetric" states) """
            new_positions = []
            for i in range(0, 4 * d.group_size, d.group_size):
                new_positions.extend(sorted(positions[i:i + d.group_size]))
            return tuple(new_positions)

        traversal = nog.TraversalShortestPaths(next_edges=next_edge, vertex_to_id=state_to_id)
        for positions in traversal.start_from(tuple(start_state), build_paths=True).go():
            # print(positions)
            for pod, (y, x) in zip(range(d.pods), positions):
                if y < 2 or x != 3 + 2 * (pod // d.group_size):  # pod in hall or in wrong room
                    break
            else:
                return traversal.distance
        return "No result"


class PartB(PartA):
    def parse(self, text, d):  # store puzzle parsing result data into attributes of d
        d.area = text.splitlines()
        d.area = d.area[:3] + ["  #D#C#B#A#", "  #D#B#A#C#"] + d.area[-2:]
        d.group_size = 4
        d.energy_for_pod = (1, 1, 1, 1, 10, 10, 10, 10, 100, 100, 100, 100, 1000, 1000, 1000, 1000)
        d.pods = 16


Day.do_day(day=23, year=2021, part_a=PartA, part_b=PartB)
