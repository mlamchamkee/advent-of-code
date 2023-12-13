# Can this be approached with some math where
# we construct a dict mapping of lower and upper bounds as keys and the value is a differential to be applied
# Example: for the following map
# seed-to-soil map:
# 50 98 2
# We have the mappping for seed
# lower_bound 98 (inclusive)
# upper_bound 100 (exclusive)
# value (a delta) = -48 (40-98)
# For seeds, from 98 to 99 ( 100 - 1), the soil value = seed value - 48

# graph = {"seed": [], "soil": [], "fertilizer": []}


def solution(fp: str):
    graph, seeds = build_graph(fp)

    min_location = float("inf")

    for seed in seeds:
        position = seed
        for key in graph:
            position = map_next(position, key, graph)
        min_location = min(min_location, position)

    return min_location


def build_graph(fp: str):
    graph = {}
    seeds = []
    # read in the input file
    file = open(fp, "r")
    # create graphs which will be a dict of lists
    key = ""
    # iterate over each line in the file
    for line in file:
        if line.startswith("seeds: "):
            seeds = [int(i) for i in line[7:].replace("\n", "").split(" ")]
        # look for a -, that's when we know to reset the key
        end = line.find("-")
        if end > 0:
            key = line[:end]
            graph[key] = []
        # if the line is not empty line
        elif line != "\n" and not line.startswith("seeds: "):
            read_line(key, line, graph)
    return graph, seeds


def read_line(key: str, line: str, graph):
    # split the line
    l = [int(i) for i in line.replace("\n", "").split(" ")]
    # lower is first
    lower = l[1]
    # upper is lower + last element
    upper = l[1] + l[2]
    # delta is second minus first element
    delta = l[0] - l[1]
    # append to graph
    graph[key].append([lower, upper, delta])


def map_next(i: int, key: str, graph) -> int:
    # Iterate over the graph of a specific key
    for v in graph[key]:
        # for each element
        # if that element is between lower and upper
        if v[0] <= i < v[1]:
            # return i + delta
            return i + v[2]
    return i


if __name__ == "__main__":
    seed_graph = {"seed": [[0, 4, 5], [50, 52, 2]]}
    assert map_next(50, "seed", seed_graph) == 52, "Test 1: In range"
    assert map_next(7, "seed", seed_graph) == 7, "Test 2: Outside range"
    print(
        "Example: ",
        solution(
            "/Users/mlamchamkee/dev/advent-of-code/2023/day5example.txt",
        ),
    )
    print(
        "Solution 1: ",
        solution(
            "/Users/mlamchamkee/dev/advent-of-code/2023/day5puzzle.txt",
        ),
    )
    # print("Solution 2: ", solution2())
