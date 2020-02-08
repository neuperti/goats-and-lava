import tkinter as tk
import threading


__author__ = "6666888, Neuperti, 7157367, Seiffert"
__credit__ = "immense time pressure"
__email__ = "s8978466@stud.uni-frankfurt.de"


def crack_lava_rim_window(list_of_return_values):
    pass


def crack_lava_rim(coordinate, window):
    return_values = []
    threading.Thread(target=lambda *args: crack_lava_rim_window(return_values)).start()
    while not return_values:
        pass
    return return_values


def crack_lava_rim_window(list_of_return_values, coordinate):
    pass


class AskForDirection(tk.Toplevel):
    def __init__(self, direction):
        tk.Toplevel.__init__(self)
        self.wm_title("Lava Rim Direction")
        tk.Label(
            self,
            text="In which direction would you like to rip the garden open?"
        ).pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        top_button = tk.Button(self, text="^",
                               command=lambda *args: direction.append("n"))
        top_button.pack(side=tk.TOP, fill=tk.X)
        middle_row = tk.Frame(self)
        middle_row.pack(side=tk.TOP, fill=tk.X)
        left_button = tk.Button(middle_row, text="<",
                                command=lambda *args: direction.append("w"))
        left_button.pack(side=tk.LEFT, fill=tk.X, expand=.5)
        right_button = tk.Button(middle_row, text=">",
                                 command=lambda *args: direction.append("o"))
        right_button.pack(side=tk.LEFT, fill=tk.X, expand=.5)
        bottom_button = tk.Button(self, text="v",
                                  command=lambda *args: direction.append("s"))
        bottom_button.pack(side=tk.TOP, fill=tk.X)


class AskForLength(tk.Toplevel):
    def __init__(self, length):
        tk.Toplevel.__init__(self)
        self.wm_title("Lava Rim Length")
        tk.Label(
            self,
            text="How long would you like your rim to go?"
        ).pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        tk.Button(
            self,
            text="Length 3",
            command=lambda *args: (length.append(3))
        ).pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        tk.Button(
            self,
            text="Length 4",
            command=lambda *args: (length.append(4))
        ).pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        tk.Button(
            self,
            text="Length 5",
            command=lambda *args: (length.append(5))
        ).pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        tk.Button(
            self,
            text="Length 6",
            command=lambda *args: (length.append(6))
        ).pack(side=tk.TOP, fill=tk.X)


def make_command_from_lists(coordinates, direction_list, length_list, queue,
                            ask_for_direction_window, ask_for_length_window):
    while not direction_list or not length_list:
        pass
    queue.append(return_values[0])

    command = (
        "s+ "
        + str(coordinates[0])
        + " " + str(coordinates[1])
        + " " + str(length_list[0])
        + " " + direction_list[0]
    )
    ask_for_length_window.destroy()
    ask_for_direction_window.destroy()
    print(command)
    queue.append(command)


def crack_lava_rim(coordinate, queue):
    print("entered parallel thread.")
    direction_list = list()
    ask_for_direction_window = AskForDirection(direction_list)
    length_list = list()
    ask_for_length_window = AskForLength(length_list)
    threading.Thread(target=lambda *args: make_command_from_lists(coordinate,
                                                                  direction_list,
                                                                  length_list, queue,
                                                                  ask_for_direction_window,
                                                                  ask_for_length_window)).start()
