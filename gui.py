from tkinter import *
from PIL import Image, ImageTk
import tkinter
from search_algorithms import MazeManager, breadth_first_search

curr_image = 0


def changeImage(tree_label, root):
    global curr_image
    path = './temp/' + str(curr_image) + '.png'

    try:
        img = Image.open(path)

        width, height = img.size
        max_width = max_height = 700

        if width > max_width or height > max_height:
            ratio = min(max_width / width, max_height / height)
            new_size = tuple(int(dimension * ratio) for dimension in img.size)

            img = img.resize(new_size, Image.ANTIALIAS)

        photo_image = ImageTk.PhotoImage(img)

        tree_label.config(image=photo_image)
        tree_label.image = photo_image

    except FileNotFoundError:
        # search_ended_txt = Label(root, text='Immagini finite')
        # search_ended_txt.pack()
        pass

    curr_image += 1


if __name__ == "__main__":
    manager = MazeManager(9, 9)
    # manager.drawMaze(manager.maze, stateSpace=True)

    dps = breadth_first_search(manager.maze, manager.maze.start, manager.maze.end)

    # Tkinter
    root = Tk()
    root.geometry("1920x1080")
    root.title("Maze Solver")
    root.config(bg="lightgrey")

    # Setting next button
    nextButton = tkinter.Button(root, text="Next", command=lambda: changeImage(tree_label, root))
    nextButton.pack(pady=50, side=BOTTOM)

    # Setting tree images
    tree_label = Label(root, width=900, height=700, bg="white", borderwidth=20)
    tree_label.pack(padx=5, pady=15, side=LEFT, expand=True)

    # Setting maze images
    maze_label = Label(root, width=900, height=700, bg="white", borderwidth=20)
    maze_label.pack(padx=5, pady=15, side=RIGHT, expand=True)

    maze_img = ImageTk.PhotoImage(Image.open('./maze.png'))
    maze_label.config(image=maze_img)
    maze_label.image = maze_img

    # Starting with first image
    changeImage(tree_label, root)

    root.mainloop()
