"""
__project__ = 'holoinsight-ai'
__file_name__ = 'node.py'
__author__ = 'LuYuan'
__time__ = '2023/4/11 17:36'
__info__ = 'Define the core class Node and implement functions for parent-child relationships, drilling down, copying,
            and matching nodes in an interval tree.'
"""


class Node:
    """
    Core class representing a node in an interval tree.
    """

    def __init__(self, level, left, right, parents=None):
        """
        Initialize a new Node with the given level, left endpoint, right endpoint, and parent nodes.

        :param level: The current level of the node.
        :param left: The left endpoint of the interval (closed interval).
        :param right: The right endpoint of the interval (closed interval).
        :param parents: A list of parent nodes, with the left parent at index 0 and the right parent at index -1.
                        Defaults to an empty list.
        """
        if parents is None:
            parents = []
        self.level = level
        self.left = left
        self.right = right
        self.parents = parents

    def add_parent(self, parent_node):
        """
        Add a parent node to the node's list of parent nodes if the parent node fully contains the current node.

        :param parent_node: The parent node to add.
        :return: None.
        """
        if self.left <= parent_node.left and self.right >= parent_node.right:
            self.parents.append(parent_node)

    def drill_down_to_node(self, direction):
        """
        Drill down from the current node to the node in the specified direction.

        :param direction: The direction to drill down, with direction=0 indicating the left direction and direction=-1
                          indicating the right direction.
        :return: The node in the specified direction.
        """
        current_node = self
        while current_node.parents:
            current_node = current_node.parents[direction]
        return current_node

    def drill_down_to_level(self, direction):
        """
        Drill down from the current node to the level in the specified direction.

        :param direction: The direction to drill down, with direction=0 indicating the left direction and direction=-1
        indicating the right direction.
        :return: The level in the specified direction.
        """

        def get_endpoint(node, direction):
            if direction == 0:
                return node.left
            else:
                return node.right

        ts = []
        current_node = self
        ts.append(get_endpoint(current_node, direction))
        while current_node.parents:
            current_node = current_node.parents[direction]
            ts.append(get_endpoint(current_node, direction))
        return ts

    def copy_node(self):
        """
        Create a copy of the current node.

        :return: A new Node object with the same level, left endpoint, and right endpoint as the original node.
        """
        new_node = Node(self.level, self.left, self.right)
        return new_node

    def matches_interval(self, ll, rr):
        """
        Check if the current node matches the given interval.

        :param ll: The left endpoint of the interval.
        :param rr: The right endpoint of the interval.
        :return: True if the current node's interval matches the given interval, False otherwise.
        """
        if self.left == ll and self.right == rr:
            return True
        return False


if __name__ == "__main__":
    pass
