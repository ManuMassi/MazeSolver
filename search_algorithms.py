from maze import MazeManager, SquareType
from tree import Node
from mazelib.solve.BacktrackingSolver import BacktrackingSolver
from gui import drawTree


def expand(maze, node):
    states, paths = MazeManager.getReachablePaths(maze, node.data)

    ancestors = [ancestor.data for ancestor in node.ancestors]

    nodes = [Node(state) for state in states if state not in ancestors]

    for i, state in enumerate(nodes):
        node.add_children(state)
        state.path_cost += len(paths[i])

    return nodes


def tree_search(maze, start_state, goal_state, enqueue, max_depth=None):

    expanded = []
    root = Node(start_state)
    goal = Node(goal_state)

    fringe = [root]

    while len(fringe) > 0:

        node = fringe.pop(0)

        if max_depth and len(node.ancestors) > max_depth - 1:
            continue

        if node.data == goal.data:
            solution = node.ancestors.copy()[::-1]
            solution.append(goal)

            drawTree(expanded)

            maze.solutions = solution
            return solution
        else:
            if max_depth and max_depth != 1 and len(node.ancestors) == max_depth - 1:
                node.ancestors[0].children.remove(node)
                node.ancestors.clear()

            else:
                successors = expand(maze, node)
                expanded.append(node)

                enqueue(successors, fringe)
    drawTree(expanded)
    return False


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
        manager = MazeManager(10, 10)
        manager.drawMaze(manager.maze, stateSpace=True)

        # ucs = uniform_cost_search(manager.maze, manager.maze.start, manager.maze.end)
        # A_s = A_star_search(manager.maze, manager.maze.start, manager.maze.end)
        # bfs = breadth_first_search(manager.maze, manager.maze.start, manager.maze.end)
        dps = iterative_deepening_depth_first_search(manager.maze, manager.maze.start, manager.maze.end)

        print("culetto", dps)
"""

"""