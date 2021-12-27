from collections import defaultdict
from collections import defaultdict
from typing import Tuple, DefaultDict, Set, Dict, List
from regex import search


def get_input() -> Tuple[Set[Tuple[int, int]], DefaultDict[str, int]]:
    coordinates = set()
    instructions = defaultdict(list)
    with open("Day_13_input.txt") as file:
        line = file.readline().strip()
        while line != "":
            coordinates.add((int(line.split(",")[0]), int(line.split(",")[1])))
            line = file.readline().strip()

        for line in file.readlines():
            instruction = search(r"[xy]=[0-9]*", line).group()
            instructions[instruction.split("=")[0]].append(
                int(instruction.split("=")[1])
            )

    return coordinates, instructions


def fold_paper(
    coordinates: Set[Tuple[int, int]], instructions: Dict[str, List[int]]
) -> Set[Tuple[int, int]]:

    coordinates = set(coordinates)

    for direction in instructions.keys():
        for location in instructions[direction]:
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

    return coordinates


def main():
    coordinates, instructions = get_input()
    new_coordinates = fold_paper(coordinates=coordinates, instructions=instructions)
    print(len(new_coordinates))
    for coor in new_coordinates:
        print(coor)


if __name__ == "__main__":
    main()
