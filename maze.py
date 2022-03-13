from enum import Enum

from matplotlib import colors
from mazelib import Maze
from mazelib.generate.AldousBroder import AldousBroder
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
        MazeManager.wallBreaker(maze)

        return maze

    @staticmethod
    def drawMaze(maze, solution=False, stateSpace=False):
        if type(maze) != Maze:
            raise TypeError("You must pass a maze to draw")

        # Temporary grid where the start and the end are set to 2 and 3
        grid = maze.grid.copy()
        grid[maze.start] = SquareType.START.value
        grid[maze.end] = SquareType.EXIT.value

        if solution and maze.solutions:
            for y, x in maze.solutions[0]:
                grid[y][x] = SquareType.SOLUTION.value

        if stateSpace:
            for y, x in MazeManager.defineStateSpace(maze):
                grid[y][x] = SquareType.STATE.value

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
    def getAdjacentSquares(maze, x, y, squareType=SquareType.WALL):
        if type(squareType) is not SquareType:
            raise TypeError("You must pass a SquareType type")

        adjacentSquares = []

        for i in range(-1, 2, 2):  # [-1, 1]
            try:
                if maze.grid[y + i][x] == squareType.value and y + i >= 0:
                    adjacentSquares.append((x, y + i))
            except IndexError:
                pass

            try:
                if maze.grid[y][x + i] == squareType.value and x + i >= 0:
                    adjacentSquares.append((x + i, y))
            except IndexError:
                pass

        return adjacentSquares

    @staticmethod
    def canBreakWall(maze, wall_x, wall_y):
        adjacentWalls = MazeManager.getAdjacentSquares(maze, wall_x, wall_y, SquareType.WALL)

        if len(adjacentWalls) != 2:
            return False

        coords = adjacentWalls[0]

        for adjacentWall in adjacentWalls[1:]:
            if adjacentWall[0] != coords[0] and adjacentWall[1] != coords[1]:
                return False
            else:
                coords = adjacentWalls

        return True

    @staticmethod
    def wallBreaker(maze):
        for i in range(1, maze.grid.shape[0] - 1):
            for j in range(1, maze.grid.shape[1] - 1):
                if maze.grid[i][j] == SquareType.WALL.value:
                    r = random.randint(1, 7)
                    if r == 7:
                        if MazeManager.canBreakWall(maze, j, i):
                            maze.grid[i][j] = SquareType.ROOM.value

    @staticmethod
    def defineStateSpace(maze):
        # maze.start and maze.end are on the outer wall. therefore, you can get the only adjacent room
        # simply by calling getAdjacentSquares on it and it returns only one room.
        stateSpace = [MazeManager.getAdjacentSquares(maze, maze.start[0], maze.start[1], SquareType.ROOM)[0],
                      MazeManager.getAdjacentSquares(maze, maze.end[0], maze.end[1], SquareType.ROOM)[0]]

        for i in range(1, maze.grid.shape[0] - 1):
            for j in range(1, maze.grid.shape[1] - 1):
                if maze.grid[i][j] == SquareType.ROOM.value:
                    if len(MazeManager.getAdjacentSquares(maze, j, i, SquareType.ROOM)) >= 3:
                        stateSpace.append((i, j))

        return stateSpace


# main :)
for i in range(1):

    manager = MazeManager(10, 10)
    manager.drawMaze(manager.maze, stateSpace=True)
    manager.defineStateSpace(manager.maze)