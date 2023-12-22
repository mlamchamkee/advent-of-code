from collections import defaultdict
from functools import cmp_to_key

WINS = {"5": 6, "41": 5, "32": 4, "311": 3, "221": 2, "2111": 1, "11111": 0}


def read_line(s: str):
    hand = s[:5]
    bid = int(s[6:].replace("\n", "").rstrip())
    return hand, bid


def value(char):
    return "AKQJT98765432".find(char)


def value2(char):
    return "AKQT98765432J".find(char)


def score_hand(hand: str):
    # build a dict of the hand
    score = defaultdict(lambda: 0)
    for card in hand:
        score[card] += 1

    l = sorted(list(score.values()), reverse=True)

    score_str = "".join([str(i) for i in l])

    return WINS[score_str]


def score_hand2(hand: str):
    # Edge case: 5 jokers
    if hand == "JJJJJ":
        return 6
    # build a dict of the hand
    score = defaultdict(lambda: 0)
    jokers = 0
    for card in hand:
        if card != "J":
            score[card] += 1
        else:
            jokers += 1

    l = sorted(list(score.values()), reverse=True)
    l[0] = l[0] + jokers

    score_str = "".join([str(i) for i in l])

    return WINS[score_str]


def compare2(hand1, hand2):
    score_1 = score_hand2(hand1)
    score_2 = score_hand2(hand2)

    if score_1 < score_2:
        return -1
    if score_1 > score_2:
        return 1

    # For when they are equal
    i = 0
    while i < len(hand1) and hand1[i] == hand2[i]:
        i += 1
    if i < len(hand1):
        if value2(hand1[i]) < value2(hand2[i]):
            return 1
        return -1
    return 0


def compare(hand1, hand2):
    score_1 = score_hand(hand1)
    score_2 = score_hand(hand2)

    if score_1 < score_2:
        return -1
    if score_1 > score_2:
        return 1

    # For when they are equal
    i = 0
    while i < len(hand1) and hand1[i] == hand2[i]:
        i += 1
    if i < len(hand1):
        if value(hand1[i]) < value(hand2[i]):
            return 1
        return -1
    return 0


def solution(fp: str, compare_func):
    file = open(fp, "r")
    ranks = []
    games = []
    for line in file:
        hand, bid = read_line(line)
        ranks.append(hand)
        games.append((hand, bid))

    ranks.sort(key=cmp_to_key(compare_func))

    total = 0
    for game in games:
        hand = game[0]
        bid = game[1]
        # find the rank of the rank
        rank = ranks.index(hand) + 1
        total += bid * rank

    return total


if __name__ == "__main__":
    BASE_PATH = "/Users/mlamchamkee/dev/advent-of-code/2023/"
    """Unit Tests"""
    assert read_line("KK677 28 \n") == ("KK677", 28), "Unit test: read_line"

    assert "".join(sorted("KK677", key=value)) == "KK776", "Unit test: value"

    assert score_hand("KKKKK") == 6, "Unit test: score_hand: Five of a kind"
    assert score_hand("KKKK1") == 5, "Unit test: score_hand: "
    assert score_hand("KKK11") == 4, "Unit test: score_hand: Full house"
    assert score_hand("KKK12") == 3, "Unit test: score_hand: "
    assert score_hand("KK677") == 2, "Unit test: score_hand: "
    assert score_hand("KK678") == 1, "Unit test: score_hand: "
    assert score_hand("K2356") == 0, "Unit test: score_hand: "

    assert score_hand2("KKKKJ") == 6, "Unit test: score_hand: Five of a kind"
    assert score_hand2("KKJ77") == 4, "Unit test: score_hand: Five of a kind"

    assert compare("KKK33", "KKK22") == 1, "Unit test: compare: "
    assert compare("KKK22", "KKK33") == -1, "Unit test: compare: "
    assert compare("KKK22", "KKK22") == 0, "Unit test: compare: "

    example1 = solution(BASE_PATH + "day7example.txt", compare)
    print("Example 1: ", example1)
    assert example1 == 6440, "Test Example 1"

    solution1 = solution(BASE_PATH + "day7puzzle.txt", compare)
    print("Solution 1: ", solution1)
    assert solution1 == 251806792, "Test Example 1"

    example2 = solution(BASE_PATH + "day7example.txt", compare2)
    print("Example 2: ", example2)
    assert example2 == 5905, "Test Example 2"

    solution2 = solution(BASE_PATH + "day7puzzle.txt", compare2)
    print("Solution 2: ", solution2)
