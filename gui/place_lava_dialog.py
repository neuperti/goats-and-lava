import tkinter as tk
import threading


def crack_lava_rim_window(list_of_return_values, coordinate):
    pass


def crack_lava_rim(coordinate, queue):
    return_values = []
    threading.Thread(target=lambda *args: crack_lava_rim_window(return_values, coordinate)).start()
    while not return_values:
        pass
    queue.append(return_values[0])
