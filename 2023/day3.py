# Could this be a graph problem?

SYMBOLS = {
    "`",
    "~",
    "!",
    "@",
    "#",
    "$",
    "%",
    "^",
    "&",
    "*",
    "(",
    ")",
    "_",
    "-",
    "+",
    "=",
    "{",
    "[",
    "}",
    "}",
    "|",
    '"',
    "<",
    ",",
    ">",
    "?",
    "/",
}


def solution():
    # store a set of visited nodes
    v = set()
    # store a total
    total = 0

    # Read in text file
    f = open("/Users/mlamchamkee/dev/advent-of-code/2023/day3puzzle.txt", "r")
    grid = [line for line in f]
    grid
    # Iterate over each node and if a symbol
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            char = grid[r][c]
            if char in SYMBOLS:
                # Going clockwise from 12 o'clock
                total += traverse(grid, r - 1, c, v)
                total += traverse(grid, r - 1, c + 1, v)
                total += traverse(grid, r, c + 1, v)
                total += traverse(grid, r + 1, c + 1, v)
                total += traverse(grid, r + 1, c, v)
                total += traverse(grid, r + 1, c - 1, v)
                total += traverse(grid, r, c - 1, v)
                total += traverse(grid, r - 1, c - 1, v)
    return total


def solution2():
    # store a set of visited nodes
    v = set()
    # store a total
    total = 0

    DIRECTIONS = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
    # Read in text file
    f = open("/Users/mlamchamkee/dev/advent-of-code/2023/day3puzzle.txt", "r")
    grid = [line for line in f]

    # Iterate over each node and if a symbol
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            char = grid[r][c]
            if char == "*":
                gears = []
                # Going clockwise from 12 o'clock
                for d in DIRECTIONS:
                    result = traverse(grid, r + d[0], c + d[1], v)
                    if result != 0:
                        gears.append(result)
                #             print("GEARS: ", gears)
                if len(gears) == 2:
                    total += gears[0] * gears[1]

    return total


# construct number takes a row and col
# if node is not visited
# move left and right
# while it's a number prepend or append
def parse_number(line: str, r: int, c: int, visited=set()):
    number = ""
    #     if not line[c].isnumeric():
    #         return 0
    #     else:
    #     print("LINE: ", line)
    #     print("R: ", r)
    #     print("C: ", c)
    if (r, c) not in visited:
        number += line[c]
        visited.add((r, c))
    i = c - 1
    j = c + 1
    while line[i].isnumeric():
        if (r, i) not in visited:
            number = line[i] + number
            visited.add((r, i))
        i -= 1

    while line[j].isnumeric():
        if (r, j) not in visited:
            number += line[j]
            visited.add((r, j))
        j += 1
    #     print("NUMBER: ", number)
    if number == "":
        return 0
    return int(number)


# traversal function, takes in the current total, the set of visited nodes
# if out of bounds return 0
# if a number is found construct a number
# add result to total
def traverse(grid, r: int, c: int, visited=set()):
    if r < 0 or r > len(grid) or c < 0 or c > len(grid[r]):
        return 0
    if not grid[r][c].isnumeric():
        return 0
    else:
        return parse_number(grid[r], r, c, visited)


if __name__ == "__main__":
    assert (parse_number("467..114..", 1, 1) == 567, "Test 1")
    print("Solution 1: ", solution())
    print("Solution 2: ", solution2())
