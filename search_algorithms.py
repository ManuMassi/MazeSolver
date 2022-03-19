from maze import MazeManager
from tree import Node
import graphviz
import random


def expand(maze, node):
    states = MazeManager.getReachableStates(maze, node.data)
    # nodes = [Node(state) for state in states if Node(state) not in node.ancestors]

    ancestors = []
    for a in node.ancestors:
        ancestors.append(a.data)

    nodes = [Node(state) for state in states if state not in ancestors]


    return nodes


def tree_search(maze, start_state, goal_state, state_space, enqueue):
    albero = graphviz.Digraph('tree', format='png')

    root = Node(start_state)
    goal = Node(goal_state)

    fringe = [root]
    expanded = []
    tree = root

    i = 0
    while len(fringe) > 0:

        node = fringe.pop(0)

        albero.node(str(node.id), str(node.data))

        if node.data == goal.data:
            solution = node.ancestors.copy()[::-1]
            solution.append(goal)
            expanded.append(goal)
            print(len(expanded))

            albero.render(directory='.', view=False)

            return solution
        else:
            successors = expand(maze, node)
            node.add_children_list(successors)

            for child in successors:
                albero.node(str(child.id), str(child.data))
                albero.edge(str(node.id), str(child.id), constraint='true')

            enqueue(successors, fringe)

            expanded.append(node)  # Mark node as expanded

            i += 1
    return False


def breadth_first_search(maze, start_state, goal_state):
    def enqueue(nodes, fringe):
        # fringe.extend(nodes)
        for node in nodes:
            fringe.append(node)

    return tree_search(maze, start_state, goal_state, MazeManager.defineStateSpace(maze), enqueue)


if __name__ == '__main__':
    manager = MazeManager(10, 10)
    # manager.drawMaze(manager.maze, stateSpace=True)

    # print(len(manager.defineStateSpace(manager.maze)))
    print(breadth_first_search(manager.maze, manager.maze.start, manager.maze.end))
