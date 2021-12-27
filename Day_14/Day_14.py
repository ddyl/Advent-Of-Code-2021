from collections import defaultdict, deque, Counter
from typing import DefaultDict, Counter


def get_input() -> tuple[str, DefaultDict[str, str]]:
    """
    Read the input data and return the template and instructions for polymer production.

    Returns:
        tuple[str, DefaultDict[str, str]]: A tuple containing the initial template, and a dict of polymer construction instructions
    """
    template = ""
    instructions = defaultdict(str)
    with open("Day_14_input.txt") as file:
        template = file.readline().strip()
        file.readline()
        for line in file.readlines():
            i, j = line.strip().split(" -> ")
            instructions[i] = j
    return template, instructions


def extend_polymer(template: str, ins: DefaultDict[str, str], steps: int) -> int:
    """
    Constructs the new polymer according to the inital template and instructions for the specified number of steps.
    Then, it returns (count of most frequently recurring element - count of least frequently recurring element)

    Args:
        template (str): The initial template, provided by the input data
        ins (DefaultDict[str, str]): The instructions, provided by the input data
        steps (int): The number of iterations to generate the new polymer for

    Returns:
        int: The difference between the count of the most frequently and least frequently recurring elements
    """

    # A counter for all polymer pairs. Each pair overlaps in the initial template (ex. 'abc' has 2 pairs - 'ab' and 'bc')
    polymer_pairs = Counter()
    for i in range(0, len(template) - 1):
        polymer_pairs[template[i : i + 2]] += 1

    # For each specified step, generate new pairs as per the instructions and keep a count of all pairs in the new polymer
    for step in range(0, steps):
        modified_polymer_pairs = Counter()
        for pair in polymer_pairs.keys():
            modified_polymer_pairs[pair[0] + ins[pair]] += polymer_pairs[pair]
            modified_polymer_pairs[ins[pair] + pair[1]] += polymer_pairs[pair]
        polymer_pairs = modified_polymer_pairs

    # A counter to hold the number of occurrences for each letter
    element_counts = Counter()
    for pair in polymer_pairs.keys():
        element_counts[pair[0]] += polymer_pairs[pair]
        element_counts[pair[1]] += polymer_pairs[pair]

    # All elements in the polymer is counted twice except the first and last characters in the initial template. So add one to the counts for both
    # Ex. For template 'abc', which has pairs 'ab' and 'bc', 'a' and 'c' are counted once, while 'b' is counted twice
    element_counts[template[0]] += 1
    element_counts[template[-1]] += 1

    # Calculate the difference between the most frequently and least frequently occuring element, and return it
    # Divide the difference by 2 before returning it, because each element is counted twice
    return int((max(element_counts.values()) - min(element_counts.values())) / 2)


def main():
    template, instructions = get_input()

    diff = extend_polymer(template=template, ins=instructions, steps=10)
    print("Answer to Part 1:", diff)

    diff = extend_polymer(template=template, ins=instructions, steps=40)
    print("Answer to Part 2:", diff)


if __name__ == "__main__":
    main()
