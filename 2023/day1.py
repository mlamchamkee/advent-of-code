# High level: Two pointer approach to iterate from left and right


def solution(read_func) -> int:
    # store a total sum
    total = 0
    file = open("/Users/mlamchamkee/dev/advent-of-code/2023/day1puzzle.txt", "r")
    # traverse each line
    for line in file:
        total += read_func(line)
    return total


def read_line(s: str) -> int:
    first = ""
    second = ""

    # iterate over each character
    for char in s:
        # if number store value
        if char.isnumeric():
            if first == "":
                first = char
            # overwrites the second number with most recent
            else:
                second = char

    # return string concat of the two number
    # assumed that if one number return it twice
    results = first + second if second != "" else first + first
    return int(results)


def read_line_2(s: str) -> int:
    first = ""
    second = ""

    i = 0
    j = len(s) - 1

    while first == "" or second == "":
        # iterate over each character
        l = s[i]
        r = s[j]

        if first == "":
            if l.isnumeric():
                first = l
            i += 1
        if second == "":
            if r.isnumeric():
                second = r
            j -= 1

    # return string concat of the two number
    # assumed that if one number return it twice
    results = first + second
    return int(results)


DICT = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}

FIRST = {"o", "t", "f", "s", "e", "n"}
COUNTS = [3, 4, 5]


def get_number(s: str, i: int):
    char = s[i]
    # if number store value
    if char.isnumeric():
        return char
    else:
        if s[i] in FIRST:
            # iterate over each possible count
            for count in COUNTS:
                # if the substring is in DICT
                word = s[i : i + count]
                if word in DICT:
                    return word


def read_line_calibrated(s: str) -> int:
    first = ""
    second = ""

    i = 0
    j = len(s) - 1
    # iterate over each character
    while first == "" or second == "":
        if first == "":
            left = get_number(s, i)

            if left:
                if left.isnumeric():
                    first = left
                else:
                    first = DICT[left]
                    i += len(left) - 1
            i += 1

        if second == "":
            right = get_number(s, j)
            if right and second == "":
                if right.isnumeric():
                    second = right
                else:
                    second = DICT[right]
                    j -= len(right) + 1
            j -= 1

    # return string concat of the two number
    results = first + second if second != "" else first + first
    return int(results)


if __name__ == "__main__":
    # Test cases for read_line helper
    assert read_line_2("1abc2") == 12, "Test 1: two numbers at end"
    assert read_line_2("pqr3stu8vwx") == 38, "Test 2: two numbers in middle"
    assert read_line_2("a1b2c3d4e5f") == 15, "Test 3: three numbers in middle"
    assert read_line_2("treb7uchet") == 77, "Test 4: one number"
    assert read_line_2("813eight") == 83, "Test 5"

    # Test cases for read_line_calibrated helper
    assert read_line_calibrated("two1nine") == 29, "Test 1"
    assert read_line_calibrated("eightwothree") == 83, "Test 2"
    assert read_line_calibrated("abcone2threexyz") == 13, "Test 3"
    assert read_line_calibrated("xtwone3four") == 24, "Test 4"
    assert read_line_calibrated("4nineeightseven2") == 42, "Test 5"
    assert read_line_calibrated("zoneight234") == 14, "Test 6"
    assert read_line_calibrated("7pqrstsixteen") == 76, "Test 7"
    assert read_line_calibrated("7pqrstoneight") == 78, "Test 8"

    # Solutions
    print("Solution 1: ", solution(read_line))
    print("Solution 1 v2: ", solution(read_line_2))

    print("Solution 2: ", solution(read_line_calibrated))
