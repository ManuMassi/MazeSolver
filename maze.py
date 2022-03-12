from matplotlib import colors
from mazelib import Maze
from mazelib.generate.AldousBroder import AldousBroder
from mazelib.solve.ShortestPath import ShortestPath
import matplotlib.pyplot as plt
import numpy as np
import random


def drawMaze(maze, solution=False):
    if type(maze) != Maze:
        raise TypeError("You must pass a maze to draw")

    # Temporary grid where the start and the end are set to 2 and 3
    grid = maze.grid
    grid[maze.start] = 2
    grid[maze.end] = 3

    if solution and maze.solutions:
        for y, x in maze.solutions[0]:
            grid[y][x] = 4

    # Color map:
    # 0 -> white : empty spaces
    # 1 -> black : walls
    # 2 -> blue : start
    # 3 -> red : exit
    color_map = colors.ListedColormap(['white', 'black', 'blue', 'red', 'yellow'])
    bounds = list(range(0, 6))  # [0, 1, 2, 3, 4]
    norm = colors.BoundaryNorm(bounds, color_map.N)

    # Draw the maze
    fig, ax = plt.subplots()
    ax.imshow(grid, cmap=color_map, norm=norm)

    # Show grid
    plt.grid(which='major', axis='both')
    plt.xticks(np.arange(-0.5, grid.shape[1], 1)), plt.yticks(np.arange(-0.5, grid.shape[0], 1))

    # Remove tick labels
    ax.set_yticklabels([])
    ax.set_xticklabels([])

    plt.show()


def getAdjacentWalls(maze, wall_x, wall_y):
    adjacentWalls = []

    for i in range(-1, 2, 2):  # [-1, 1]
        if maze.grid[wall_y + i][wall_x] == 1 and wall_y + i >= 0:
            adjacentWalls.append((wall_x, wall_y + i))

        if maze.grid[wall_y][wall_x + i] == 1 and wall_x + i >= 0:
            adjacentWalls.append((wall_x + i, wall_y))

    return adjacentWalls


def canBreakWall(maze, wall_x, wall_y):
    adjacentWalls = getAdjacentWalls(maze, wall_x, wall_y)

    if len(adjacentWalls) != 2:
        return False

    coords = adjacentWalls[0]

    for adjacentWall in adjacentWalls[1:]:
        if adjacentWall[0] != coords[0] and adjacentWall[1] != coords[1]:
            return False
        else:
            coords = adjacentWalls

    return True


def wallBreaker(maze):
    for i in range(1, maze.grid.shape[0] - 1):
        for j in range(1, maze.grid.shape[1] - 1):
            if maze.grid[i][j] == 1:
                if canBreakWall(maze, j, i):
                    r = random.randint(1, 8)
                    if r == 7:
                        maze.grid[i][j] = 0


for i in range(1):

    m = Maze()

    m.generator = AldousBroder(10, 10)
    m.generate()
    m.generate_entrances()
    m.solver = ShortestPath()
    m.solve()
    drawMaze(m, True)

    wallBreaker(m)
    m.solve()
    # print('number of solutions = ', len(m.solutions), '\n')
    drawMaze(m, True)
