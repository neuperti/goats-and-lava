import tkinter as tk

from gui.grid import Grid
from gui.player_manager import PlayerManager


class MainWindow(tk.Tk):
    def __init__(self, board, queue):
        tk.Tk.__init__(self)
        self.board = board
        self.queue = queue
        self.grid = Grid(queue)
        self.player_manager = PlayerManager()