from typing import List, Tuple, Set
from copy import copy


def get_input() -> List[List[int]]:
    return [
        [int(num) for num in line.strip()]
        for line in open("Day_11_input.txt").readlines()
    ]


def get_adj_coor(row: int, col: int) -> List[Tuple[int]]:
    """
    Helper function to return all adjacent coordinates (vertically, horizontally, and diagonally adjacent)
    given a row and column number

    Args:
        row (int): The row number
        col (int): The column number

    Returns:
        List[Tuple[int]]: A list of tuples representing the row and column (row, col)
    """
    return [
        (row - 1, col),
        (row - 1, col - 1),
        (row - 1, col + 1),
        (row + 1, col),
        (row + 1, col - 1),
        (row + 1, col + 1),
        (row, col - 1),
        (row, col + 1),
    ]


def simulate_single_cycle(levels_map: List[List[int]], copy=False) -> int:
    """
    A helper function to simulates the progression of one cycle in the levels map.
    The levels map parameter is modified in the function if 'copy' is set to 'True', and will be modified in the calling function.
    For each cycle, all levels are increased by 1.
    If the level exceeds 9, it 'flashes' and increases all surrounding numbers (vertically, horizontally, diagonally) by 1.
    Once a level flashes once, it does not increase again and remains at 0.

    Args:
        levels (List[List[int]]): The levels map to simualte a single cycle on
        copy (bool): Set to 'True' to preserve the original parameter in the calling function

    Returns:
        int: The number of levels that flashed this turn
    """

    levels = []
    if copy == True:
        levels = [line.copy() for line in levels]
    else:
        levels = levels_map

    # Indicate when the row or column is not valid
    row_limit = {-1, len(levels)}
    col_limit = {-1, len(levels[0])}

    # Keep track of the all the coordinates that have flashed already
    already_flashed = set()

    # Iterate through every item in the map
    for row, line in enumerate(levels):
        for col, level in enumerate(line):

            # If the number has already flashed, do not do anything
            if (row, col) in already_flashed:
                continue

            # If the level is below 9, it will not flash this turn
            elif level < 9:
                levels[row][col] += 1

            # if the level is 9, it will flash this turn
            elif levels[row][col] == 9:
                to_flash_queue = [(row, col)]
                while len(to_flash_queue) > 0:
                    flash = to_flash_queue.pop()
                    already_flashed.add(flash)
                    levels[flash[0]][flash[1]] = 0
                    for adj_row, adj_col in get_adj_coor(row=flash[0], col=flash[1]):
                        if (
                            (adj_row, adj_col) not in already_flashed
                            and adj_row not in row_limit
                            and adj_col not in col_limit
                        ):
                            levels[adj_row][adj_col] += 1
                            if levels[adj_row][adj_col] > 9:
                                levels[adj_row][adj_col] = 0
                                to_flash_queue.append((adj_row, adj_col))
    return len(already_flashed)


def count_flashes(levels_map: List[List[int]], cycles: int) -> int:
    """
    Simulates the number of cycles provided and returns the number of levels that flashed

    Args:
        levels_map (List[List[int]]): The map of levels, which is the input file
        cycles (int): The number of cycles to go through

    Returns:
        int: The count of numbers that flashed
    """

    # Copy the parameter to preserve the original input
    levels = [line.copy() for line in levels_map]
    total_flashes = 0

    # Simulate the number of cycles specified
    for cycle in range(0, cycles):
        flashed = simulate_single_cycle(levels_map=levels)
        total_flashes += flashed

    return total_flashes


def find_synchronized_step(levels_map: List[List[int]]) -> int:
    """
    Will find the first step (the 'synchronized step') where all levels flash (exceed the value of 9).

    Args:
        levels_map (List[List[int]]): The levels map (the given input)

    Returns:
        int: The first step where all levels exceed the value of 9
    """

    # Copy the parameter to preserve the original input
    levels = [line.copy() for line in levels_map]
    step = 0

    # Execute an infinite loop until the synchronizing step is found
    while 1 == 1:
        step += 1
        flashed = simulate_single_cycle(levels_map=levels)

        if flashed == len(levels) * len(levels[0]):
            return step


def main():
    levels = get_input()
    print("Answer to Part 1:", count_flashes(levels_map=levels, cycles=100))
    print("Answer to Part 2:", find_synchronized_step(levels_map=levels))


if __name__ == "__main__":
    main()
