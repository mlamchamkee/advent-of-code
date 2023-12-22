def count_ways(t: int, d: int):
    sum = 0
    for i in range(t):
        speed = i
        travel = (t - i) * speed
        if travel > d:
            sum += 1
    return sum


def solution(races):
    prod = 1
    for race in races:
        prod *= count_ways(race[0], race[1])
    return prod


def solution2():
    pass


if __name__ == "__main__":
    """Unit Tests"""
    assert count_ways(7, 9) == 4, "count_ways, Test 1"

    example1 = solution([(7, 9), (15, 40), (30, 200)])
    print("Example 1: ", example1)
    assert example1 == 288, "Test Example 1"

    solution1 = solution([(59, 430), (70, 1218), (78, 1213), (78, 1276)])
    print("Solution 1: ", solution1)

    example2 = count_ways(71530, 940200)
    print("Example 2: ", example2)
    assert example2 == 71503, "Test Example 2"

    solution2 = count_ways(59707878, 430121812131276)
    print("Solution 2: ", solution2)
