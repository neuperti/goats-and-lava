import threading
import tkinter as tk

from gui.window import MainWindow
from logic.main_cmd import start_game
from logic.main_cmd import Board
from queue import Queue


QUEUE = Queue()


def start_window():
    board = Board(QUEUE)
    board.intro = ""
    main_window = MainWindow(board, QUEUE)
    main_window.mainloop()


if __name__ == "__main__":
    start_window()
