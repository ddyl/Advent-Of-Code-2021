from typing import Iterable


def get_input() -> Iterable[int]:
    return [int(num) for num in open("Day_01_input.txt").readlines()]


# Determine the number of times the depth increases. Answers Part 1
def increase_count_one_depth(depths: int) -> int:
    increases = 0
    i = 1
    while i < len(depths):
        if depths[i - 1] < depths[i]:
            increases += 1
        i += 1
    return increases


# Determine the number of times the depth increases on a three-element sliding window sum. Answers Part 2
def increase_count_three_depths(depths: int) -> int:
    increases = 0
    i = 2
    while i < len(depths) - 1:
        temp = depths[i] + depths[i - 1]
        if temp + depths[i - 2] < temp + depths[i + 1]:
            increases += 1
        i += 1
    return increases


def main():
    depthList = get_input()
    print("Part 1 Answer:", increase_count_one_depth(depths=depthList))
    print("Part 2 Answer:", increase_count_three_depths(depths=depthList))


if __name__ == "__main__":
    main()
