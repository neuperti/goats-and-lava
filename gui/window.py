import tkinter as tk

from gui.grid import Grid
from gui.player_manager import PlayerManager


class MainWindow(tk.Tk):
    def __init__(self, board, queue):
        tk.Tk.__init__(self)
        self.board = board
        self.queue = queue
        self.grid = Grid(self, queue)
        self.player_manager = PlayerManager(self, queue, self.grid)
        self.player_manager.pack(side=tk.LEFT, fill=tk.Y)
        self.grid.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
