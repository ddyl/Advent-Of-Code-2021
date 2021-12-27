from typing import Tuple, Set, List
from regex import search


def get_input() -> Tuple[Set[Tuple[int, int]], List[Tuple[str, int]]]:
    """
    Read in the input data

    Returns:
        Set[Tuple[int, int]], List[Tuple[str, int]]: Returns a set of coordinates and a list of instructions.
        One coordinate or instruction is represented as a tuple
    """
    coordinates = set()
    instructions = []
    with open("Day_13_input.txt") as file:
        line = file.readline().strip()
        # The coordinates and instructions are separated by a newline
        while line != "":
            coordinates.add((int(line.split(",")[0]), int(line.split(",")[1])))
            line = file.readline().strip()

        # The instructions will contain a direction (x or y) and a location (where to fold)
        for line in file.readlines():
            ins = search(r"[xy]=[0-9]*", line).group()
            instructions.append((ins.split("=")[0], int(ins.split("=")[1])))

    return coordinates, instructions


def do_single_fold(coordinates: Set[Tuple[int, int]], instruction: Tuple[str, int]):
    """
    A helper function to a single fold for a single instruction

    Args:
        coordinates (Set[Tuple[int, int]]): The set of coordinates that will be continuously modified by the function
        instruction (Tuple[str, int]): The instrucitons by which to modify this function
    """
    direction = instruction[0]
    location = instruction[1]
    coor_to_move = [
        coor
        for coor in coordinates
        if (direction == "x" and coor[0] > location)
        or (direction == "y" and coor[1] > location)
    ]

    for coor in coor_to_move:
        coordinates.remove(coor)
        if direction == "x":
            coordinates.add((coor[0] - (coor[0] - location) * 2, coor[1]))
        elif direction == "y":
            coordinates.add((coor[0], coor[1] - (coor[1] - location) * 2))


def fold_paper(
    coordinates: Set[Tuple[int, int]],
    instructions: List[Tuple[str, int]],
    step_amt: int = 0,
) -> Set[Tuple[int, int]]:
    """
    A wrapper method to carry out the instructions, either a couple at a time or all at once.

    Args:
        coordinates (Set[Tuple[int, int]]): The set of coordinates given by the input. Will not be modified by this function.
        instructions (List[Tuple[str, int]]): The set of instructions given by the input. Will not be modified by this function.
        step_amt (int, optional): The number of instructions to carry out. If 0, all instructions are carried out. Defaults to 0.

    Returns:
        Set[Tuple[int, int]]: The set of remaining coordinates
    """

    coordinates = set(coordinates)

    if step_amt > 0:
        for i in range(0, min(step_amt, len(instructions))):
            do_single_fold(coordinates=coordinates, instruction=instructions[i])
    else:
        for instruction in instructions:
            do_single_fold(coordinates=coordinates, instruction=instruction)

    return coordinates


def pretty_print_coordinates(coordinates: Set[Tuple[int, int]]) -> str:
    """
    The coordinates actually have to be shown as a display and typed in to the prompt to answer the question.
    This function returns a string that pretty prints the coordinates.

    Args:
        coordinates (Set[Tuple[int, int]]): The set of coordinates to display

    Returns:
        str: A pretty-printed string that shows the coordinates
    """
    max_x = 0
    max_y = 0
    for coor in coordinates:
        if coor[0] > max_x:
            max_x = coor[0]
        if coor[1] > max_y:
            max_y = coor[0]
    display = [" " * (max_x + 1)] * (max_y + 1)
    for coor in coordinates:
        line = display[coor[1]]
        display[coor[1]] = line[: coor[0]] + "|" + line[coor[0] + 1 :]
    return "\n".join(display)


def main():
    coor, ins = get_input()

    new_coordinates = fold_paper(coordinates=coor, instructions=ins, step_amt=1)
    print("Answer to Part 1:", len(new_coordinates))

    new_coordinates = fold_paper(coordinates=coor, instructions=ins)
    pretty_print = pretty_print_coordinates(coordinates=new_coordinates)
    print("Answer to Part 2:")
    print(pretty_print)


if __name__ == "__main__":
    main()
