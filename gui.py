import graphviz
from tkinter import *
from PIL import Image, ImageTk
import tkinter
import os


def drawTree(nodes):
	tree = graphviz.Digraph('tree', format='png')

	for node in nodes:
		# Adds nodes
		tree.node(str(node.id), str(node.data))

		for child in node.children:
			# Adds child
			tree.node(str(child.id), str(child.data))
			# Create edge
			tree.edge(str(node.id), str(child.id))

	# Save tree.png
	tree.render(directory='.', view=False)

	os.remove('./tree.gv')
	os.rename('./tree.gv.png', './tree.png')



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

