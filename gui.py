from tkinter import *
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import graphviz
import numpy as np

import os

from maze import Maze, SquareType, getReachablePaths


curr_image = 0


def drawMaze(maze, filename, solution=False, stateSpace=False, node=None):
    if type(maze) != Maze:
        raise TypeError("You must pass a maze to draw")

    grid = maze.colored_grid.copy() if stateSpace else maze.grid.copy()

    grid[maze.start] = SquareType.START.value
    grid[maze.end] = SquareType.EXIT.value

    if solution and maze.solutions:
        for i, state in enumerate(maze.solutions):
            if i != len(maze.solutions) - 1:
                reach_states, paths = getReachablePaths(maze, state.data)
                index = reach_states.index(maze.solutions[i + 1].data)
                path = paths[index]
                for room in path:
                    if room != maze.end:
                        grid[room[0]][room[1]] = SquareType.SOLUTION.value

    if node is not None:
        grid[node.data[0]][node.data[1]] = SquareType.SOLUTION.value

    # Draw the maze
    fig, ax = plt.subplots()
    ax.imshow(grid, cmap=maze.color_map, norm=maze.norm)

    # Show grid
    plt.grid(which='major', axis='both')
    plt.xticks(np.arange(-0.5, maze.colored_grid.shape[1], 1))
    plt.yticks(np.arange(-0.5, maze.colored_grid.shape[0], 1))

    # # Remove tick labels
    ax.set_yticklabels([])
    ax.set_xticklabels([])

    try:
        os.mkdir('./mazes')
    except FileExistsError:
        pass
    plt.savefig('./mazes/' + str(filename) + '.png')


def drawTree(nodes, selected_node, filename, goal=False, prune=False):
    tree = graphviz.Digraph(filename, format='png')
    directory = './trees/'

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


def images_cleanup():
    try:
        for file in os.listdir('./trees'):
            os.remove('./trees/' + file)
        for file in os.listdir('./mazes'):
            os.remove('./mazes/' + file)
    except FileNotFoundError:
        pass

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


def showImage(path, label):
    img = resizeImage(Image.open(path), 700, 700)
    photo_image = ImageTk.PhotoImage(img)

    label.config(image=photo_image)
    label.image = photo_image
