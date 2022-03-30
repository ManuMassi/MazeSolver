from enum import Enum
from matplotlib import colors
import random


from mazelib import Maze
from mazelib.generate.AldousBroder import AldousBroder


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
        maze = Maze()
        maze.generator = AldousBroder(height, width)
        maze.generate()
        maze.generate_entrances()

        maze.start = MazeManager.getAdjacentSquares(maze, maze.start, SquareType.ROOM)[0]
        maze.end = MazeManager.getAdjacentSquares(maze, maze.end, SquareType.ROOM)[0]

        MazeManager.wallBreaker(maze)

        maze.state_space = MazeManager.defineStateSpace(maze)

        MazeManager._initialize_colors(maze)

        return maze

    def _initialize_colors(maze):
        # Temporary grid where the start and the end are set to 2 and 3
        maze.colored_grid = maze.grid.copy()

        for y, x in maze.state_space:
            maze.colored_grid[y][x] = SquareType.STATE.value

        maze.colored_grid[maze.start] = SquareType.START.value
        maze.colored_grid[maze.end] = SquareType.EXIT.value

        # Color map:
        # 0 -> white : empty spaces
        # 1 -> black : walls
        # 2 -> blue : start
        # 3 -> red : exit
        # 4 -> yellow : solution
        # 5 -> purple : state
        maze.color_map = colors.ListedColormap(['white', 'black', 'blue', 'red', 'yellow', 'purple'])
        maze.bounds = list(range(0, 7))  # [0, 1, 2, 3, 4, 5]
        maze.norm = colors.BoundaryNorm(maze.bounds, maze.color_map.N)

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
                    if MazeManager.isState(maze, (i, j)):
                        state_space.append((i, j))

        return state_space

    @staticmethod
    def isState(maze, room):
        return len(MazeManager.getAdjacentSquares(maze, room, SquareType.ROOM)) >= 3 or room == maze.start or room == maze.end

    @staticmethod
    def getReachablePaths(maze, start):
        paths = []
        visited_adjacents = []
        reachable_states = []
        current_path = []

        room = start

        while True:
            # Find adjacents actual node
            adjacents = MazeManager.getAdjacentSquares(maze, room, SquareType.ROOM)

            # Find an adjacent not yet explored
            current_adjacent = None

            for adjacent in adjacents:
                if adjacent not in visited_adjacents:
                    current_adjacent = adjacent
                    break

            if current_adjacent:
                visited_adjacents.append(room)
                visited_adjacents.append(current_adjacent)

                current_path.append(current_adjacent)

                # If the adjacent is a reachable state of start node
                if MazeManager.isState(maze, current_adjacent):
                    reachable_states.append(current_adjacent)
                    paths.append(current_path)

                    current_path = []
                    room = start

                else:
                    room = current_adjacent

            else:
                if room == start:
                    return reachable_states, paths
                current_path = []
                room = start
