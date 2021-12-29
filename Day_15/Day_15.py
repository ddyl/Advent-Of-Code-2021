from collections import namedtuple
from sys import maxsize


def get_input() -> list[list[int]]:
    """
    Get the input data and return it as a nested integer list.
    A better data structure could have been used here. I consulted other solutions online after finishing this one, and saw
    many approaches using dictionaries instead of a list. A dictionary would have been a better choice, as I use Dijkstra's algorithm,
    and with dictionaries finding neighbours is less complicated (as I would not need to worry about coordinates falling out of bounds)

    Returns:
        [type]: list[list[int]]
    """
    return [
        [int(num) for num in line.strip()]
        for line in open("Day_15_input.txt").readlines()
    ]


def find_shortest_cost(graph: list[list[int]]) -> int:
    """
    Finds the shortest cost for any path from the source node (top left) to the destination node (bottom right).
    As mentioned in the documentation for get_input(), a better data structure to represent the map would have been a dictionary.
    Also, rather than using a set to represent candidate nodes, a better data structure would have been to use a heap queue.
    Using a dictionary and heap queue would have reduced the runtime of this function. Currently, Part 2 executes in around 30 seconds

    Args:
        graph (list[list[int]]): The map given in the input data

    Returns:
        int: The lowest cost path from the source to destination points
    """
    # A namedtuple to make points easier to access
    Point = namedtuple("Point", ["row", "col"])

    # An initial array of distances that is the same size as the graph in the input data. Required for Dijkstra's algorithm
    distances = [[maxsize] * len(graph[0]) for i in range(0, len(graph))]

    # Set the start node
    distances[0][0] = 0

    # A set of nodes to visit. Required for Dijkstra's algorithm
    to_visit = {Point(row=0, col=0)}
    # The set of nodes already visited. Required for Dijkstra's algorithm
    visited = set()

    while len(to_visit) != 0:
        # Find point in to_visit with the smallest distance
        min_dist = maxsize
        point = None
        for candidate_point in to_visit:
            if distances[candidate_point.row][candidate_point.col] <= min_dist:
                min_dist = distances[candidate_point.row][candidate_point.col]
                point = candidate_point
        to_visit.remove(point)
        visited.add(point)

        # If there are still neighbours to visit, populate them into the to_visit set,
        # as long as they are within the bounds of the graph and haven't been visited already
        neighbours = set()
        for row in [point.row - 1, point.row + 1]:
            if row not in (-1, len(distances)):
                neighbours.add(Point(row=row, col=point.col))
        for col in [point.col - 1, point.col + 1]:
            if col not in (-1, len(distances[0])):
                neighbours.add(Point(row=point.row, col=col))
        for neighbour in neighbours:
            if neighbour not in visited:
                to_visit.add(neighbour)

        # Calculate the new distance values for each neighbouring node
        for neighbour in neighbours:
            new_dist = (
                distances[point.row][point.col] + graph[neighbour.row][neighbour.col]
            )
            if new_dist < distances[neighbour.row][neighbour.col]:
                distances[neighbour.row][neighbour.col] = new_dist

    return distances[len(distances) - 1][len(distances[0]) - 1]


def extend_map(graph: list[list[int]], repeat: int) -> list[list[int]]:
    """
    Extends the map given in the original input.

    Args:
        graph (list[list[int]]): The original map given in the input data
        repeat (int): The number of times to repeat the map. If a map is replicated 5 times, 25 "tiles" of the original map is created.

    Returns:
        list[list[int]]: The extended map
    """

    height = len(graph)
    width = len(graph[0])

    for iter in range(0, repeat - 1):
        for row in graph:
            for i in range(0, width):
                increased = row[iter * width + i] + 1
                if increased < 10:
                    row.append(increased)
                else:
                    row.append(1)

    for iter in range(0, repeat - 1):
        for i in range(0, height):
            graph.append(graph[iter * height + i][:])
            for j, num in enumerate(graph[-1]):
                num += 1
                if num >= 10:
                    num = 1
                graph[-1][j] = num

    return graph


def main():
    graph = get_input()
    print("Answer to Part 1:", find_shortest_cost(graph))

    extended_graph = extend_map(graph, 5)
    print("Answer to Part 2:", find_shortest_cost(extended_graph))


if __name__ == "__main__":
    main()
