from typing import List, Tuple
from collections import deque, defaultdict
from statistics import median


def lookup_close(bracket: str) -> str:
    """
    Helper function to find the closing bracket given an opening bracket

    Args:
        bracket (str): The opening bracket

    Returns:
        str: The closing bracket
    """
    if bracket == "(":
        return ")"
    elif bracket == "[":
        return "]"
    elif bracket == "{":
        return "}"
    elif bracket == "<":
        return ">"


def lookup_incorrect_points(bracket: str) -> int:
    """
    Helper function to return the incorrect score for each bracket.
    The scores are defined in the problem specification

    Args:
        bracket (str): The closing bracket

    Returns:
        int: The score associated with the closing bracket
    """
    if bracket == ")":
        return 3
    elif bracket == "]":
        return 57
    elif bracket == "}":
        return 1197
    elif bracket == ">":
        return 25137


def lookup_correct_points(bracket: str) -> int:
    """
    Helper function to return the correct score for each bracket.
    The scores are defined in the problem specification

    Args:
        bracket (str): The closing bracket

    Returns:
        int: The score associated with the closing bracket
    """
    if bracket == ")":
        return 1
    elif bracket == "]":
        return 2
    elif bracket == "}":
        return 3
    elif bracket == ">":
        return 4


def get_input() -> List[str]:
    return [line.strip() for line in open("Day_10_input.txt").readlines()]


def find_and_discard_corrupted_lines(lines: List[str]) -> Tuple[int, List[str]]:
    """
    Finds corrupted lines given a set list of lines (which is the input).
    A corrupted line is a set of brackets that do not resolve correctly (ex. "([])" is correct, "([{])" is not).
    Returns a tuple containing the incorrect score (calculated as per the problem specification)
    and a line containing only valid (and incomplete) lines.

    Args:
        lines (List[str]): The set of lines, which is the input

    Returns:
        Tuple[int, List[str]]: A tuple containing the incorrect score and a list containing only the valid (but incomplete) lines
    """

    # A set is used to identify the open brackets
    open_brackets = {"(", "[", "{", "<"}

    # A deque is used to keep track of the encountered brackets in order
    brackets_deque = deque()

    # A dictionary used to keep track of the number of incorrect closing brackets encountered in the input
    incorrect_brackets = defaultdict(int)

    # A list used to keep track of the indices for corrupted lines
    incorrect_lines_ind = []

    for num, line in enumerate(lines):
        for bracket in line:
            if bracket in open_brackets:
                brackets_deque.append(bracket)
            elif bracket != lookup_close(bracket=brackets_deque.pop()):
                incorrect_brackets[bracket] += 1
                incorrect_lines_ind.append(num)

    # Remove the corrupted lines from the input in reverse order, so that the indices can be used to remove the corrupted lines
    for num in sorted(incorrect_lines_ind, reverse=True):
        lines.pop(num)

    # Calculate the incorrect score, as per the problem definition
    incorrect_score = 0
    for bracket in incorrect_brackets.keys():
        incorrect_score += incorrect_brackets[bracket] * lookup_incorrect_points(
            bracket=bracket
        )

    return incorrect_score, lines


def fix_incomplete_lines(lines: List[str]) -> int:
    """
    Generates a set of brackets that would complete each line in the provided list of lines.
    For example, given "([{<>", the functon would generate "}])" to complete the line.
    The function then computes a correct score for each lines as defined by the problem specification,
    and returns its median.

    Args:
        lines (List[str]): A list of valid but incomplete lines

    Returns:
        int: The correct score, as per the problem specification
    """

    # A set is used to identify the opening brackets
    open_brackets = {"(", "[", "{", "<"}

    # A deque is used to keep track of the brackets in order
    brackets_deque = deque()

    # A list is used to keep track of all correct scores for all lines
    correct_scores = []

    for line in lines:
        for bracket in line:
            if bracket in open_brackets:
                brackets_deque.append(bracket)

            # No need to validate closing brackets, as corrupted lines were already removed in Part 1
            else:
                brackets_deque.pop()

        correct_brackets = []
        while len(brackets_deque) > 0:
            correct_brackets.append(lookup_close(bracket=brackets_deque.pop()))

        # Add a new item in the correct_scores list and calculate the correct score, as per the problem specification
        correct_scores.append(0)
        for bracket in correct_brackets:
            correct_scores[-1] *= 5
            correct_scores[-1] += lookup_correct_points(bracket=bracket)

    return median(correct_scores)


def main():
    lines = get_input()
    incorrect_score, incomplete_lines = find_and_discard_corrupted_lines(lines=lines)
    print("Answer to Part 1:", incorrect_score)
    correct_score = fix_incomplete_lines(lines=incomplete_lines)
    print("Answer to Part 2:", correct_score)


if __name__ == "__main__":
    main()
