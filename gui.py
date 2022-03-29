from tkinter import *
from PIL import Image, ImageTk
import tkinter
from search_algorithms import MazeManager, breadth_first_search

curr_image = 0


def changeImage(tree_label, root):
	global curr_image
	path = './temp/' + str(curr_image) + '.png'

	try:
		photo_image = ImageTk.PhotoImage(Image.open(path))
		tree_label.config(image=photo_image)
		tree_label.image = photo_image
	except FileNotFoundError:
		search_ended_txt = Label(root, text='Immagini finite')
		search_ended_txt.pack()

	curr_image += 1


if __name__ == "__main__":
	manager = MazeManager(5, 5)
	manager.drawMaze(manager.maze, stateSpace=True)

	dps = breadth_first_search(manager.maze, manager.maze.start, manager.maze.end)

	# Tkinter
	root = Tk()
	root.geometry("1920x1080")
	root.title("Maze Solver")
	# root.config(bg="white")

	# Setting next button
	nextButton = tkinter.Button(root, text="Next", command=lambda: changeImage(tree_label, root))
	nextButton.pack(pady=50, side=BOTTOM)

	# Setting tree images
	tree_label = Label(root)
	tree_label.pack(padx=5, pady=15, side=LEFT, expand=True)

	# Setting maze images
	maze_label = Label(root)
	maze_label.pack(padx=5, pady=15, side=RIGHT, expand=True)

	maze_img = ImageTk.PhotoImage(Image.open('./maze.png'))
	maze_label.config(image=maze_img)
	maze_label.image = maze_img

	# Starting with first image
	changeImage(tree_label, root)

	root.mainloop()

