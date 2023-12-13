# Does the game index matter?
# Read in a line and parse into:
# 1) Set of winning numbers
# 2) Start reading the actual numbers and compute the score
def solution():
    total = 0
    # Init var total to 0
    # Iterate over each card
    f = open("/Users/mlamchamkee/dev/advent-of-code/2023/day4puzzle.txt", "r")
    for line in f:
        # Add the score to total
        total += score_card(line)
    # Return total
    return total


# Part two
# Have a dict with game numbers 1, to count the cards
# cards = defaultdict(int)
def solution2():
    cards = {i: 1 for i in range(1, 202)}
    # total_cards
    total_cards = 0
    # iterate through each line index:
    f = open("/Users/mlamchamkee/dev/advent-of-code/2023/day4puzzle.txt", "r")
    grid = [line for line in f]
    for i in range(len(grid)):
        # if line index in dict, score it
        game_i = i + 1
        if game_i in cards:
            score = score_card(grid[i], True)
            # print(f"Game {game_i}: {score}")
            # get new cards
            # iterate from line index + 1 to index + score + 1
            for new_i in range(game_i + 1, game_i + 1 + score):
                # increment value at dict[i] by dict[line index]
                if new_i < 202:
                    cards[new_i] += cards[game_i]
            #         print("GAME: ", game_i)
            # print("CARDS: ", cards)

            # count the cards
            # increment total_cards by dict[line index]
            total_cards += cards[game_i]
    return total_cards


def score_card(line: str, part2=False):
    win_numbers = set()
    MODE = ["index", "winning", "counting"]
    mode_index = 0
    number = ""
    count = -1
    # Iterate over each character
    for char in line:
        # if numeric, add to number
        if char.isnumeric():
            number += char
        else:
            # else
            # if it's a separator, switch mode
            if char in {":", "|"}:
                mode_index += 1
                number = ""
            # if index mode: nothing
            #             if MODE[mode_index] == "index":
            #                 continue
            # if winning mode: add to set of winning numbers
            if MODE[mode_index] == "winning":
                #                 print("NUMBER: ", number)
                if number.isnumeric():
                    win_numbers.add(int(number))
            # if counting: increment count
            if MODE[mode_index] == "counting":
                if number.isnumeric() and int(number) in win_numbers:
                    count += 1
            number = ""

    #     print("Winnning Numbers: ", win_numbers)
    # return 2 power count
    if not part2:
        if count == -1:
            return 0
        return 2**count
    return count + 1


if __name__ == "__main__":
    score_card("Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53")
    score_card("Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83")
    score_card("Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36")
    score_card(
        "Card 197: 38  3 57 72 97 45 66 73 56  8 | 83 68 28 64 58 66 85 15 53 65 23  3 37 87 20 17 47 63 55 69 88 70 62 92 76"
    )
    score_card(
        "Card   1: 58 96 35 20 93 34 10 27 37 30 | 99 70 93 11 63 41 37 29  7 28 34 10 40 96 38 35 27 30 20 21  4 51 58 39 56\n",
        True,
    )
    score_card(
        "Card   2: 64 84 57 46 53 86 90 99 59 70 | 99 59 30 83 84 70 31 57  6 29 18 82 15 88 86 53 51 64 32 47 44 46 80 39 90\n",
        True,
    )
    print("Solution 1: ", solution())
    print("Solution 2: ", solution2())
