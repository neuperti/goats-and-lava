import tkinter as tk

from gui.grid import Grid
from gui.player_manager import PlayerManager
from gui.grid import absolute_path
from gui.console_manager import ConsoleManager


class MainWindow(tk.Tk):
    def __init__(self, board, queue):
        tk.Tk.__init__(self)
        self.tk.call('wm', 'iconphoto', self._w, tk.PhotoImage(file='images/goat_icon.png'))
        self.title("Goats & Lava")
        self.board = board
        self.queue = queue
        self.grid = Grid(self, queue)
        self.player_manager = PlayerManager(self, queue, self.grid)
        self.player_manager.pack(side=tk.LEFT, fill=tk.Y)
        self.grid.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.console_manager = ConsoleManager(self, queue)
        self.console_manager.pack(side=tk.LEFT, fill=tk.Y)

    def finish_initialisation(self):
        self.player_manager.finish_initialisation()
        self.grid.cell_function = lambda coordinates: (
            self.queue.append("bb " + str(coordinates[0]) + " " + str(coordinates[1]))
        )
