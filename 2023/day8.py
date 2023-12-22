# Finally a graph problem!
from math import lcm


def read_line(s: str):
    node = s[:3]
    left = s[7:10]
    right = s[12:15]
    return {node: {"L": left, "R": right}}


def find_z(instructions: str, start, end, desert_map, match=3):
    node = start
    steps = 0
    i = 0
    while node[-match:] != end[-match:]:
        direction = instructions[i]
        node = desert_map[node][direction]
        steps += 1
        i = i + 1 if i < len(instructions) - 1 else 0

    return steps


def solution(fp: str, instructions: str):
    file = open(fp, "r")
    desert_map = {}
    for line in file:
        desert_map.update(read_line(line))

    return find_z(instructions, "AAA", "ZZZ", desert_map)


class Nodes:
    def __init__(self):
        self.length = 0
        self.nodes = []
        self.z = 0

    def add(self, node: str):
        self.nodes.append(node)
        self.length += 1
        if node[-1] == "Z":
            self.z += 1

    def end(self):
        return self.z == self.length


def solution2(fp: str, instructions: str):
    file = open(fp, "r")
    desert_map = {}
    nodes = Nodes()
    # steps = 0
    steps = []
    i = 0

    for line in file:
        entry = read_line(line)
        desert_map.update(entry)
        if list(entry.keys())[0][-1] == "A":
            nodes.add(list(entry.keys())[0])

    for node in nodes.nodes:
        steps.append(find_z(instructions, node, "ZZZ", desert_map, 1))

    results = lcm(*steps)

    return results

    # while not nodes.end():
    #     next_nodes = Nodes()
    #     direction = instructions[i]
    #     for node in nodes.nodes:
    #         next_node = desert_map[node][direction]
    #         next_nodes.add(next_node)
    #     nodes = next_nodes

    #     steps += 1
    #     i = i + 1 if i < len(instructions) - 1 else 0

    # return steps


if __name__ == "__main__":
    BASE_PATH = "/Users/mlamchamkee/dev/advent-of-code/2023/"

    """Unit Tests"""

    example1 = solution(BASE_PATH + "day8example.txt", "LLR")
    print("Example 1: ", example1)
    assert example1 == 6, "Test Example 1"

    instructions = "LLRLRLRRRLRLRRRLRRRLRRLLRLLRRRLRLRRLLRLRLRRLRLRLLRLRRRLRLRRLRRLRRRLRRLRRLRRLLRRLLRRRLRRLRRLRRRLRLRRLRRLLLLRLRRLRLRRLLLRRLRRRLRRRLLRRRLRRRLRRLRRRLLLRRRLLLRRLRRLRRRLRRLRRRLRRLRRRLLRLRLRRRLRRLRLRLRRRLRLRLLLRRRLRRRLRRLRRLRLRRRLRRRLLRRRLRRLRLLLRRLLRRRLRRRLRRRLLRRRLLRRLRLRRRLRRLRRRR"
    solution1 = solution(BASE_PATH + "day8puzzle.txt", instructions)
    print("Solution 1: ", solution1)

    example2 = solution2(BASE_PATH + "day8example2.txt", "LR")
    print("Example 2: ", example2)
    assert example2 == 6, "Test Example 2"

    solution2 = solution2(BASE_PATH + "day8puzzle.txt", instructions)
    print("Solution 2: ", solution2)
