from search_algorithms import breadth_first_search, \
    A_star_search, \
    uniform_cost_search, \
    iterative_deepening_depth_first_search
import time
from maze import MazeManager


def computeTime():
    for size in range(5, 26, 5):
        for algorithm in [breadth_first_search, uniform_cost_search,
                          A_star_search, iterative_deepening_depth_first_search]:

            avg_time = 0
            for i in range(30):
                maze = MazeManager.generateMaze(size, size)

                start_time = time.time()
                algorithm(maze, draw=False)
                end_time = time.time()

                avg_time += (end_time - start_time)
            avg_time = avg_time / 30
            print(f'size: {size}x{size}\n'
                  f'algorithm: {algorithm.__name__}\n'
                  f'time: {avg_time}\n')


def computeGeneratedNodes():
    pass


def computeSolutionCost():
    pass

computeTime()