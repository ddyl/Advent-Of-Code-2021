from statistics import median, mean
from typing import List


def get_median_cost(positions: List[int]) -> int:
    """
    Returns the fuel cost to navigate to the median of the position

    Args:
        positions (List[int]): List of positions

    Returns:
        int: The total fuel cost
    """
    target = int(median(positions))
    fuel = 0
    for position in positions:
        fuel += abs(position - target)
    return fuel


def get_mean_cost(positions: List[int]) -> int:
    """
    Returns the fuel cost to navigate to the mean of the position. Checks 5 different estimates
    (the mean being the middle number) and returns the minimum fuel cost.

    Args:
        positions (List[int]): List of positions

    Returns:
        int: The total fuel cost
    """
    target = round(mean(positions))
    fuel = 0

    estimates = [target - 2, target - 1, target, target + 1, target + 2]
    costs = []

    for estimate in estimates:
        cost = 0
        for position in positions:
            # Use Gaussian Sum to calculate the cost
            n = abs(estimate - position)
            cost += (n * (n + 1)) / 2
        costs.append(int(cost))

    return min(costs)


def get_input() -> List[int]:
    return [int(num) for num in open("Day_07_input.txt").readline().split(",")]


def main():
    positions = get_input()
    print("Answer to Part 1:", get_median_cost(positions=positions))
    print("Answer to Part 2:", get_mean_cost(positions=positions))


if __name__ == "__main__":
    main()
