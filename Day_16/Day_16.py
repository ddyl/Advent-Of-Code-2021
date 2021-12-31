from collections import namedtuple


class TreeNode:
    def __init__(self):
        self.version = None
        self.type = None
        self.value = None
        self.children = []
        self.parents = []


def get_input() -> str:
    return open("Day_16_input.txt").readline().strip()


def unpack(packet_str: str) -> TreeNode:
    """
    This function steps through the provided hex value of the packets and constructs a tree to represent the structure of the
    packets. The root of the tree is returned.

    Args:
        packet_str (str): The hexadecimal value of the packets (the puzzle input)

    Returns:
        TreeNode: The root of the tree
    """
    packet_bin = format(int(packet_str, 16), "0" + str(len(packet_str * 4)) + "b")
    root = unpack_all_packets(packet_bin=packet_bin)[0]
    return root


def unpack_all_packets(packet_bin: str, node: TreeNode = None) -> tuple[TreeNode, str]:
    """
    Recursively steps through the binary representation of the input's hex values.
    This function creates a tree of the packets that the binary values represent, and returns the root node and the remaining packet string

    Args:
        packet_str (str): The binary value of the input's hex values
        node (TreeNode, optional): A TreeNode instance. Defaults to None.

    Returns:
        tuple[TreeNode, str]: The root node of the tree and the remaining packet string
    """

    # If no node is supplied, create a new TreeNode
    if node is None:
        node = TreeNode()

    # Parse through the binary string and get the version and type of the packet
    node.version = int(packet_bin[:3], 2)
    node.type = int(packet_bin[3:6], 2)

    # Packet type 4 indicates a packet containing the literal value
    if node.type == 4:
        # Compile the literal value form the remaining string, and assign it to the node value
        node.value, packet_bin = unpack_literal(packet_bin=packet_bin[6:])
        return node, packet_bin

    # Every other packet type indicates an operator packet
    else:
        operator_type = packet_bin[6]

        # If the operator packet type is 0, the next 15 bits indicate the number of bits the sub packets take up
        # Any number of packets may be present within those bits
        if operator_type == "0":

            # Get the number of bits the subpackets take up
            subpacket_len = int(packet_bin[7 : 7 + 15], 2)
            packet_bin = packet_bin[7 + 15 :]
            suppacket_len = len(packet_bin)

            # While the returned packet's length + subpacket != the length of the superpacket, recursively call the current function
            while subpacket_len + len(packet_bin) > suppacket_len:
                child_node, packet_bin = unpack_all_packets(packet_bin, TreeNode())
                node.children.append(child_node)
                child_node.parents.append(node)

        # If the operator packet type is 1, the next 11 bits indicate the number of packets included in the remaining packet bits
        elif operator_type == "1":

            # Get the number of subpackets contained within this packet
            subpacket_count = int(packet_bin[7 : 7 + 11], 2)
            packet_bin = packet_bin[7 + 11 :]

            # Call the current function for each subpacket residing in the remaining bits
            for i in range(0, subpacket_count):
                child_node, packet_bin = unpack_all_packets(packet_bin, TreeNode())
                node.children.append(child_node)
                child_node.parents.append(node)

    return node, packet_bin


def unpack_literal(packet_bin: str) -> tuple[int, str]:
    """
    Extracts the literal value of the packet based on the problem specifications, and returns the value and the reamining packet string.
    The problem states that the literal value should be unpacked the following way:
        5 bits should be considered at a time. If the first bit is 1, the remaining 4 is added to the value.
        This continues until the first bit is 0.
        Ex. "10100100001111100001" -> "10100 10000 11111 00001" -> "0100 0000 1111 0001" -> "0100000011110001"

    Args:
        packet_str (str): The packet string to decode

    Returns:
        tuple[int, str]: The literal value, and the reamining packet string
    """

    bin_num = ""

    index = 0
    while packet_bin[index] != "0":
        bin_num += packet_bin[index + 1 : index + 5]
        index += 5

    bin_num += packet_bin[index + 1 : index + 5]

    return int(bin_num, 2), packet_bin[index + 5 :]


def get_version_sum(root: TreeNode) -> int:
    """
    Does a Breadth-First-Search (BFS) through the packet tree and returns the sum of all the packet's versions.

    Args:
        root (TreeNode): The root node of the packet tree

    Returns:
        int: The sum of all the packet versions
    """
    nodes = [root]
    version_sum = 0
    while len(nodes) > 0:
        node = nodes.pop()
        for child_node in node.children:
            nodes.append(child_node)
        version_sum += node.version
    return version_sum


def do_packet_instructions(node: TreeNode) -> int:
    """
    For each packet type, Part 2 gave a mathematical operation to do for each node. This function does a Depth-First-Search (DFS) and
    does the mathematical operation for each node in the tree. The value at the root of the tree is returned.

    Args:
        node (TreeNode): The root of the tree

    Returns:
        int: The resulting value at the root node of the tree after all mathematical operations have been completed
    """

    if len(node.children) > 0:
        for child in node.children:
            do_packet_instructions(child)

    # Get the sum of all child nodes. Get the value of the child node if there is only one child node
    if node.type == 0:
        node.value = 0
        for child in node.children:
            node.value += child.value
    # Get the product of all child nodes. Get the value of the child node if there is only one child node
    elif node.type == 1:
        node.value = 1
        for child in node.children:
            node.value *= child.value
    # Get the minimum value of all the child nodes
    elif node.type == 2:
        node.value = node.children[0].value
        for child in node.children:
            node.value = min([node.value, child.value])
    # Get the maximum value of all the child nodes
    elif node.type == 3:
        node.value = node.children[0].value
        for child in node.children:
            node.value = max([node.value, child.value])
    # Return 1 if the first child node's value is greater than the second, 0 if not
    elif node.type == 5:
        if node.children[0].value > node.children[1].value:
            node.value = 1
        else:
            node.value = 0
    # Return 1 if the first child node's value is less than the second, 0 if not
    elif node.type == 6:
        if node.children[0].value < node.children[1].value:
            node.value = 1
        else:
            node.value = 0
    # Return 1 if the two child values are equal to each other, 0 if not
    elif node.type == 7:
        if node.children[0].value == node.children[1].value:
            node.value = 1
        else:
            node.value = 0

    return node.value


def main():
    packet = get_input()
    root = unpack(packet_str=packet)
    print("Answer to Part 1:", get_version_sum(root=root))
    print("Answer to Part 2:", do_packet_instructions(node=root))


if __name__ == "__main__":
    main()
