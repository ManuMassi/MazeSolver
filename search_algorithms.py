from maze import MazeManager
from tree import Node
import graphviz
import random


def expand(maze, node):
    states = MazeManager.getReachableStates(maze, node.data)
    nodes = [Node(state) for state in states if Node(state) not in node.ancestors]
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

        albero.node(str(node.data) + str(i))

        if node == goal:
            print(goal.ancestors)
            albero.render(directory='.', view=False)
            return True
        else:
            successors = expand(maze, node)
            node.add_children_list(successors)

            for child in successors:
                albero.edge(str(node.data) + str(i), str(child.data) + str(i), constraint='true')

            enqueue(successors, fringe)

            expanded.append(node)  # Mark node as expanded

            # print(node, ':', node.children)
            i += 1
    return False


def breadth_first_search(maze, start_state, goal_state):
    def enqueue(nodes, fringe):
        # fringe.extend(nodes)
        for node in nodes:
            if node not in fringe:
                fringe.append(node)

    return tree_search(maze, start_state, goal_state, MazeManager.defineStateSpace(maze), enqueue)


if __name__ == '__main__':
    manager = MazeManager(10, 10)
    # manager.drawMaze(manager.maze, stateSpace=True)

    print(len(manager.defineStateSpace(manager.maze)))
    print(breadth_first_search(manager.maze, manager.maze.start, manager.maze.end))
