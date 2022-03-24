from maze import MazeManager, SquareType
from tree import Node
from mazelib.solve.BacktrackingSolver import BacktrackingSolver
from gui import drawTree


def expand(maze, node):
    states = MazeManager.getReachableStates(maze, node.data)
    # states = MazeManager.getAdjacentSquares(maze, node.data, SquareType.ROOM)

    ancestors = [ancestor.data for ancestor in node.ancestors]

    nodes = [Node(state) for state in states if state not in ancestors]

    return nodes


def tree_search(maze, start_state, goal_state, enqueue):

    expanded = []
    root = Node(start_state)
    goal = Node(goal_state)

    fringe = [root]

    while len(fringe) > 0:

        node = fringe.pop(0)

        # tree.node(str(node.id), str(node.data))

        if node.data == goal.data:
            solution = node.ancestors.copy()[::-1]
            # solution.append(goal)
            print(node.path_cost)

            drawTree(expanded)

            maze.solutions = solution
            return solution
        else:
            successors = expand(maze, node)
            expanded.append(node)

            for successor in successors:
                node.add_children(successor)
                # successor.path_cost += len(MazeManager.getPath(maze, node.data, successor.data))

            enqueue(successors, fringe)
        # print(node, ':', node.path_cost)
    return False


def breadth_first_search(maze, start_state, goal_state):
    def enqueue(nodes, fringe):
        # fringe.extend(nodes)
        for node in nodes:
            fringe.append(node)

    return tree_search(maze, start_state, goal_state, enqueue)


if __name__ == '__main__':
    for i in range(1):
        manager = MazeManager(10, 10)
        # manager.drawMaze(manager.maze, stateSpace=True)

        print(breadth_first_search(manager.maze, manager.maze.start, manager.maze.end))
        manager.drawMaze(manager.maze, solution=True, stateSpace=True)