from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk
from search_algorithms import MazeManager, breadth_first_search

curr_image = 0


def changeImage(tree_label, maze_label):
    global curr_image

    # Finding the path of the current image
    tree_path = './trees/' + str(curr_image) + '.png'
    maze_path = './mazes/' + str(curr_image) + '.png'

    try:
        # Resizing images
        tree_img = resizeImage(Image.open(tree_path), 900, 700)
        maze_img = resizeImage(Image.open(maze_path), 700, 700)

        tree = ImageTk.PhotoImage(tree_img)
        maze = ImageTk.PhotoImage(maze_img)

        # Initialazing tree label
        tree_label.config(image=tree)
        tree_label.image = tree

        # Initializing maze label
        maze_label.config(image=maze)
        maze_label.image = maze

    except FileNotFoundError:
        # search_ended_txt = Label(root, text='Immagini finite')
        # search_ended_txt.pack()
        pass

    curr_image += 1


def resizeImage(img, max_width, max_height):
    width, height = img.size

    if width > max_width or height > max_height:
        ratio = min(max_width / width, max_height / height)
        new_size = tuple(int(dimension * ratio) for dimension in img.size)

        img = img.resize(new_size, Image.ANTIALIAS)

    return img


if __name__ == "__main__":
    manager = MazeManager(7, 7)

    dps = breadth_first_search(manager.maze, manager.maze.start, manager.maze.end)

    root = Tk()
    root.geometry("1920x1080")
    root.title("Maze Solver")
    root.config(bg="lightgrey")

    # Setting buttons
    nextButton = ttk.Button(root, style="TButton", text="Next", command=lambda: changeImage(tree_label, maze_label))
    nextButton.pack(pady=50, side=BOTTOM)

    # Setting tree images
    tree_label = Label(root, width=900, height=700, bg="white", borderwidth=20)
    tree_label.pack(padx=5, pady=15, side=LEFT, expand=True)

    # Setting maze images
    maze_label = Label(root, width=700, height=700, bg="white", borderwidth=20)
    maze_label.pack(padx=5, pady=15, side=RIGHT, expand=True)

    # Starting with first image
    changeImage(tree_label, maze_label)

    # Setting styles
    button_style = ttk.Style(root)
    button_style.theme_use('classic')
    button_style.configure("TButton",background='#afccfa', borderwidth=0.1, font=('Helvetica', 40))

    root.mainloop()

