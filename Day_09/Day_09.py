from typing import List, Tuple
from re import findall


def get_input() -> List[List[int]]:
    """
    Returns the input string as a 2-dimensional integer list

    Returns:
        List[List[int]]: A two dimensional list of integers
    """
    return [
        list(map(int, findall(r"[0-9]", line)))
        for line in open("Day_09_input.txt").readlines()
    ]


def get_min_risk_levels(height_map: List[List[int]]) -> int:
    """
    Evaluates the numbers around the grid (horizontally and vertically) to determine the minimum risk levels.
    Returns the sum of all (minimum risk level + 1)

    Args:
        height_map (List[List[int]]): A 2-dimensional integer list representing the input string

    Returns:
        int: The sum of all (minimum risk level + 1)
    """

    # Define the boundary limits of the provided map input
    row_limit = {-1, len(height_map)}
    col_limit = {-1, len(height_map[0])}

    local_min_count = 0

    # Iterate through each point in the height map
    for row, line in enumerate(height_map):
        for col, num in enumerate(line):
            local_nums = []

            # Add the current point and all adjacent points to a temporary list
            for adj in [
                [row, col],
                [row - 1, col],
                [row + 1, col],
                [row, col - 1],
                [row, col + 1],
            ]:

                # Ensure that the coordinates for the adjacent points do not fall outside of the boundaries
                if adj[0] not in row_limit and adj[1] not in col_limit:
                    local_nums.append(height_map[adj[0]][adj[1]])

            # Return the minimum of the temporary list. Ensure that the list contains only one of the minimum value
            if num == min(local_nums) and local_nums.count(num) == 1:
                local_min_count += 1 + num

    return local_min_count


def get_basins(height_map: List[List[int]]) -> int:
    """
    Evalueates the given 2-Dimensional list for all basins. Basins are defined as submaps
    that are bounded by "9"

    Args:
        height_map (List[List[int]]): The given 2-Dimensional input

    Returns:
        int: The product of the three largest basin sizes
    """

    # Define the boudnary limits of the provided map
    row_limit = {-1, len(height_map)}
    col_limit = {-1, len(height_map[0])}

    # Initiate array to contain the size of all the basins
    basin_sizes = [0]

    """
    To find the size of each array, a queue/bfs will be used. Each point and its adjacent points will be evaluated to see if they are 
    within the boundaries of the basin. If they are, they will be added to the queue, and each point will be flipped to "-1" to 
    indicate that they have been visited already
        - '9' is the boundary of each basin, as specified in the problem.
        - '-1' will indicate that a point has been visited already
    """
    invalid_height = {-1, 9}

    # Iterate through every point in the map
    for row, line in enumerate(height_map):
        for col, num in enumerate(line):

            # If the point is not a basin boundary, and has not been visited already, do the following
            if height_map[row][col] not in invalid_height:
                basin_queue = []
                basin_queue.append([row, col])

                # All points in the basin will be in basin_queue at some point. Continue graph bfs while the queue is not empty
                while len(basin_queue) != 0:
                    coor = basin_queue.pop(0)
                    height_map[coor[0]][coor[1]] = -1
                    basin_sizes[-1] += 1

                    # Check all adjacent points to see if they are within the boundaries of the basin. If they are, add them to the queue
                    for adj in [
                        [coor[0], coor[1]],
                        [coor[0] - 1, coor[1]],
                        [coor[0] + 1, coor[1]],
                        [coor[0], coor[1] - 1],
                        [coor[0], coor[1] + 1],
                    ]:

                        # Check to see if the adjacent points falls outside of the boundary of the map
                        if adj[0] not in row_limit and adj[1] not in col_limit:

                            # Check if the adjacent points are the boundary, or if they have been visited already
                            if height_map[adj[0]][adj[1]] not in invalid_height:
                                height_map[adj[0]][adj[1]] = -1
                                basin_queue.append([adj[0], adj[1]])

                # We have finished evaluating the size of one basin. Append another item for another basin
                basin_sizes.append(0)

        basin_sizes.sort(reverse=True)
    return basin_sizes[0] * basin_sizes[1] * basin_sizes[2]


def main():
    height_map = get_input()
    print("Answer to Part 1:", get_min_risk_levels(height_map))
    print("Answer to Part 2:", get_basins(height_map=height_map))


if __name__ == "__main__":
    main()
