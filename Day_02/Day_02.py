from typing import Iterable

# Represents the current position. If aim is not enabled, the depth changes with "down" or "up" commands. If aim is enabled, the depth changes only with "forward" commands
class ShipPosition:
    def __init__(self, enable_aim: bool = False):
        self._horizontal = 0
        self._depth = 0
        self._aim = 0
        self._enable_aim = enable_aim

    def move_forward(self, quantity: int):
        if self._enable_aim == True:
            self._depth += self._aim * quantity
        self._horizontal += quantity

    def move_down(self, quantity: int):
        if self._enable_aim == True:
            self._aim += quantity
        else:
            self._depth += quantity

    def move_up(self, quantity: int):
        if self._enable_aim == True:
            self._aim -= quantity
        else:
            self._depth -= quantity

    def get_horizontal(self):
        return self._horizontal

    def get_depth(self):
        return self._depth


# Class to hold each direction and the quantity of each movement
class Direction:
    def __init__(self, direction: str, quantity: int):
        self._direction = direction
        self._quantity = int(quantity)

    def get_direction(self):
        return self._direction

    def get_quantity(self):
        return self._quantity


def get_input() -> Iterable[Direction]:
    return [
        Direction(direction.split(" ")[0], direction.split(" ")[1])
        for direction in open("Day_02_input.txt").readlines()
    ]


def get_final_position(
    ship_position: ShipPosition, directions: Iterable[Direction]
) -> int:
    for direction in directions:
        if direction.get_direction() == "forward":
            ship_position.move_forward(direction.get_quantity())
        if direction.get_direction() == "down":
            ship_position.move_down(direction.get_quantity())
        if direction.get_direction() == "up":
            ship_position.move_up(direction.get_quantity())
    return ship_position.get_horizontal() * ship_position.get_depth()


def main():
    directions = get_input()
    print(
        "Answer to Part 1:",
        get_final_position(ShipPosition(enable_aim=False), directions),
    )
    print(
        "Answer to Part 2:",
        get_final_position(ShipPosition(enable_aim=True), directions),
    )


if __name__ == "__main__":
    main()
