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

def changeImage(label):
	global curr_image
	path = './temp/' + str(curr_image) + '.png'

	try:
		photo_image = ImageTk.PhotoImage(Image.open(path))
		label.config(image=photo_image)
		label.image = photo_image
	except FileNotFoundError:
		print("Immagini finite")
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

	label = Label(root)
	label.pack()

	nextButton = tkinter.Button(root, text="Next", command=lambda: changeImage(label))
	nextButton.pack()

	T = Text(root,)

	changeImage(label)

	root.mainloop()

