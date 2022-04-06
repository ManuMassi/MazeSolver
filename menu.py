import tkinter as tk
from tkinter import font as tkfont

import sys

from maze import generateMaze
from gui import changeImage
from search_algorithms import breadth_first_search, \
    A_star_search, \
    uniform_cost_search, \
    iterative_deepening_depth_first_search


class MazeSolverApp(tk.Tk):
    """
    Main class to manage the menu.
    It manages all the frames relative to each different page of the application.
    """

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("1920x1080")
        self.title("MazeSolver")

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Initialize all the frames
        self.frames = {}
        for F in (StartPage, MazeSelectPage, SizeSelectPage, AlgorithmSelectPage, SolverPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage") # Show the starting page

        self.maze = None
        self.algorithm = None

    def show_frame(self, page_name):
        """
        Method to show a page given its name
        :param page_name: the name of the page to show
        """
        # Show a frame for the given page name
        frame = self.frames[page_name]
        frame.tkraise()

    def initialize_maze(self, width=5, height=5):
        """
        Method that initialize the maze relative to the application
        :param width of the maze
        :param height of the maze
        """
        self.maze = generateMaze(height, width, seed=12345)

    def setAlgorithm(self, algorithm):
        """
        Method that sets the current algorithm for path finding
        :param algorithm to use
        """
        if algorithm != breadth_first_search and \
                algorithm != A_star_search and \
                algorithm != uniform_cost_search and \
                algorithm != iterative_deepening_depth_first_search:
            raise TypeError("Algorithm not valid")

        self.algorithm = algorithm

        self.algorithm(self.maze)  # Solve the maze right after algorithm selection


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        tk.Label(self, text="Welcome to MazeSolver", font=controller.title_font).place(relx=0.5, rely=0.4,
                                                                                       anchor=tk.CENTER)

        tk.Button(self, text="START", height=1, width=15,
                  command=lambda: controller.show_frame("MazeSelectPage")).place(relx=0.5, rely=0.45, anchor=tk.CENTER)

        tk.Button(self, text="QUIT", height=1, width=15,
                  command=lambda: sys.exit()).place(relx=0.5, rely=0.48, anchor=tk.CENTER)


class MazeSelectPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        tk.Label(self, text="MazeSolver", font=controller.title_font).place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        tk.Button(self, text="Select maze size", height=1, width=15,
                  command=lambda: controller.show_frame("SizeSelectPage")).place(relx=0.5, rely=0.45, anchor=tk.CENTER)

        tk.Button(self, text="Use default maze (5x5)", height=1, width=15,
                  command=lambda: self.selectMaze()).place(relx=0.5, rely=0.48, anchor=tk.CENTER)

    def selectMaze(self):
        self.controller.initialize_maze()
        self.controller.show_frame("AlgorithmSelectPage")


class SizeSelectPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        tk.Label(self, text="Select the maze size", font=controller.title_font).place(relx=0.5, rely=0.4,
                                                                                      anchor=tk.CENTER)

        option_list = [str(i) + "x" + str(i) for i in range(3, 16)]
        input_value = tk.StringVar(self)
        input_value.set("Select maze dimension")

        tk.OptionMenu(self, input_value, *option_list).place(relx=0.5, rely=0.45, anchor=tk.CENTER)

        tk.Button(self, text="Create Maze", height=1, width=15,
                  command=lambda: self.selectMaze(input_value)).place(relx=0.5, rely=0.48, anchor=tk.CENTER)

    def selectMaze(self, input_value):

        if input_value.get()[1] != 'x' and input_value.get()[0] != 's':
            size = int(input_value.get()[0:2])
        else:
            size = int(input_value.get()[0])

        self.controller.initialize_maze(width=size, height=size)
        self.controller.show_frame("AlgorithmSelectPage")


class AlgorithmSelectPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        tk.Label(self, text="Choose an algorithm", font=controller.title_font).place(relx=0.5, rely=0.4,
                                                                                     anchor=tk.CENTER)

        tk.Button(self, text="Breadth First Search", height=1, width=25,
                  command=lambda: self.selectAlgorithm(breadth_first_search)).place(relx=0.43, rely=0.45,
                                                                                    anchor=tk.CENTER)

        tk.Button(self, text="A* Search", height=1, width=25,
                  command=lambda: self.selectAlgorithm(A_star_search)).place(relx=0.57, rely=0.45, anchor=tk.CENTER)

        tk.Button(self, text="Uniform Cost Search", height=1, width=25,
                  command=lambda: self.selectAlgorithm(uniform_cost_search)).place(relx=0.43, rely=0.48,
                                                                                   anchor=tk.CENTER)

        tk.Button(self, text="Iterative Deepening Depth First Search", height=1, width=25,
                  command=lambda: self.selectAlgorithm(iterative_deepening_depth_first_search)).place(relx=0.57,
                                                                                                      rely=0.48,
                                                                                                      anchor=tk.CENTER)

    def selectAlgorithm(self, algorithm):
        self.controller.setAlgorithm(algorithm)
        self.controller.show_frame("SolverPage")


class SolverPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        tk.Label(self, text="SolverPage", font=controller.title_font).pack(side="top", fill="x", pady=10)

        # Setting buttons
        nextButton = tk.Button(self, text="Start", height=1, width=15,
                               command=lambda: [changeImage(tree_label, maze_label),
                                                self.changeButtonName(nextButton)])
        nextButton.pack(pady=30, side=tk.BOTTOM)

        tk.Button(self, text="Quit", height=1, width=15,
                  command=lambda: sys.exit()).pack(side=tk.BOTTOM, padx=100, pady=0)

        # Setting tree images
        tree_label = tk.Label(self, width=900, height=700, bg="white")
        tree_label.pack(padx=5, pady=15, side=tk.LEFT, expand=True)

        # Setting maze images
        maze_label = tk.Label(self, width=700, height=700, bg="white")
        maze_label.pack(padx=5, pady=15, side=tk.RIGHT, expand=True)

    @staticmethod
    def changeButtonName(button):
        if button['text'] == 'Start':
            button['text'] = 'Next'


if __name__ == "__main__":
    app = MazeSolverApp()
    app.mainloop()
