from typing import Iterable, Tuple


def most_common_bit(nums: Iterable[int], position: int) -> int:
    """Finds the most common bit given an integer list and a position

    Args:
        nums (Iterable[int]): The list of integers to look at
        position (int): The bit position

    Returns:
        int: The most common bit, or -1 if they are equally represented
    """
    mask = 0x1 << position - 1
    count_one = 0
    count_zero = 0
    for num in nums:
        count_one += (num & mask) > 0
        count_zero += (num & mask) == 0
    if count_one > count_zero:
        return 1
    elif count_one < count_zero:
        return 0
    else:
        return -1


def find_gamma_epsilon_product(diagnostics: Iterable[int], bin_len: int) -> int:
    """Calculates gamma and epsilon, as per the problem specification in Advent of Code, and returns its product

    Args:
        diagnostics (Iterable[int]): A list of puzzle input numbers, converted from a binary string (ex. '010101') to an int
        bin_len (int): The length of each binary string in the puzzle, which is the same for all inputs (strings are padded with leading zeros when necessary)

    Returns:
        int: The product of gamma and epsilon as defined by Advent of Code
    """
    # The index of the list will represent the bit position
    # The value will represent the number of diagnostic int that have that position set to 1
    gamma = 0x0
    epsilon = 0x0

    while bin_len > 0:

        # If 1 is more common in the position than 0, increase gamma by bitwise OR. Else, increase epsilon
        if most_common_bit(nums=diagnostics, position=bin_len) == 1:
            gamma |= 0x1 << bin_len - 1
        else:
            epsilon |= 0x1 << bin_len - 1

        bin_len -= 1

    return gamma * epsilon


def find_o2_co2_product(diagnostics: Iterable[int], bin_len: int) -> int:
    """Calculates the product of the oxygen and carbon dioxide rate, as per the specification in Advent of Code

    Args:
        diagnostics (Iterable[int]): A list of puzzle input numbers, converted from binary string (ex. '010101') to an int
        bin_len (int): The length of each binary string in the puzzle, which is the same for all inputs (strings are padded with leading zeros when necessary)

    Returns:
        int: The product of oxygen and carbon dioxide rate, as per the specification in Advent of Code
    """
    oxygen = diagnostics
    position = bin_len
    while len(oxygen) > 1:
        common_bit = most_common_bit(oxygen, position)

        # The problem specifies that if 0's and 1's are equally represented in a position, 1 should be used
        if common_bit == -1:
            common_bit = 1

        temp = []
        for num in oxygen:
            if ((num >> (position - 1)) & 0x1) == common_bit:
                temp.append(num)
        oxygen = temp
        position -= 1

    carbon_dioxide = diagnostics
    position = bin_len
    while len(carbon_dioxide) > 1:
        common_bit = most_common_bit(carbon_dioxide, position)

        # The problem specifies that the less common bit should be used, and 0 should be used if 0 and 1 are equally represented
        if common_bit == -1 or common_bit == 1:
            common_bit = 0
        else:
            common_bit = 1

        temp = []
        for num in carbon_dioxide:
            if ((num >> (position - 1)) & 0x1) == common_bit:
                temp.append(num)
        carbon_dioxide = temp
        position -= 1

    return oxygen[0] * carbon_dioxide[0]


# Converts the binary string into its equivalent integer, and returns the length of each binary array (length is constant in the output)
def get_input() -> Tuple[Iterable[int], int]:
    return (
        [int(num, 2) for num in open("Day_03_input.txt").readlines()],
        len(open("Day_03_input.txt").readlines()[0].strip()),
    )


def main():
    diagnostics = get_input()
    print(
        "Answer to Part 1:",
        find_gamma_epsilon_product(diagnostics=diagnostics[0], bin_len=diagnostics[1]),
    )
    print(
        "Answer to Part 2:",
        find_o2_co2_product(diagnostics=diagnostics[0], bin_len=diagnostics[1]),
    )


if __name__ == "__main__":
    main()
