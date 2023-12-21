from typing import List, Tuple

# Overall Strategy
# Given a map of seed->soil, soil->fertilizer, ..., humidity->location,
# combined all the maps together and create a map of seed->location
#
# Then, with the range of seeds, find the location of the seeds that are on
# a) the lower bound of the seed range
# b) then step through the lower bound of the coombined ranges above
#    until we reach the end of the seed range

# Constant divisor to make large numbers more readable while debugging
DIV = 1


def combine_entry(
    mapping: Tuple[
        float,
        float,
        float,
        float,
    ],
    targets: List[
        Tuple[
            float,
            float,
            float,
            float,
        ]
    ],
):
    """This function combines one map entry with the following map as a way of mapping
    Given a -> b -> c, the mapping of a -> c is produced
    """
    # Mapping data
    target = mapping[0]
    source = mapping[1]
    rng = mapping[2]
    delta = target - source
    # Base case 1: If the range is 0 or negative
    if rng <= 0:
        return []

    # Base case 2: The target is out of bounds of the next map
    if target < targets[0][1] or target >= targets[-1][1] + targets[-1][2]:
        return [mapping]

    # Find the index of the entry where the target falls in
    i = 0
    while (
        i < len(targets) and not targets[i][1] <= target < targets[i][1] + targets[i][2]
    ):
        i += 1
    # if an entry is found, combine map entries
    if i < len(targets):
        # Combined the portion that is in current entry's range
        # and recursively call combine_entry on portion falling outside of range

        # Mapping data for the current entry
        curr_source = targets[i][1]
        curr_r = targets[i][2]
        curr_delta = targets[i][3]
        sum_delta = delta + curr_delta

        # The increment falling inside the range of the current entry
        inc = min(rng, curr_source + curr_r - target)

        # Combined map entry for the portion inside the range of the current entry
        curr_map = [(source + sum_delta, source, inc, sum_delta)]

        # Inputs for the next recursive call
        next_source = source + inc
        next_input = (next_source + delta, next_source, rng - inc, delta)

        return curr_map + combine_entry(next_input, targets)


def map_locations(
    seeds: List[int],
    map: List[
        Tuple[
            float,
            float,
            float,
            float,
        ]
    ],
):
    """Maps the locations of a list of seed ranges
    Maps the first seed of the range and in increments of the map
    """
    locations = []
    for i in range(0, len(seeds), 2):
        seed = seeds[i]
        interval = seeds[i + 1]
        locations += find_min(seed, interval, map)
    return locations


def find_min(
    seed: int,
    inc: int,
    map: List[
        Tuple[
            float,
            float,
            float,
            float,
        ]
    ],
):
    """Given the range for one seed, map the locations"""
    map.sort(key=lambda x: x[1])
    if inc <= 0:
        return []
    # Edge case: seed is out of bounds of the map
    if seed < map[0][1] or seed >= map[-1][1] + map[-1][2]:
        return [(seed, "position unknown")]

    # Find the index of the entry where the seed falls in
    i = 0
    while i < len(map) and not map[i][1] <= seed < map[i][1] + map[i][2]:
        i += 1
    # If an entry is found, map the location of the seed
    if i < len(map):
        # If the range of seeds given goes beyond the range of the current entry

        # Find the last seed number of current interval
        last_seed = map[i][1] + map[i][2]
        # Set the next seed
        next_seed = min(seed + inc, last_seed)
        curt_int_loc = [
            (seed, seed + map[i][3]),
            # (next_seed - 1, next_seed - 1 + m[i][3]),
        ]
        return curt_int_loc + find_min(last_seed, seed + inc - next_seed, map)


def read_line(key: str, line: str, graph):
    """Reads one line of the text file to parse out the map entry"""
    # split the line
    l = [int(i) for i in line.replace("\n", "").split(" ")]
    target = l[0]
    source = l[1]
    rng = l[2]
    # source + delta = target
    delta = l[0] - l[1]
    # append to graph with divisor applied
    graph[key].append((target / DIV, source / DIV, rng / DIV, delta / DIV))


def fill_blanks(map):
    """Given a map (List of map entries), fill in missing intervals, including starting 0
    Sort the map
    """
    blanks = []
    start = map[0][1]
    if start > 0:
        map.append((0, 0, start, 0))

    for i in range(1, len(map)):
        prior_end = map[i - 1][1] + map[i - 1][2]
        curr_start = map[i][1]
        if curr_start > prior_end:
            blanks.append((prior_end, prior_end, curr_start - prior_end, 0))

    results = map + blanks
    results.sort(key=lambda x: x[1])
    return results


def build_graph(fp: str):
    """Reads the text file and
    1) get the list of seed ranges
    2) builds the list of map entries for each key (seed, soill, water, etc)
    """
    graph = {}
    seeds = []
    # read in the input file
    file = open(fp, "r")
    # create graphs, which will be a dict of lists
    key = ""
    # iterate over each line in the file
    for line in file:
        if line.startswith("seeds: "):
            seeds = [int(i) / DIV for i in line[7:].replace("\n", "").split(" ")]
        # look for a -, that's when we know to reset the key
        end = line.find("-")
        if end > 0:
            key = line[:end]
            graph[key] = []
        # if the line is not empty line
        elif line != "\n" and not line.startswith("seeds: "):
            read_line(key, line, graph)

    # Sorts the entries of the graph and fills blank ranges
    for key in graph:
        graph[key].sort(key=lambda x: x[1])
        graph[key] = fill_blanks(graph[key])
    return graph, seeds


