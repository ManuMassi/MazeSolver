from maze import getReachablePaths
from tree import Node

from gui import drawTree, drawMaze, images_cleanup

# Name of the current file to save to visualize the tree / maze
filename = 0


def expand(maze, node):
    """
    Function that expands the node passed as argument
    :param maze: current maze
    :param node: node to expand
    :return: the list of successors of the node
    """

    # Get reachable states and paths from the node to expand
    states, paths = getReachablePaths(maze, node.data)

    ancestors = [ancestor.data for ancestor in node.ancestors]

    successors = []

    for i, state in enumerate(states):
        # Convert the reachable state to Node object
        successor = Node(state)

        # Check that is not in the same path
        if successor.data not in ancestors:
            node.add_children(successor)

            # Update path cost
            successor.path_cost += len(paths[i])

            successors.append(successor)

    return successors


def tree_search(maze, enqueue, max_depth=None, draw=True, analysis=False):
    """
    Generic function that find the solution of a maze using search trees
    :param analysis: boolean parameters that allows implementing analysis
    :param maze: maze to solve
    :param enqueue: functions to adds nodes to the fringe. It depends on the actual search algorithm used
    :param max_depth: maximum depth used in the iterative deepening depth first search
    :param draw: boolean parameter that allows to save images from each step
    :return: a list containing the solution if it founds one, False otherwise
    """
    # Remove all previous images
    images_cleanup()

    global filename
    filename = 0

    # Convert root and goal to Node object
    root = Node(maze.start)
    goal = Node(maze.end)

    # Initialize fringe and expanded
    fringe = [root]
    expanded = []

    if analysis:
        generated_nodes = 0

    if draw:
        drawMaze(maze, filename)
        drawTree(fringe, selected_node=root, filename=str(filename))
        filename += 1

    while len(fringe) > 0:
        # Remove first state from the fringe
        node = fringe.pop(0)

        # This will be true only in the iterative deepening depth first search
        if max_depth:
            curr_depth = len(node.ancestors)

            # Max depth reached
            if curr_depth > max_depth:
                continue

        # Goal node selected
        if node.data == goal.data:
            expanded.append(node)

            # Revert the ancestors list of the goal node to get the solution
            solution = node.ancestors.copy()[::-1]
            solution.append(goal)

            maze.solutions = solution

            if draw:
                # Save images
                drawMaze(maze, filename, solution=True, stateSpace=True)
                drawTree(expanded, node, str(filename), goal=True)

            if analysis:
                generated_nodes = len(expanded) + len(fringe)

                return solution, generated_nodes, node.path_cost
            else:
                return solution
        else:
            # Expand the node
            successors = expand(maze, node)
            expanded.append(node)

            # Add the successors to the fringe (it depends on the algorithm)
            enqueue(successors, fringe)

            if draw:
                # Save images
                drawMaze(maze, filename, stateSpace=True, node=node)
                drawTree(expanded, node, str(filename))

            # Prune the tree in the case of the iterative deepening depth first search
            if max_depth:
                if (curr_depth == max_depth) or len(node.children) == 0:
                    _prune(node, expanded, maze, draw)

        filename += 1

    # If it exits the while loop, it did not found the solution
    return False


def _prune(node, expanded, maze, draw=True):
    """
    Function that prune the node passed as parameter
    :param node: node to prune
    :param expanded: list of expanded nodes
    :param maze: maze to solve
    """
    global filename

    if draw:
        filename += 1
        # Save images
        drawTree(expanded, node, str(filename), prune=True)
        drawMaze(maze, filename, stateSpace=True, node=node)

    if node in expanded:
        expanded.remove(node)

    # If the node has a father
    if len(node.ancestors) > 0:
        # Remove the node from the father's children list
        node.ancestors[0].children.remove(node)

        # Prune recursively its parent if it hasn't any other children
        if len(node.ancestors[0].children) == 0:
            _prune(node.ancestors[0], expanded, maze, draw)

        node.ancestors = []


def breadth_first_search(maze, draw=True, analysis=False):
    """
    Implementation of the breadth first search algorithm for maze pathfinding
    :param maze: the maze to solve
    :param draw: boolean parameter that allows to save images of the maze step by step (it increase time complexity)
    :param analysis: boolean parameter that allows to return more information about the algorithm
    :return: the solution and, if analysis is true, also the number of generated notes and the path cost
    """

    # The bfs algorithm add the new nodes to the end of the fringe (fifo)
    def enqueue(nodes, fringe):
        for node in nodes:
            fringe.append(node)

    return tree_search(maze, enqueue, draw=draw, analysis=analysis)


def uniform_cost_search(maze, draw=True, analysis=False):
    """
    Implementation of the uniform cost search algorithm for maze pathfinding
    :param maze: the maze to solve
    :param draw: boolean parameter that allows to save images of the maze step by step (it increase time complexity)
    :param analysis: boolean parameter that allows to return more information about the algorithm
    :return: the solution and, if analysis is true, also the number of generated notes and the path cost
    """

    # The ucs algorithm choose to expand the node with the minimum path cost.
    # Since the tree_search takes always the first node from the fringe, it sorts the fringe by path cost
    def enqueue(nodes, fringe):
        fringe.extend(nodes)
        fringe.sort(key=lambda node: node.path_cost)

    return tree_search(maze, enqueue, draw=draw, analysis=analysis)


def A_star_search(maze, draw=True, analysis=False):
    """
    Implementation of the A* search algorithm for maze pathfinding
    :param maze: the maze to solve
    :param draw: boolean parameter that allows to save images of the maze step by step (it increase time complexity)
    :param analysis: boolean parameter that allows to return more information about the algorithm
    :return: the solution and, if analysis is true, also the number of generated notes and the path cost
    """

    # Heuristic function defined for each node
    def heuristic(node, goal):
        return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

    # The A* algorithm expands the node with the minimum value of [g(n) + h(n)], so it sorts the fringe by this value
    def enqueue(nodes, fringe):
        fringe.extend(nodes)
        fringe.sort(key=lambda node: node.path_cost + heuristic(node.data, maze.end))

    return tree_search(maze, enqueue, draw=draw, analysis=analysis)


def iterative_deepening_depth_first_search(maze, draw=True, analysis=False):
    """
    Implementation of the iterative deepening depth first search algorithm for maze pathfinding.
    :param maze: the maze to solve
    :param draw: boolean parameter that allows to save images of the maze step by step (it increase time complexity)
    :param analysis: boolean parameter that allows to return more information about the algorithm
    :return: the solution and, if analysis is true, also the number of generated notes and the path cost
    """

    # The depth first search expands the last node found, so it adds the new nodes in the head of the fringe
    def enqueue(nodes, fringe):
        for node in nodes:
            fringe.insert(0, node)

    max_depth = 1

    solution = False
    # Until it does not find a solution, it increases the max_depth
    while not solution:
        solution = tree_search(maze, enqueue, max_depth, draw=draw, analysis=analysis)

        max_depth += 1

    return solution
