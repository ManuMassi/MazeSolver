import time

from maze import MazeManager
from search_algorithms import breadth_first_search, \
    A_star_search, \
    uniform_cost_search, \
    iterative_deepening_depth_first_search


def analysis(min_size, max_size, n_mazes):
    for size in range(min_size, max_size + 1, 5):
        for i in range(n_mazes):
            maze = MazeManager.generateMaze(size, size, 12345)

            avg_time = 0
            avg_nodes = 0
            avg_path_cost = 0

            for algorithm in [breadth_first_search, uniform_cost_search,
                              A_star_search, iterative_deepening_depth_first_search]:

                start_time = time.time()
                generated_nodes, path_cost = algorithm(maze, draw=False, analysis=True)[1:]
                end_time = time.time()

                avg_time += (end_time - start_time)
                avg_nodes += generated_nodes
                avg_path_cost += path_cost

            # NIOOOOOOO DA CORRREEEEGGEREEEE
            avg_time = avg_time / n_mazes
            avg_nodes = avg_nodes / n_mazes
            avg_path_cost = avg_path_cost / n_mazes
            print(f'size: {size}x{size}\n'
                  f'algorithm: {algorithm.__name__}\n'
                  f'time: {avg_time}\n'
                  f'generated_nodes: {avg_nodes}\n'
                  f'path_cost: {avg_path_cost}\n'
                  '\n')


if __name__ == "__main__":
    analysis(5, 25, 1)
