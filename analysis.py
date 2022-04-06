import time

from maze import generateMaze
from search_algorithms import breadth_first_search, \
    A_star_search, \
    uniform_cost_search, \
    iterative_deepening_depth_first_search


def analysis(min_size, max_size, n_mazes):
    """
    A function that creates mazes starting from size min_size until it reaches max_size with steps of five dimensions.
    Each maze of a certain size is generated n_mazes times.
    Every maze is solved with the four implemented algorithms.
    The function gives the average analysis of each algorithm for each size.
    :param min_size: the starting size of mazes to create
    :param max_size: the maximum size of mazes to create
    :param n_mazes: the number of mazes to create for each size
    """
    # Creates mazes starting from min_sizes until it reaches max_size with steps of 5 dimensions.
    for size in range(min_size, max_size + 1, 5):
        # Data structure that contains the average data for each algorithm for each size
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
        # For a given size, it creates n_mazes mazes
        for i in range(n_mazes):
            maze = generateMaze(size, size)

            # Each maze is solved with each algorithm
            for algorithm in [breadth_first_search, uniform_cost_search,
                              A_star_search, iterative_deepening_depth_first_search]:

                # Saving all the information about a maze
                start_time = time.time()
                generated_nodes, path_cost = algorithm(maze, draw=False, analysis=True)[1:]
                end_time = time.time()

                # Calculating the average data for each information
                analysis_result[algorithm]['avg_time'] += (end_time - start_time)
                analysis_result[algorithm]['avg_nodes'] += generated_nodes
                analysis_result[algorithm]['avg_path_cost'] += path_cost

        # Prints all the information
        print("Size", size)
        for algo in analysis_result.keys():
            print("Algo:", algo.__name__)
            for avg in analysis_result[algo].keys():
                analysis_result[algo][avg] /= n_mazes
                print(avg, analysis_result[algo][avg])
            print("\n")
        print("\n\n")


if __name__ == "__main__":
    analysis(5, 15, n_mazes=30)
