import graphviz
from tkinter import *
from PIL import Image, ImageTk
import tkinter
import os
from search_algorithms import MazeManager, breadth_first_search

curr_image = 0


# def changeImage(path, label):
# 	photoImage = ImageTk.PhotoImage(Image.open(path))
# 	label.config(image=photoImage)
# 	label.image = photoImage

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

	# ucs = uniform_cost_search(manager.maze, manager.maze.start, manager.maze.end)
	# A_s = A_star_search(manager.maze, manager.maze.start, manager.maze.end)
	dps = breadth_first_search(manager.maze, manager.maze.start, manager.maze.end)
	# dps = iterative_deepening_depth_first_search(manager.maze, manager.maze.start, manager.maze.end)

	# Tkinter
	root = Tk()
	root.geometry()

	tree_label = Label(root)
	tree_label.pack()

	nextButton = tkinter.Button(root, text="Next", command=lambda: changeImage(tree_label, root))
	nextButton.pack()

	changeImage(tree_label, root)

	maze_label = Label(root)
	maze_label.pack()
	maze_img = ImageTk.PhotoImage(Image.open('./maze.png'))
	maze_label.config(image=maze_img)
	maze_label.image = maze_img

	root.mainloop()

