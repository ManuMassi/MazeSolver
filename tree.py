class Node:
    """
    Class that allows to save all data relative to a node
    """

    def __init__(self, data):
        self.data = data
        self.children = []
        self.ancestors = []
        self.path_cost = 0

        self.id = id(self)  # Unique id to identify the node

    def add_children(self, node):
        """
        Method that allows to add a node in the children list
        :type node: Node
        :param node: the child node to add
        """
        if type(node) is not Node:
            raise TypeError("You must add a node type: (Node(data))")

        self.children.append(node)
        node._add_ancestor(self)  # Adds this node to the ancestors of the child

        for ancestor in self.ancestors:
            node._add_ancestor(ancestor)

    def _add_ancestor(self, node):
        """
        Method to add a node in the ancestors list of another node
        :param node: the ancestor
        """
        if type(node) is not Node:
            raise TypeError("You must add a node type (Node(data))")

        self.ancestors.append(node)

        # If it's the first ancestor added, it means it's the node's father, so it must inherit its path cost
        if len(self.ancestors) == 1:
            self.path_cost = self.ancestors[0].path_cost

    def __eq__(self, other):
        if type(other) is not Node:
            raise TypeError("You must add a node type")

        return self.data == other.data and self.ancestors == other.ancestors and \
            self.children == other.children and self.id == other.id

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return self.__str__()
