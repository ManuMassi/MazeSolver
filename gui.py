import graphviz
from tkinter import *
from PIL import Image, ImageTk
import tkinter
import os


def drawTree(nodes, selected_node, directory, filename, goal=False, prune=False):
	tree = graphviz.Digraph(filename, format='png')

	for node in nodes:
		# Adds nodes
		if node == selected_node:
			if goal:
				tree.node(str(node.id), str(node.data), style="filled", color="green")
			elif prune:
				tree.node(str(node.id), str(node.data), style="filled", color="red")
			else:
				tree.node(str(node.id), str(node.data), color="yellow")
		else:
			tree.node(str(node.id), str(node.data))

		for child in node.children:
			# Adds child
			if prune and node == selected_node:
				tree.node(str(child.id), str(child.data), style="filled", color="red")
			else:
				tree.node(str(child.id), str(child.data))
			# Create edge
			tree.edge(str(node.id), str(child.id))

	# Save tree.png
	tree.render(directory=directory, view=False)

	os.remove(directory + filename + ".gv")
	os.rename(directory + filename + ".gv.png", directory + filename + ".png")


def changeImage(path, label):
	photoImage = ImageTk.PhotoImage(Image.open(path))
	label.config(image=photoImage)
	label.image = photoImage


if __name__ == "__main__":
	dot = graphviz.Digraph('img1', format='png')

	dot.node('A')
	dot.node('B')
	dot.node('C')

	dot.edge('A', 'B', constraint='true')
	dot.edge('A', 'C', constraint='true')

	# Save image
	dot.render(directory='.', view=False)

	dot.edge('B', 'C', constraint='false')
	dot.render(directory='./ciao/', view=False)

	# Tkinter
	root = Tk()

	label = Label(root)
	label.pack()

	nextButton = tkinter.Button(root, text="Next", command=lambda: changeImage('./ciao/img1.gv.png', label))
	nextButton.pack()

	changeImage('./img1.gv.png', label)

	root.mainloop()

