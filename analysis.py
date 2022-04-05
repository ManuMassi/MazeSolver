import time

from maze import generateMaze
from search_algorithms import breadth_first_search, \
    A_star_search, \
    uniform_cost_search, \
    iterative_deepening_depth_first_search


def analysis(min_size, max_size, n_mazes):
    for size in range(min_size, max_size + 1, 5):
        analysis_result = {
            breadth_first_search: {
                'avg_time': 0,
                'avg_nodes': 0,
                'avg_path_cost': 0
            },
            uniform_cost_search: {
                'avg_time': 0,
                'avg_nodes': 0,
                'avg_path_cost': 0
            },
            A_star_search: {
                'avg_time': 0,
                'avg_nodes': 0,
                'avg_path_cost': 0
            },
            iterative_deepening_depth_first_search: {
                'avg_time': 0,
                'avg_nodes': 0,
                'avg_path_cost': 0
            }
        }
        for i in range(n_mazes):
            maze = generateMaze(size, size)

            for algorithm in [breadth_first_search, uniform_cost_search,
                              A_star_search, iterative_deepening_depth_first_search]:

                start_time = time.time()
                generated_nodes, path_cost = algorithm(maze, draw=False, analysis=True)[1:]
                end_time = time.time()

                analysis_result[algorithm]['avg_time'] += (end_time - start_time)
                analysis_result[algorithm]['avg_nodes'] += generated_nodes
                analysis_result[algorithm]['avg_path_cost'] += path_cost

        print("Size", size)
        for algo in analysis_result.keys():
            print("Algo:", algo.__name__)
            for avg in analysis_result[algo].keys():
                analysis_result[algo][avg] /= n_mazes
                print(avg, analysis_result[algo][avg])
            print("\n")
        print("\n\n")


if __name__ == "__main__":
    analysis(5, 20, n_mazes=30)