def map_next(i: int, map) -> int:
    """Used for solution 1, where we go iterate through the maps"""

    for entry in map:
        # for each entry of the map
        source = entry[1]
        rng = entry[2]
        delta = entry[3]
        # if that element is within range of the entry
        if source <= i < source + rng:
            # return i + delta
            return i + delta

    # If not found in map, return i
    return i


def build_map_example(fp: str):
    """For debugging only: Generates the full list of seeds and the corresponding location"""
    graph, seeds = build_graph(fp)
    current = range(100)
    for key in graph:
        results = []
        for i in current:
            next = map_next(i, graph[key])
            results.append((i, next))
        current = [result[1] for result in results]
        output = [(x, y[1]) for x, y in zip(range(100), results)]
        print("Results: ", key, output)
    output = [(x, y[1]) for x, y in zip(range(100), results)]
    return output


def solution(fp: str):
    # Parses text file and builds the graph and list of seeds
    graph, seeds = build_graph(fp)
    min_location = float("inf")
    for seed in seeds:
        # Sets position to the seed then go through graphs to map location
        position = seed
        for key in graph:
            position = map_next(position, graph[key])
        # Location is mapped and we compare for minimum
        min_location = min(min_location, position)
    # After all seeds are mapped, return the minimum location
    return min_location


def solution2(fp: str):
    # Parses text file and builds the graph and list of seeds
    graph, seed_ranges = build_graph(fp)

    # Gets the list of elements to map (seed, soil water, etc)
    k = list(graph.keys())

    # Gets the list of seed map entries
    # Initially it will be seed->soil and eventually will be seed->location
    seed_to_location = graph[k[0]]
    # Iterate through remaining map entries and combine with seed map entry
    for i in range(1, len(k), 1):
        map = graph[k[i]]
        combined_seeds = []

        for entry in seed_to_location:
            combined_seeds += combine_entry(entry, map)
        # print(k[i], expanded_seeds)
        seed_to_location = combined_seeds

    seed_to_location.sort(key=lambda x: x[1])

    # Map the locations of the seed ranges and sort
    locations = map_locations(seed_ranges, seed_to_location)
    locations.sort(key=lambda x: x[1])

    # The lowest location is the first element
    return locations[0][1]


if __name__ == "__main__":
    """Unit Tests"""
    # Function: map_next
    graph = {"seed": [(50, 98, 2, 48), (52, 50, 2, 2)]}
    assert map_next(50, graph["seed"]) == 52, "Test 1: In range"
    assert map_next(7, graph["seed"]) == 7, "Test 2: Outside range"

    # Function: fill_blanks
    seed_map = {"seed": [[0, 4, 5], [50, 52, 2]]}
    map0 = [(52, 5, 10, 47), (98, 20, 15, 78), (60, 55, 12, 5)]
    assert fill_blanks(map0) == [
        (0, 0, 5, 0),
        (52, 5, 10, 47),
        (15, 15, 5, 0),
        (98, 20, 15, 78),
        (35, 35, 20, 0),
        (60, 55, 12, 5),
    ], "fill_blanks"

    s = [79, 14, 55, 13]
    map1 = [(46, 50, 2, -4), (7, 52, 30, -45)]
    assert fill_blanks(map1) == [
        (0, 0, 50, 0),
        (46, 50, 2, -4),
        (7, 52, 30, -45),
    ], "fill_blanks: test 2"

    # Function: find_min
    assert find_min(79, 14, map1) == [
        (79, 34),
        (82, "position unknown"),
    ], "find_min, test 1"
    assert find_min(55, 13, map1) == [(55, 10)], "find_min, test 2"

    soil_fert = [(39, 0, 15, 39), (0, 15, 37, -15), (37, 52, 2, -15)]
    fert_water = [(42, 0, 7, 42), (57, 7, 4, 50), (0, 11, 42, -11), (49, 53, 8, -4)]
    water_light = [(0, 0, 18, 0), (88, 18, 7, 70), (18, 25, 70, -7)]
    light_temp = [(0, 0, 45, 0), (81, 45, 19, 36), (68, 64, 13, 4), (45, 77, 23, -32)]

    # Function: combine_entry
    assert combine_entry(
        (52, 50, 48, 2),
        soil_fert,
    ) == [(37, 50, 2, -13), (54, 52, 46, 2)], "map_seeds, test 1"

    # Function: map_locations
    assert map_locations(s, map1) == [
        (79, 34),
        (82, "position unknown"),
        (55, 10),
    ], "map_locations"

    """DEBUGGING
    """
    # print("Example Map: ", build_map_example("day5example.txt"))

    """SOLUTION TO PART 1
    """
    example1 = solution("/Users/mlamchamkee/dev/advent-of-code/2023/day5example.txt")
    print("Example 1: ", example1)
    assert example1 == 35, "Example 1"

    solution1 = solution("/Users/mlamchamkee/dev/advent-of-code/2023/day5puzzle.txt")
    print("Solution 1: ", solution1)
    assert solution1 == 389056265, "Solution 1"

    """SOLUTION TO PART 2
    """
    example2 = solution2("/Users/mlamchamkee/dev/advent-of-code/2023/day5example.txt")
    print("Example 2: ", example2)
    assert example2 == 46, "Example 2"

    solution2 = solution2("/Users/mlamchamkee/dev/advent-of-code/2023/day5puzzle.txt")
    assert solution2 == 137516820, "Solution 2"
    print("Solution 2: ", solution2)
