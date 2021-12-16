from typing import Tuple, List
from re import findall


class CoorPair:
    """
    Class to hold all coordinate pairs. The coordinate with minimum x (or minimum y if both x coordinates are the same) will
    always come first, meaning that any calculations for diagonal lines will need to handle positive and negative slopes separately.
    """

    def __init__(self, x1: int, y1: int, x2: int, y2: int):
        self.x1 = None
        self.x2 = None
        self.y1 = None
        self.y2 = None
        self.horizontal = False
        self.vertical = False
        self.diagonal = False

        if x1 == x2:
            self.vertical = True
            if y1 < y2:
                self.x1 = x1
                self.y1 = y1
                self.x2 = x2
                self.y2 = y2
            else:
                self.x1 = x2
                self.y1 = y2
                self.x2 = x1
                self.y2 = y1
        elif y1 == y2:
            self.horizontal = True
            if x1 < x2:
                self.x1 = x1
                self.y1 = y1
                self.x2 = x2
                self.y2 = y2
            else:
                self.x1 = x2
                self.y1 = y2
                self.x2 = x1
                self.y2 = y1
        else:
            self.diagonal = True
            if x1 < x2:
                self.x1 = x1
                self.y1 = y1
                self.x2 = x2
                self.y2 = y2
            else:
                self.x1 = x2
                self.y1 = y2
                self.x2 = x1
                self.y2 = y1


def get_input() -> List[CoorPair]:
    """
    Reads the input file and returns all coordinate pairs as a list of CoorPair instances

    Returns:
        List[CoorPair]: List of coordinate pairs
    """
    coor_pairs = []
    with open("Day_05_input.txt") as file:
        for line in file.readlines():
            coors = findall("[0-9]+", line)
            coor_pairs.append(
                CoorPair(int(coors[0]), int(coors[1]), int(coors[2]), int(coors[3]))
            )
    return coor_pairs


def generate_all_points(pair: CoorPair) -> set[Tuple[int]]:
    """
    Given a CoorPair instance, will generate all possible points as a set of tuples

    Args:
        pair (CoorPair): The coordinate pair to generate all points for, supplied as a CoorPair instance

    Returns:
        set[Tuple[int]]: A set of int tuples, each of which will represent a coordinate
    """

    # Handle the case when the line is a horizontal line
    if pair.horizontal == True:
        return {(x, pair.y1) for x in range(pair.x1, pair.x2 + 1)}

    # Handle the case when the line is a vertical line
    if pair.vertical == True:
        return {(pair.x1, y) for y in range(pair.y1, pair.y2 + 1)}

    if pair.diagonal == True:
        # Handle the case when the diagonal line is a positive line
        if pair.y1 < pair.y2:
            return {(pair.x1 + i, pair.y1 + i) for i in range(0, pair.y2 - pair.y1 + 1)}

        # Handle the case when the diagonal line is a positive line
        if pair.y1 > pair.y2:
            return {(pair.x1 + i, pair.y1 - i) for i in range(0, pair.y1 - pair.y2 + 1)}


def get_overlapping_coordinates(
    pair1: CoorPair, pair2: CoorPair
) -> List[Tuple[int, int]]:
    """
    Given two coordinate pairs, generates all possible points for each pair and finds the intersecting coordinates

    Args:
        pair1 (CoorPair): The first coordinate pair
        pair2 (CoorPair): The second coordinate pairs

    Returns:
        List[Tuple[int, int]]: All intersecting coordinates between the two pairs
    """
    set1 = generate_all_points(pair1)
    set2 = generate_all_points(pair2)

    return [coor for coor in set1 if coor in set2]


def count_overlapping_coordinates(
    pairs: List[CoorPair], include_diagonals: bool
) -> int:
    """
    Generates a set of all overlapping coordinates and returns the number of coordinates. A point that overlaps three times still gets
    counted once

    Args:
        pairs (List[CoorPair]): The list of coordinate pairs, represented by a list of CoorPair class instances
        include_diagonals (bool): Indicates whether diagonal pairs should be included

    Returns:
        int: The number of overlapping coordinates
    """
    overlapping_coordinates = set()
    for i, pair in enumerate(pairs):
        while i < len(pairs) - 1:
            i += 1
            overlaps = set()
            if include_diagonals == False:
                if pair.diagonal == False and pairs[i].diagonal == False:
                    overlaps = get_overlapping_coordinates(pair, pairs[i])
            else:
                overlaps = get_overlapping_coordinates(pair, pairs[i])
            for overlap in overlaps:
                overlapping_coordinates.add(overlap)

    return len(overlapping_coordinates)


def main():
    pairs = get_input()
    print(
        "Part 1 solution:",
        count_overlapping_coordinates(pairs, include_diagonals=False),
    )
    print(
        "Part 2 solution:", count_overlapping_coordinates(pairs, include_diagonals=True)
    )


if __name__ == "__main__":
    main()
