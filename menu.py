
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
        for F in (StartPage, MazeSelectPage, SizeSelectPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

        self.maze = None

    def show_frame(self, page_name):
        # Show a frame for the given page name
        frame = self.frames[page_name]
        frame.tkraise()

    def initialize_maze(self, default=True, width=5, height=5):
        self.maze = MazeManager.generateMaze(height, width)
        print('ciao')


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Welcome to MazeSolver", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="START",
                            command=lambda: controller.show_frame("PageOne"))
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
                           command=lambda: controller.show_frame("StartPage"))
        random_maze_button.pack()

        default_maze_button = tk.Button(self, text="Use default maze (5x5)",
                           command=lambda: controller.initialize_maze())
        default_maze_button.pack()


class SizeSelectPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 2", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()


class AlgorithmSelectpage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 2", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()


class SolverPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 2", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()