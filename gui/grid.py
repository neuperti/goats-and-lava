import tkinter as tk
from PIL import Image
from PIL import ImageTk

SCREEN_HEIGHT = 0  # calculate this!


class Grid(tk.Frame):
    def __init__(self, queue, size=10):
        self.update_size(size)
        self.queue = queue
        #tkiniit aufrufen

    def update_size(self, size):
        self.cell_size = 0  # berechnet zellengröße
        self.cells = dict()
        self.images = dict()
        self.size = size

    def change_function_of_cells(self, function):
        # ändert die an jede Zelle angebundene Funktion zu function
        # platzieren (init), nichts (defensiver modus), "bb " + "".join(coordinate)
        # in queue reihen (offensiver modus)
        pass

    def draw(self, standard_image: str, *set_image_doubles):
        # set_image_doubles are
        pass