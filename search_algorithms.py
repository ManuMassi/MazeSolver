from maze import MazeManager, SquareType
from tree import Node
from gui import drawTree
import os

filename = 0


def expand(maze, node):
    states, paths = MazeManager.getReachablePaths(maze, node.data)

    ancestors = [ancestor.data for ancestor in node.ancestors]

    successors = []

    for i, state in enumerate(states):
        successor = Node(state)
        if successor.data not in ancestors:
            node.add_children(successor)

            successor.path_cost += len(paths[i])

            successors.append(successor)

    return successors


def tree_search(maze, start_state, goal_state, enqueue, max_depth=None):
    try:
        for file in os.listdir('./temp'):
                os.remove('./temp/' + file)
    except FileNotFoundError:
        pass

    global filename

    expanded = []
    root = Node(start_state)
    goal = Node(goal_state)

    fringe = [root]

    filename = 0

    while len(fringe) > 0:

        node = fringe.pop(0)

        if max_depth:
            curr_depth = len(node.ancestors)
            if curr_depth > max_depth:
                continue

        if node.data == goal.data:
            expanded.append(node)

            solution = node.ancestors.copy()[::-1]
            solution.append(goal)

            drawTree(expanded, node, "./temp/", str(filename), goal=True)
            # drawTree(expanded, node, './', 'tree', goal=True)

            maze.solutions = solution
            return solution
        else:
            successors = expand(maze, node)
            expanded.append(node)

            enqueue(successors, fringe)

            if max_depth:
                if (curr_depth == max_depth) or len(node.children) == 0:
                    _prune(node, expanded)

            drawTree(expanded, node, "./temp/", str(filename))
        filename += 1

    return False


def _prune(node, expanded):
    global filename

    drawTree(expanded, node, "./temp/", str(filename), prune=True)
    filename += 1

    if node in expanded:
        expanded.remove(node)

    if len(node.ancestors) > 0:
        node.ancestors[0].children.remove(node)

        if len(node.ancestors[0].children) == 0:
            _prune(node.ancestors[0], expanded)

        node.ancestors = []


def breadth_first_search(maze, start_state, goal_state):
    def enqueue(nodes, fringe):
        for node in nodes:
            fringe.append(node)

    return tree_search(maze, start_state, goal_state, enqueue)


def uniform_cost_search(maze, start_state, goal_state):
    def enqueue(nodes, fringe):
        fringe.extend(nodes)
        fringe.sort(key=lambda node: node.path_cost)

    return tree_search(maze, start_state, goal_state, enqueue)


def A_star_search(maze, start_state, goal_state):
    def heuristic(node, goal):
        return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

    def enqueue(nodes, fringe):
        fringe.extend(nodes)
        fringe.sort(key=lambda node: node.path_cost + heuristic(node.data, goal_state))

    return tree_search(maze, start_state, goal_state, enqueue)


def iterative_deepening_depth_first_search(maze, start_state, goal_state):
    def enqueue(nodes, fringe):
        for node in nodes:
            fringe.insert(0, node)

    max_depth = 1
    solution = False
    while not solution:
        solution = tree_search(maze, start_state, goal_state, enqueue, max_depth)
        max_depth += 1

    return solution


if __name__ == '__main__':
    for i in range(1):
        manager = MazeManager(5, 5)
        manager.drawMaze(manager.maze, stateSpace=True)

        # ucs = uniform_cost_search(manager.maze, manager.maze.start, manager.maze.end)
        # A_s = A_star_search(manager.maze, manager.maze.start, manager.maze.end)
        # dps = breadth_first_search(manager.maze, manager.maze.start, manager.maze.end)
        dps = iterative_deepening_depth_first_search(manager.maze, manager.maze.start, manager.maze.end)

        print("bread", dps)
