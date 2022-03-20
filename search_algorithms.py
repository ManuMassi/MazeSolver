from maze import MazeManager
from tree import Node
import graphviz


def expand(maze, node):
    states = MazeManager.getReachableStates(maze, node.data)

    ancestors = [ancestor.data for ancestor in node.ancestors]

    nodes = [Node(state) for state in states if state not in ancestors]

    return nodes


def tree_search(maze, start_state, goal_state, enqueue):
    tree = graphviz.Digraph('tree', format='png')

    root = Node(start_state)
    goal = Node(goal_state)

    fringe = [root]

    while len(fringe) > 0:

        node = fringe.pop(0)

        tree.node(str(node.id), str(node.data))

        if node.data == goal.data:
            solution = node.ancestors.copy()[::-1]
            solution.append(goal)

            tree.render(directory='.', view=False)

            maze.solutions = solution
            return solution
        else:
            successors = expand(maze, node)
            node.add_children_list(successors)

            for child in successors:
                tree.node(str(child.id), str(child.data))
                tree.edge(str(node.id), str(child.id), constraint='true')

            enqueue(successors, fringe)

    return False


def breadth_first_search(maze, start_state, goal_state):
    def enqueue(nodes, fringe):
        # fringe.extend(nodes)
        for node in nodes:
            fringe.append(node)

    return tree_search(maze, start_state, goal_state, enqueue)


if __name__ == '__main__':
    manager = MazeManager(10, 10)

    print(breadth_first_search(manager.maze, manager.maze.start, manager.maze.end))
    manager.drawMaze(manager.maze, solution=True, stateSpace=True)
