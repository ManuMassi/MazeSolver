
class Node:
    def __init__(self, data):
        self.data = data
        self.children = []
        self.ancestors = []

    def add_children(self, node):
        if type(node) is not Node:
            raise TypeError("You must add a node type (Node(data))")

        self.children.append(node)
        node._add_ancestor(self)

    def add_children_list(self, nodes):
        for node in nodes:
            self.add_children(node)

    def _add_ancestor(self, node):
        if type(node) is not Node:
            raise TypeError("You must add a node type (Node(data))")

        self.ancestors.append(node)

    def __eq__(self, other):
        if type(other) is not Node:
            raise TypeError("You must add a node type")

        return self.data == other.data

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return self.__str__()


class Tree:
    def __init__(self, root):
        if type(root) is not Node:
            raise TypeError("You must add a node type (Node(data))")

        self.root = root