from tkinter import *
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import graphviz
import numpy as np

import os

from maze import Maze, SquareType, getReachablePaths


curr_image = 0


def drawMaze(maze, filename=None, solution=None, stateSpace=None, node=None):
    """
    Function that given a maze draws it graphically.
    It can save it on mazes directory or just show it on the app.
    :param maze: The maze to print
    :param filename: If specified, it saves the maze image in the mazes directory with filename. Otherwise, it just
    shows the image
    :param solution: If specified, the functions prints the solution in the image. Otherwise, it doesn't.
    :param stateSpace: If specified, the state space is printed in the maze. Otherwise, it isn't.
    :param node: If specified, the node is actually selected and printed in yellow. Otherwise, it isn't.
    """

    # Check
    if type(maze) != Maze:
        raise TypeError("You must pass a maze to draw")

    # If the state space doesn't need to be print, it uses a clean grid. Otherwise, it uses the colored one
    grid = maze.colored_grid.copy() if stateSpace else maze.grid.copy()

    # Initialization of start and end rooms of the maze which are printed in yellow
    grid[maze.start] = SquareType.START.value
    grid[maze.end] = SquareType.EXIT.value

    # If the solution has to be printed and exists
    if solution and maze.solutions:
        # For each state of the solution
        for i, state in enumerate(maze.solutions):
            if i != len(maze.solutions) - 1:
                # Finds the correct path from the current state to the next state
                reach_states, paths = getReachablePaths(maze, state.data)
                index = reach_states.index(maze.solutions[i + 1].data)
                path = paths[index]
                # For each room in that path
                for room in path:
                    if room != maze.end:
                        grid[room[0]][room[1]] = SquareType.SOLUTION.value

    # If node is specified, it is printed in yellow
    if node is not None:
        grid[node.data[0]][node.data[1]] = SquareType.SOLUTION.value

    # Draw the maze
    fig, ax = plt.subplots()
    ax.imshow(grid, cmap=maze.color_map, norm=maze.norm)

    # Show grid
    plt.grid(which='major', axis='both')
    plt.xticks(np.arange(-0.5, maze.colored_grid.shape[1], 1))
    plt.yticks(np.arange(-0.5, maze.colored_grid.shape[0], 1))

    # Remove tick labels
    ax.set_yticklabels([])
    ax.set_xticklabels([])

    # If filename is specified it saves it in the directory
    if filename is not None:
        try:
            os.mkdir('./mazes')
        except FileExistsError:
            pass
        plt.savefig('./mazes/' + str(filename) + '.png')
    # Otherwise it just shows the maze's image
    else:
        plt.show()


def drawTree(nodes, selected_node, filename, goal=False, prune=False):
    """
    Function that given nodes of the tree and the actual selected node draws it graphically.
    It can save it on trees directory or just show it on the app.
    :param nodes: nodes of the tree
    :param selected_node: actual selected node
    :param filename:
    :param goal:
    :param prune:
    :return:
    """
    # Settings
    tree = graphviz.Digraph(filename, format='png')
    directory = './trees/'

    # For each node of the tree
    for node in nodes:
        # If the node is the currently selected node
        if node == selected_node:
            # If the node is the goal
            if goal:
                tree.node(str(node.id), str(node.data), style="filled", color="green")
            # If the node is pruned
            elif prune:
                tree.node(str(node.id), str(node.data), style="filled", color="red")
            # If none of the previous checks is true
            else:
                tree.node(str(node.id), str(node.data), color="yellow")
        # All the other nodes in the tree are printed normally
        else:
            tree.node(str(node.id), str(node.data))

        # For every child of the current node
        for child in node.children:
            # If the parent node is pruned, then prune all its children
            if prune and node == selected_node:
                tree.node(str(child.id), str(child.data), style="filled", color="red")
            else:
                tree.node(str(child.id), str(child.data))
            # Create edge
            tree.edge(str(node.id), str(child.id))

    # Save tree.png
    tree.render(directory=directory, view=False)

    # Saving image
    os.remove(directory + filename + ".gv")
    os.rename(directory + filename + ".gv.png", directory + filename + ".png")


def images_cleanup():
    """
    Function that deletes all the images previously saved in the directories mazed and trees
    """
    try:
        for file in os.listdir('./trees'):
            os.remove('./trees/' + file)
        for file in os.listdir('./mazes'):
            os.remove('./mazes/' + file)
    except FileNotFoundError:
        pass


def changeImage(tree_label, maze_label):
    """
    Function that changes the image currently showed in the windows.
    It shows the next image in ascending order
    :param tree_label: the label containing tree images
    :param maze_label: the label containing maze images
    """
    # This function modifies the index of the current images
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
        pass

    # Index update
    curr_image += 1


def resizeImage(img, max_width, max_height):
    """
    Function that resizes the image if it exceeds maximum width and height
    :param img: the image to resize
    :param max_width: the maximum width the image should not exceed
    :param max_height: the maximum height the image should not exceed
    :return: resized image
    """

    # Current width and height of the image
    width, height = img.size

    # If the image sizes exceeds the limit the function resizes it
    if width > max_width or height > max_height:
        ratio = min(max_width / width, max_height / height)
        new_size = tuple(int(dimension * ratio) for dimension in img.size)

        # Actual resize
        img = img.resize(new_size, Image.ANTIALIAS)

    return img


def showImage(path, label):
    """
    Function that open, resizes and shows an image in a given label
    :param path: path of the image to open
    :param label: label in which to show the image
    """
    # Opening and resizing image
    img = resizeImage(Image.open(path), 700, 700)
    # Converting in tkinter format
    photo_image = ImageTk.PhotoImage(img)

    # Showing the image on the given label
    label.config(image=photo_image)
    label.image = photo_image
