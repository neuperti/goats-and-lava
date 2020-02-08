import tkinter as tk
import threading


def crack_lava_rim_window(list_of_return_values):
    pass


def crack_lava_rim(coordinate, window):
    return_values = []
    threading.Thread(target=lambda *args: crack_lava_rim_window(return_values)).start()
    while not return_values:
        pass
    return return_values
