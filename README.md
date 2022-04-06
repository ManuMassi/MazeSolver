**Artificial Intelligence project** made for the AI course of Computer Engineering, Cybersecurity and Artificial Intelligence's master degree.

This project is made by Emmanuele Massidda and Aurora Arrus.

This application should show the expansion of a search tree while it searches for the best solution of a given maze.

Implemented algorithms: \
    - A* \
    - Breath First Search \
    - Iterative Deepening Depth First Search \
    - Uniform Cost Search

**Usage**  
  
To run the graphic interface:  
`python3 menu.py`  
  
To try the algorithms without saving any images of the steps:  
    - Go to search_algorithms.py  
    - Generate a maze: `maze = generateMaze(5, 5)`  
    - Solve the maze using an algorithm like that:  
    `breadth_first_search(maze, draw=False)`  
    - The algorithms will return the solution and it will also store it in maze.solutions
