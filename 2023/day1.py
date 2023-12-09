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


def read_line_calibrated(s: str) -> int:
    first = ""
    second = ""

    i = 0
    # iterate over each character
    while i < len(s):
        char = s[i]
        # if number store value
        if char.isnumeric():
            if first == "":
                first = char
            # overwrites the second number with most recent
            else:
                second = char
        else:
            # if char is in FIRST
            if char in FIRST:
                # iterate over each possible count
                for count in COUNTS:
                    # if the substring is in DICT
                    word = s[i : i + count]
                    if word in DICT:
                        # convert to number and move the index up by count
                        num = DICT[word]
                        if first == "":
                            first = num
                        # overwrites the second number with most recent
                        else:
                            second = num
                        i += count - 1
                        break
        i += 1
    # return string concat of the two number
    # assumed that if one number return it twice
    results = first + second if second != "" else first + first
    return int(results)


if __name__ == "__main__":
    # Test cases for read_line helper
    assert read_line("1abc2") == 12, "Test 1: two numbers at end"
    assert read_line("pqr3stu8vwx") == 38, "Test 2: two numbers in middle"
    assert read_line("a1b2c3d4e5f") == 15, "Test 3: three numbers in middle"
    assert read_line("treb7uchet") == 77, "Test 4: one number"

    # Test cases for read_line_calibrated helper
    assert read_line_calibrated("two1nine") == 29, "Test 1"
    assert read_line_calibrated("eightwothree") == 83, "Test 2"
    assert read_line_calibrated("abcone2threexyz") == 13, "Test 3"
    assert read_line_calibrated("xtwone3four") == 24, "Test 4"
    assert read_line_calibrated("4nineeightseven2") == 42, "Test 5"
    assert read_line_calibrated("zoneight234") == 14, "Test 6"
    assert read_line_calibrated("7pqrstsixteen") == 76, "Test 7"

    # Solutions
    # print("Solution 1: ", solution(read_line))

    print("Solution 2: ", solution(read_line_calibrated))
