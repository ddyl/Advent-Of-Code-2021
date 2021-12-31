from random import gauss
from regex import findall


def get_input() -> tuple[tuple[int], tuple[int]]:
    """
    Read in the input data and return the target square's x and y ranges as a tuple

    Returns:
        tuple[tuple[int], tuple[int]]: A tuple for the x range and a tuple for the y range
    """
    coordinates = findall(r"-?[0-9]+", open("Day_17_input.txt").readline())
    x_bounds = (int(coordinates[0]), int(coordinates[1]))
    y_bounds = (int(coordinates[2]), int(coordinates[3]))
    return x_bounds, y_bounds


def get_max_y(y_bounds: tuple) -> int:
    """
    The maximum possible height is the Gauss sum of the absolute value of: minimum bound for y - 1.
    Please see the attached markdown file (Day_17_explanation.md) in the same directory for further explanation.

    Args:
        y_bounds (tuple): The y boundaries for the target square, given as a tuple

    Returns:
        int: The maximum possible height to reach the target square
    """
    n = abs(min(y_bounds)) - 1
    return int((n * (n + 1)) / 2)


def get_gauss_num(num: int) -> int:
    """
    Get the number whose Gauss sum is the closest to (and greater than) that of the provided number.

    Args:
        num (int): The provided number. The returned number's Gauss sum is the closest to (and greater than) this number

    Returns:
        int: The number whose Gauss sum is closest to (and greater than) the provided number
    """
    i = 0
    gauss_sum = 0
    while gauss_sum < num:
        i += 1
        gauss_sum = (i * (i + 1)) / 2
    return i


def check_if_hit(x: int, y: int, x_bounds: tuple[int], y_bounds: tuple[int]) -> bool:
    """
    Checks if the given starting (x, y) velocities land in the target square given by the input

    Args:
        x (int): The starting x velocity
        y (int): The starting y velocity
        x_bounds (tuple[int]): The target square's x bounds, as defined by the problem
        y_bounds (tuple[int]): The target square's y bounds, as defined by the problem

    Returns:
        bool: Returns True if the starting velocities land in the target square, False if not
    """
    x_coor = 0
    y_coor = 0
    while True:
        if x_coor > max(x_bounds) or y_coor < min(y_bounds):
            break
        x_coor += x
        y_coor += y
        if x != 0:
            x -= 1
        y -= 1
        if (
            x_coor >= min(x_bounds)
            and x_coor <= max(x_bounds)
            and y_coor >= min(y_bounds)
            and y_coor <= max(y_bounds)
        ):
            return True
    return False


def get_all_starts(x_bounds: tuple, y_bounds: tuple) -> list[tuple[int]]:
    """
    Returns all starting velocities that eventually result in a coordinate in the target square

    Args:
        x_bounds (tuple): The x boundaries of the target square, as defined by the puzzle input
        y_bounds (tuple): The y boundaries of the target square, as defined by the puzzle input

    Returns:
        list[tuple[int]]: A list of tuples, where each tuple represents the x and y starting velocities
    """

    # Define the lower and upper limits for the starting x velocity
    # The x value decreases by one for each step, effectively making the minimum value the first value where the Guassian sum crosses the minimum x bound
    # The maximum x value is the maximum possible starting x velocity
    x_limit = (get_gauss_num(num=min(x_bounds)), max(x_bounds))

    # Define the lower and upper limits for the starting y velocity
    # The minimum bound is the lowermost y bound (which is a negative number)
    # The maximum bound is the absolute value of the lowest y bound. Any value larger than this will miss the y bound entirely
    y_limit = (min(y_bounds), abs(min(y_bounds)))
    all_coor = []

    for x in range(x_limit[0], x_limit[1] + 1):
        for y in range(y_limit[0], y_limit[1] + 1):
            if check_if_hit(x=x, y=y, x_bounds=x_bounds, y_bounds=y_bounds) == True:
                all_coor.append((x, y))

    return all_coor


def main():
    x_bounds, y_bounds = get_input()
    print("Answer to Part 1:", get_max_y(y_bounds=y_bounds))
    all_start_coor = get_all_starts(x_bounds=x_bounds, y_bounds=y_bounds)
    print("Answer to Part 2:", len(all_start_coor))


if __name__ == "__main__":
    main()
