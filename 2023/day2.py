import string

ALPHA_SET = set(string.ascii_letters)

MAX = {"red": 12, "blue": 14, "green": 13}


def solution():
    # store a total sum
    total = 0
    file = open("/Users/mlamchamkee/dev/advent-of-code/2023/day2puzzle.txt", "r")
    # traverse each line
    for line in file:
        total += read_line(line)
    return total


def solution2():
    # store a total sum
    total = 0
    file = open("/Users/mlamchamkee/dev/advent-of-code/2023/day2puzzle.txt", "r")
    # traverse each line
    for line in file:
        start = line.find(":")
        total += max_colors(line[start:])
    return total


def read_line(s: str) -> int:
    game_index = ""
    game_result = False
    # iterate over each index
    for i in range(len(s)):
        # if its numeric add to game_index
        char = s[i]
        if char.isnumeric():
            game_index += char
        # if colon incoke is_feasible on the rest of the string
        if char == ":":
            games = s[i:].split(";")
            for game in games:
                game_result = is_feasible(game)
                # if True add to total
                if not game_result:
                    return 0
            break

    return int(game_index)


def check_game(colors):
    for color in colors:
        if MAX[color] < colors[color]:
            return False
    return True


def is_feasible(s: str):
    colors = {"red": 0, "blue": 0, "green": 0}

    count = ""
    color = ""
    for char in s:
        if char.isnumeric():
            count += char
        if char in ALPHA_SET:
            color += char
        if color in colors:
            colors[color] = int(count)
            color = ""
            count = ""
    return check_game(colors)


def max_colors(s: str):
    colors = {"red": 0, "blue": 0, "green": 0}

    count = ""
    color = ""
    for char in s:
        if char.isnumeric():
            count += char
        if char in ALPHA_SET:
            color += char
        if color in colors:
            colors[color] = max(int(count), colors[color])
            color = ""
            count = ""
    return colors["red"] * colors["blue"] * colors["green"]


if __name__ == "__main__":
    assert (
        read_line("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green") == 1
    ), "Game 1"
    assert (
        read_line("Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue")
        == 2
    ), "Game 2"
    assert (
        read_line(
            "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red"
        )
        == 0
    ), "Game 3"
    assert (
        read_line(
            "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red"
        )
        == 0
    ), "Game 4"
    assert (
        read_line("Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green") == 5
    ), "Game 5"

    print("Solution 1: ", solution())
    print("Solution 2: ", solution2())
