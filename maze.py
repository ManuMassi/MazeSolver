from enum import Enum

from matplotlib import colors
from mazelib import Maze
from mazelib.generate.AldousBroder import AldousBroder
from mazelib.solve.ShortestPaths import ShortestPaths
import matplotlib.pyplot as plt
import numpy as np
import random


class SquareType(Enum):
    ROOM = 0
    WALL = 1
    START = 2
    EXIT = 3
    SOLUTION = 4
    STATE = 5


class MazeManager:

    def __init__(self, height, width):
        self.maze = self.generateMaze(height, width)

    @staticmethod
    def generateMaze(height, width):
        maze = Maze(12345)
        maze.generator = AldousBroder(height, width)
        maze.generate()
        maze.generate_entrances()

        maze.start = MazeManager.getAdjacentSquares(maze, maze.start, SquareType.ROOM)[0]
        maze.end = MazeManager.getAdjacentSquares(maze, maze.end, SquareType.ROOM)[0]

        MazeManager.wallBreaker(maze)

        maze.state_space = MazeManager.defineStateSpace(maze)
        return maze

    @staticmethod
    def drawMaze(maze, solution=False, stateSpace=False):
        if type(maze) != Maze:
            raise TypeError("You must pass a maze to draw")

        # Temporary grid where the start and the end are set to 2 and 3
        grid = maze.grid.copy()

        if stateSpace:
            for y, x in maze.state_space:
                grid[y][x] = SquareType.STATE.value

        # if solution and maze.solutions:
        #     for i, state in enumerate(maze.solutions):
        #         grid[state.data[0]][state.data[1]] = SquareType.SOLUTION.value

        if solution and maze.solutions:
            for i, state in enumerate(maze.solutions):
                if i != len(maze.solutions) - 1:
                    path = MazeManager.getPath(maze, state.data, maze.solutions[i+1].data)
                    for room in path:
                        grid[room[0]][room[1]] = SquareType.SOLUTION.value

        grid[maze.start] = SquareType.START.value
        grid[maze.end] = SquareType.EXIT.value

        # Color map:
        # 0 -> white : empty spaces
        # 1 -> black : walls
        # 2 -> blue : start
        # 3 -> red : exit
        # 4 -> yellow : solution
        # 5 -> purple : state
        color_map = colors.ListedColormap(['white', 'black', 'blue', 'red', 'yellow', 'purple'])
        bounds = list(range(0, 7))  # [0, 1, 2, 3, 4, 5]
        norm = colors.BoundaryNorm(bounds, color_map.N)

        # Draw the maze
        fig, ax = plt.subplots()
        ax.imshow(grid, cmap=color_map, norm=norm)

        # Show grid
        plt.grid(which='major', axis='both')
        plt.xticks(np.arange(-0.5, grid.shape[1], 1))
        plt.yticks(np.arange(-0.5, grid.shape[0], 1))

        # Remove tick labels
        ax.set_yticklabels([])
        ax.set_xticklabels([])

        plt.show()

    @staticmethod
    def getAdjacentSquares(maze, square, squareType=SquareType.WALL):
        if type(squareType) is not SquareType:
            raise TypeError("You must pass a SquareType type")

        y = square[0]
        x = square[1]
        adjacent_squares = []

        for i in range(-1, 2, 2):  # [-1, 1]
            try:
                if maze.grid[y + i][x] == squareType.value and y + i >= 0:
                    adjacent_squares.append((y + i, x))
            except IndexError:
                pass

            try:
                if maze.grid[y][x + i] == squareType.value and x + i >= 0:
                    adjacent_squares.append((y, x + i))
            except IndexError:
                pass

        return adjacent_squares

    @staticmethod
    def canBreakWall(maze, wall):
        adjacent_walls = MazeManager.getAdjacentSquares(maze, wall, SquareType.WALL)

        if len(adjacent_walls) != 2:
            return False

        coords = adjacent_walls[0]

        for adjacentWall in adjacent_walls[1:]:
            if adjacentWall[0] != coords[0] and adjacentWall[1] != coords[1]:
                return False
            else:
                coords = adjacent_walls

        return True

    @staticmethod
    def wallBreaker(maze):
        for i in range(1, maze.grid.shape[0] - 1):
            for j in range(1, maze.grid.shape[1] - 1):
                if maze.grid[i][j] == SquareType.WALL.value:
                    r = random.randint(1, 7)
                    if r == 7:
                        if MazeManager.canBreakWall(maze, (i, j)):
                            maze.grid[i][j] = SquareType.ROOM.value

    @staticmethod
    def defineStateSpace(maze):
        # maze.start and maze.end are on the outer wall. therefore, you can get the only adjacent room
        # simply by calling getAdjacentSquares on it and it returns only one room.
        state_space = [maze.start, maze.end]

        for i in range(1, maze.grid.shape[0] - 1):
            for j in range(1, maze.grid.shape[1] - 1):
                if maze.grid[i][j] == SquareType.ROOM.value:
                    if len(MazeManager.getAdjacentSquares(maze, (i, j), SquareType.ROOM)) >= 3:
                        state_space.append((i, j))

        return state_space

    @staticmethod
    def getReachableStates(maze, state):
        reachable_states = []
        visited_rooms = []
        state_space = maze.state_space
        if state not in state_space:
            raise ValueError("The room is not a state of the maze problem")

        curr_state = state
        while curr_state is not None:
            adjacents = MazeManager.getAdjacentSquares(maze, curr_state, SquareType.ROOM)
            for square in adjacents:
                if square not in visited_rooms:
                    visited_rooms.append(square)
                    if square in state_space:
                        reachable_states.append(square)
                        
                    else:
                        curr_state = square

        return reachable_states

    # @staticmethod
    # def getReachableStates(maze, state):
    #     reachable_states = []
    #     state_space = maze.state_space
    #     if state not in state_space:
    #         raise ValueError("The room is not a state of the maze problem")
    #
    #     def recursiveNeighboursSearch(maze, state, state_space, reachable_states, visited_rooms):
    #         for square in MazeManager.getAdjacentSquares(maze, state, SquareType.ROOM):
    #             if square not in visited_rooms:
    #                 visited_rooms.append(square)
    #                 if square in state_space:
    #                     reachable_states.append(square)
    #                 else:
    #                     recursiveNeighboursSearch(maze, square, state_space, reachable_states, visited_rooms)
    #
    #     recursiveNeighboursSearch(maze, state, state_space, reachable_states, [state])
    #     return reachable_states

    @staticmethod
    def getPath(maze, start, goal):
        path = []
        visited_adjacents = []
        reachable_states = MazeManager.getReachableStates(maze, start)

        room = start

        while room != goal:
            # Find adjacents actual node
            adjacents = MazeManager.getAdjacentSquares(maze, room, SquareType.ROOM)

            # Find an adjacent not yet explored

            random_adjacent = None

            for adjacent in adjacents:
                if adjacent not in visited_adjacents:
                    random_adjacent = adjacent

            if random_adjacent is None:
                room = start
                path = []
                continue

            visited_adjacents.append(room)
            visited_adjacents.append(random_adjacent)

            # If the adjacent is a reachable state of start node
            if random_adjacent in reachable_states:
                # If the adjacent state is the goal
                if random_adjacent == goal:
                    path.append(random_adjacent)  # Add the adjacent to the path
                    return path  # Return solution
                # If the adjacent state isn't the goal
                else:
                    path = []  # clear the list
                    room = start

            else:
                path.append(random_adjacent)
                room = random_adjacent


if __name__ == "__main__":
    for i in range(1):

        manager = MazeManager(10, 10)
        manager.drawMaze(manager.maze, stateSpace=True, solution=True)
        # print(manager.getReachableStates(manager.maze, state=(19, 9)))
        # print(manager.getReachableStatesIterative(manager.maze, state=(19, 9)))
        #print(MazeManager.getPath(manager.maze, (19, 9), (17, 7)))
        print(MazeManager.getReachableStates(manager.maze, (17, 7)))
