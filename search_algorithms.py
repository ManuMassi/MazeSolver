from maze import MazeManager


def expand(maze, node, expanded):

    nodes = MazeManager.getReachableStates(maze, node)
    nodes = [node for node in nodes if node not in expanded]
    return nodes


def tree_search(maze, start_state, goal_state, state_space, enqueue):
    fringe = [start_state]
    expanded = []

    while len(fringe) > 0:
        node = fringe.pop(0)
        print(node)

        if node not in expanded:
            if node == goal_state:
                return True
            else:
                enqueue(expand(maze, node, expanded), fringe)
                # Mark as expanded
                expanded.append(node)

    return False


def breadth_first_search(maze, start_state, goal_state):
    def enqueue(nodes, fringe):
        # fringe.extend(nodes)
        for node in nodes:
            if node not in fringe:
                fringe.append(node)

    return tree_search(maze, start_state, goal_state, MazeManager.defineStateSpace(maze), enqueue)




manager = MazeManager(10, 10)
manager.drawMaze(manager.maze, stateSpace=True)

print(len(manager.defineStateSpace(manager.maze)))
print(breadth_first_search(manager.maze, manager.maze.start, manager.maze.end))
