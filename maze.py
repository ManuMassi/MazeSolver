from enum import Enum
from matplotlib import colors
import random

from mazelib import Maze
from mazelib.generate.AldousBroder import AldousBroder


class SquareType(Enum):
    """
    An enum class that represents the types of squares in the maze
    """
    ROOM = 0
    WALL = 1
    START = 2
    EXIT = 3
    SOLUTION = 4
    STATE = 5


def generateMaze(height, width, seed=None):
    """
    Function that generates and initializes a maze with a given height and width.
    :param height: height of the maze
    :param width: width of the maze
    :param seed: optional seed to create a certain maze
    :return: the generated maze
    """
    # Creation of the maze with mazelib functions
    maze = Maze(seed)
    maze.generator = AldousBroder(height, width)
    maze.generate()
    maze.generate_entrances()

    # Initializing start and end of the maze
    maze.start = getAdjacentSquares(maze, maze.start, SquareType.ROOM)[0]
    maze.end = getAdjacentSquares(maze, maze.end, SquareType.ROOM)[0]

    # Breaking random walls in the maze to create more solutions
    wallBreaker(maze)

    # Defining the state space
    maze.state_space = defineStateSpace(maze)

    # Settings proper rooms to their color
    _initialize_colors(maze)

    return maze


def _initialize_colors(maze):
    """
    Function that initialize maze's square colors
    :param maze: the maze to work with
    """

    # Temporary grid where the start and the end are set to 2 and 3
    maze.colored_grid = maze.grid.copy()

    # Coloring state space squares
    for y, x in maze.state_space:
        maze.colored_grid[y][x] = SquareType.STATE.value

    # Coloring start and end
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


def getAdjacentSquares(maze, square, square_type=SquareType.WALL):
    """
    Function that returns tha adjacent squares of a given squares.
    :param maze: the maze to work with
    :param square: the square to analyze
    :param square_type: the type of adjacents squares to return
    :return: the adjacent squares of the given square type
    """

    # Type checlk
    if type(square_type) is not SquareType:
        raise TypeError("You must pass a SquareType type")

    # Initializing variables
    y = square[0]
    x = square[1]
    adjacent_squares = []

    # Iteration in all the four directions
    for i in range(-1, 2, 2):  # [-1, 1]
        try:
            # Checking if the type of the current adjacent square is the requested type
            if maze.grid[y + i][x] == square_type.value and y + i >= 0:
                # Appending if true
                adjacent_squares.append((y + i, x))
        except IndexError:
            pass

        try:
            # Checking if the type of the current adjacent square is the requested type
            if maze.grid[y][x + i] == square_type.value and x + i >= 0:
                # Appending if true
                adjacent_squares.append((y, x + i))
        except IndexError:
            pass

    return adjacent_squares


def canBreakWall(maze, wall):
    """
    Function that returns True if a wall can be broken, False otherwise.
    This function returns true only if a wall is surrounded vertically or horizontally by other
    two walls.
    :param maze: maze to work with
    :param wall: wall to check if it can be broken
    :return:
    """
    # Getting adjacent walls of the current wall
    adjacent_walls = getAdjacentSquares(maze, wall, SquareType.WALL)

    # If there are not two walls that surround it, the wall can't be broken
    if len(adjacent_walls) != 2:
        return False

    # Saving coords
    coords = adjacent_walls[0]

    # If the surrounding walls are not positioned vertically or horizontally with respect to the current wall,
    # it cannot be broken
    for adjacentWall in adjacent_walls[1:]:
        if adjacentWall[0] != coords[0] and adjacentWall[1] != coords[1]:
            return False
        else:
            coords = adjacent_walls

    # If the wall passed all the previous checks
    return True


def wallBreaker(maze):
    """
    Function that randomly breaks walls of the maze to create new solutions.
    :param maze: The maze to work with
    :return:
    """

    # Checking all the walls in the maze
    for i in range(1, maze.grid.shape[0] - 1):
        for j in range(1, maze.grid.shape[1] - 1):
            if maze.grid[i][j] == SquareType.WALL.value:
                # Creating a random number
                r = random.randint(1, 7)
                if r == 7:
                    # If the wall can be broken, the function replaces it with a room
                    if canBreakWall(maze, (i, j)):
                        maze.grid[i][j] = SquareType.ROOM.value


def defineStateSpace(maze):
    """
    A function that defines the state space of the maze. To reduce the complexity, a state is defined
    by a room that corresponds to an intersection between paths.
    :param maze: maze to work with
    :return: the state space of the maze
    """
    # Adding the start and end rooms to the state space
    state_space = [maze.start, maze.end]

    # Checking all the rooms in the maze
    for i in range(1, maze.grid.shape[0] - 1):
        for j in range(1, maze.grid.shape[1] - 1):
            if maze.grid[i][j] == SquareType.ROOM.value:
                # If the room can be considered a state, it is added to state spaxe
                if isState(maze, (i, j)):
                    state_space.append((i, j))

    return state_space


def isState(maze, room):
    """
    Function that returns true if the room is a state. A room is a state when it corresponds to an
    intersection.
    :param maze: maze to work with
    :param room: room to analyze
    :return:
    """

    # If the adjacents rooms are three or more, the current room is a state
    return len(getAdjacentSquares(maze, room, SquareType.ROOM)) >= 3 or \
           room == maze.start or \
           room == maze.end


def getReachablePaths(maze, start):
    """
    Functions that defines the reachable states and relative paths from start node to each reachable state
    :param maze: maze to work with
    :param start: start room
    :return:
    """

    # Initializing variables
    paths = []
    visited_adjacents = []
    reachable_states = []
    current_path = []

    room = start

    # Infinite loop
    while True:
        # Find adjacents actual node
        adjacents = getAdjacentSquares(maze, room, SquareType.ROOM)

        # Find an adjacent not yet explored
        current_adjacent = None

        for adjacent in adjacents:
            if adjacent not in visited_adjacents:
                current_adjacent = adjacent
                break

        # If more adjacent rooms can be visited
        if current_adjacent:
            # The adjacent and the room are set as visited
            visited_adjacents.append(room)
            visited_adjacents.append(current_adjacent)

            # Adding the adjacent to the current path
            current_path.append(current_adjacent)

            # If the adjacent is a reachable state of start node
            if isState(maze, current_adjacent):
                # The adjacent is added to reachable state
                reachable_states.append(current_adjacent)
                # The path from the start room to this reachable state is set to the current path
                paths.append(current_path)

                # Emptying tha current path and returning to the start
                current_path = []
                room = start

            # If the adjacent is not a reachable state, it is set to be the next analyzed state
            else:
                room = current_adjacent

        # If there are not more visitable adjacents, it returns the solution. Otherwise, it starts over
        else:
            if room == start:
                return reachable_states, paths
            current_path = []
            room = start
