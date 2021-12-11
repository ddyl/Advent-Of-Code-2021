from re import findall
from typing import Tuple, List
from collections import defaultdict


class Display:
    def __init__(self, pattern: List[str], output: List[str]):
        self.pattern = pattern
        self.output = output


def get_input() -> List[Display]:
    displays = []
    with open("Day_08_input.txt") as file:
        for line in file.readlines():
            pattern, output = line.split("|")
            displays.append(
                Display(findall("[a-g]+", pattern), findall("[a-g]+", output))
            )
    return displays


def count_unique_digit(display: Display) -> int:
    """
    Counts the number of digits with a unique number of segments and returns the count.
    The unique segments are 1, 4, 7, and 8, which have 2, 4, 3, and 7 segments respectively

    Args:
        display (Display): A Display class variable

    Returns:
        int: Number of occurrences of 1, 4, 7, and 8 patterns
    """
    unique_digit = 0
    for digit in display.output:
        if len(digit) in [2, 3, 4, 7]:
            unique_digit += 1
    return unique_digit


def identify_digits(patterns: List[int]) -> defaultdict[int]:
    """
    Just from the letters of each pattern and each pattern length, it is possible to determine all numbers.
    This function does that and returns a dictionary mapping each pattern to a number.
    The comparisons made are as follows:
        1. Numbers 1, 4, 7, 8 can be identified purely by the number of segments they have
        2. Numbers with 6 segments (0, 6, 9) can be identified next (4 is a subset of 9, 1 is a subset of 0, the remaining pattern is 6)
        3. Numbers with 5 segments (2, 3, 5) can be identified next (1, is a subset of 3, 4 has 3 segments not matching with 5, the remaining pattern is 2)

    Args:
        patterns (List[int]): The patterns representing the combination of segments

    Returns:
        defaultdict[int]: A dictionary mapping each pattern to a number
    """
    identified_digits = defaultdict(str)

    # Identify all numbers with a unique number of segments
    for digit in patterns:
        if len(digit) == 2:
            identified_digits[1] = digit
        elif len(digit) == 3:
            identified_digits[7] = digit
        elif len(digit) == 4:
            identified_digits[4] = digit
        elif len(digit) == 7:
            identified_digits[8] = digit

    # Identify all numbers made up of 6 segments
    for digit in patterns:
        if len(digit) == 6:
            if set(identified_digits[4]).issubset(set(digit)):
                identified_digits[9] = digit
            elif set(identified_digits[1]).issubset(set(digit)):
                identified_digits[0] = digit
            else:
                identified_digits[6] = digit

    # Identify all numbers made up of 5 segments
    for digit in patterns:
        if len(digit) == 5:
            if set(identified_digits[1]).issubset(set(digit)):
                identified_digits[3] = digit
            elif len(set(identified_digits[4]).symmetric_difference(set(digit))) == 3:
                identified_digits[5] = digit
            else:
                identified_digits[2] = digit

    return identified_digits


def get_output(display: Display) -> int:
    """
    Based on the output of the function identify_digits, computes the output and returns it

    Args:
        display (Display): A Display class variable

    Returns:
        int: The number that the output represents
    """
    digits = identify_digits(display.pattern)

    output = 0

    for digit in display.output:
        for key in digits.keys():
            if set(digit) == set(digits[key]):
                output *= 10
                output += key

    return output


def wrapper(part_1: bool, part_2: bool, displays: List[Display]):
    """
    Is a wrapper class to execute the appropriate functions for each display in the input

    Args:
        part_1 (bool): Indicates if the wrapper is to solve part 1
        part_2 (bool): Indicates if the wrapper is to solve part 2
        displays (List[Display]): The list of displays, obtained from the input

    Returns:
        [type]: The final answer, which is an integer
    """
    if part_1:
        total_unique_digit = 0
        for display in displays:
            total_unique_digit += count_unique_digit(display)
        return total_unique_digit
    if part_2:
        all_output_sum = 0
        for display in displays:
            all_output_sum += get_output(display)
        return all_output_sum


def main():
    displays = get_input()

    print("Answer to Part 1:", wrapper(part_1=True, part_2=False, displays=displays))
    print("Answer to Part 2:", wrapper(part_1=False, part_2=True, displays=displays))


if __name__ == "__main__":
    main()
