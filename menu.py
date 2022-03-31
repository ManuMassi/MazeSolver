import tkinter as tk
from tkinter import font as tkfont
import sys
from search_algorithms import breadth_first_search, \
    A_star_search, \
    uniform_cost_search, \
    iterative_deepening_depth_first_search
from maze import MazeManager


class SampleApp(tk.Tk):

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

        self.frames = {}
        for F in (StartPage, MazeSelectPage, SizeSelectPage, AlgorithmSelectPage, SolverPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

        self.maze = None
        self.algorithm = None

    def show_frame(self, page_name):
        # Show a frame for the given page name
        frame = self.frames[page_name]
        frame.tkraise()

    def initialize_maze(self, width=5, height=5):
        self.maze = MazeManager.generateMaze(height, width)

    def setAlgorithm(self, algorithm):
        if algorithm != breadth_first_search or \
                algorithm != A_star_search or \
                algorithm != uniform_cost_search or \
                algorithm != iterative_deepening_depth_first_search:
            raise TypeError("Algorithm not valid")

        self.algorithm = algorithm


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Welcome to MazeSolver", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="START",
                            command=lambda: controller.show_frame("MazeSelectPage"))
        button2 = tk.Button(self, text="QUIT",
                            command=lambda: sys.exit())
        button1.pack()
        button2.pack()


class MazeSelectPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="MazeSolver", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        random_maze_button = tk.Button(self, text="Generate random maze",
                                       command=lambda: controller.show_frame("SizeSelectPage"))
        random_maze_button.pack()

        default_maze_button = tk.Button(self, text="Use default maze (5x5)",
                                        command=lambda: self.selectMaze())
        default_maze_button.pack()

    def selectMaze(self):
        self.controller.initialize_maze()
        self.controller.show_frame("AlgorithmSelectPage")


class SizeSelectPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Select the maze size", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        option_list = [str(i) + "x" + str(i) for i in range(3, 16)]
        input_value = tk.StringVar(self)
        input_value.set("Select maze dimension")

        dropdown_menu = tk.OptionMenu(self, input_value, *option_list)
        dropdown_menu.pack()

        button = tk.Button(self, text="Create Maze", command=lambda: self.selectMaze(input_value))
        button.pack()

    def selectMaze(self, input_value):

        if input_value.get()[1] != 'x':
            size = int(input_value.get()[0:2])
        else:
            size = int(input_value.get()[0])

        self.controller.initialize_maze(width=size, height=size)
        self.controller.show_frame("AlgorithmSelectPage")


class AlgorithmSelectPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Choose an algorithm", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        bfs_button = tk.Button(self, text="Breadth First Search",
                               command=lambda: self.selectAlgorithm(breadth_first_search))
        bfs_button.pack()

        a_s_button = tk.Button(self, text="A* Search",
                               command=lambda: self.selectAlgorithm(A_star_search))
        a_s_button.pack()

        ucs_button = tk.Button(self, text="Uniform Cost Search",
                               command=lambda: self.selectAlgorithm(uniform_cost_search))
        ucs_button.pack()

        iddfs_button = tk.Button(self, text="Iterative Deepening Depth First Search",
                                 command=lambda: self.selectAlgorithm(iterative_deepening_depth_first_search))
        iddfs_button.pack()

    def selectAlgorithm(self, algorithm):
        self.controller.setAlgorithm(algorithm)
        self.controller.show_frame("SolverPage")


class SolverPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="SolverPage", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)



if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
