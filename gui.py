import graphviz
from tkinter import *
from PIL import Image, ImageTk
import tkinter


def changeImage(path, label):
	photoImage = ImageTk.PhotoImage(Image.open(path))
	label.config(image=photoImage)
	label.image = photoImage


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

