from collections import defaultdict
from typing import DefaultDict, List


def get_input() -> DefaultDict[str, List[str]]:
    """
    Reads the input data from a file and returns it in the form of a DefaultDict.
    The problem specificies that this is not to be an directed graph, so distinguishing parents from children is not necessary.

    Returns:
        DefaultDict[str, List[str]]: A DefaultDict, where the key is the node, and the value is the list of connected nodes
    """
    cave_mappings = defaultdict(list)
    for line in open("Day_12_input.txt").readlines():
        cave_pair = line.strip().split("-")
        cave_mappings[cave_pair[0]].append(cave_pair[1])
        cave_mappings[cave_pair[1]].append(cave_pair[0])
    return cave_mappings


def find_paths(
    mappings: DefaultDict[str, List[str]],
    current: List[str],
    all_paths: List[str],
    node_name: str,
    visited: set[str],
):
    """
    Recursive function to find all paths from the start cave to the end cave.

    Args:
        mappings (DefaultDict[str, List[str]]): The mapping of all caves (the input data)
        current (List[str]): The current path taken so far
        all_paths (List[str]): All paths that lead from start to end
        node_name (str): The current node's name
        visited (set[str]): The smaller caves (lowercase nodes) that have been visited already
    """

    # Append the current node to the current path, copy the visited set, and if the name is lowercase add it to the "visited" set
    current.append(node_name)
    visited = set(visited)
    if node_name.islower():
        visited.add(node_name)

    # If the current node is "end", then append the node to the current path, add it to all_paths, and exit the function
    if node_name == "end":
        all_paths.append(current[:])
        return

    # For each connected node, if the node has not been visited yet then visit the node recursively. Do not visit the "start" node again
    for adj in mappings[node_name]:
        if adj == "start":
            continue
        elif adj not in visited:
            find_paths(
                mappings=mappings,
                current=current[:],
                all_paths=all_paths,
                visited=visited,
                node_name=adj,
            )


def find_paths_part_2(
    mappings: DefaultDict[str, List[str]],
    current: List[str],
    all_paths: List[str],
    node_name: str,
    visited: set(),
    visited_twice: bool,
):
    """
    This function serves the same purpose as find_paths, but implements the modified problem in part 2.
    The modification states that a single cave may be visited twice for each trip

    Args:
        mappings (DefaultDict[str, List[str]]): The mapping of all caves (the input data)
        current (List[str]): The current path taken so far
        all_paths (List[str]): All paths that lead from start to end
        node_name (str): The current node's name
        visited (set[str]): The smaller caves (lowercase nodes) that have been visited already
        visited_twice (bool): An indicator to determine if a small cave has been visited twice in the current path
    """

    # Append the current node to the current path, copy the visited set, and if the name is lowercase add it to the "visited" set
    current.append(node_name)
    visited = set(visited)
    if node_name.islower():
        visited.add(node_name)

    # If the current node is "end", then append the node to the current path, add it to all_paths, and exit the function
    if node_name == "end":
        all_paths.append(current[:])
        return

    # For each connected node, if the node has not been visited yet then visit the node recursively. Do not visit the "start" node again
    for adj in mappings[node_name]:
        if adj == "start":
            continue
        elif adj not in visited:
            find_paths_part_2(
                mappings=mappings,
                current=current[:],
                all_paths=all_paths,
                visited=visited,
                node_name=adj,
                visited_twice=visited_twice,
            )
        # If a small cave has been visited once (has a lowercase name), and no other small cave has been visited twice,
        # visit the current small cave for a second time
        elif adj in visited and visited_twice == False:
            find_paths_part_2(
                mappings=mappings,
                current=current[:],
                all_paths=all_paths,
                visited=visited,
                node_name=adj,
                visited_twice=True,
            )


def find_all_paths(
    cave_mappings: DefaultDict[str, List[str]], visit_small_cave_twice: bool = False
) -> List[List[str]]:
    """
    Returns a list of all paths in a given cave system (the problem input)

    Args:
        cave_mappings (DefaultDict[str, List[str]]): The problem input organized in a DefaultDict, where the key is a cave and the value is the list of connected nodes
        visit_small_cave_twice (bool, optional): Specify if a small cave can be visited twice. Is required for Part 2 of the problem. Defaults to False.

    Returns:
        List[List[str]]: Returns a list of paths, where each path is a list of strings
    """

    if not visit_small_cave_twice:
        all_paths = []
        find_paths(
            mappings=cave_mappings,
            current=[],
            all_paths=all_paths,
            visited=set(),
            node_name="start",
        )
    else:
        all_paths = []
        find_paths_part_2(
            mappings=cave_mappings,
            current=[],
            all_paths=all_paths,
            visited=set(),
            node_name="start",
            visited_twice=False,
        )
    return all_paths


def main():
    cave_mappings = get_input()
    all_paths = find_all_paths(cave_mappings=cave_mappings)
    print("Answer to Part 1:", len(all_paths))
    all_paths = find_all_paths(cave_mappings=cave_mappings, visit_small_cave_twice=True)
    print("Answer to Part 2:", len(all_paths))


if __name__ == "__main__":
    main()
