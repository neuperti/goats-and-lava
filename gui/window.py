import tkinter as tk

from gui.grid import Grid
from gui.player_manager import PlayerManager
from gui.grid import absolute_path
from gui.console_manager import ConsoleManager


class MainWindow(tk.Tk):
    def __init__(self, board, queue):
        tk.Tk.__init__(self)
        self.tk.call('wm', 'iconphoto', self._w, tk.PhotoImage(file=absolute_path('/images/goat_icon.png')))
        self.title("Goats & Lava")
        self.intro_button = IntroButton(self, lambda: self.after_intro(board, queue))
        self.intro_button.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def after_intro(self, board, queue):
        self.board = board
        self.queue = queue
        self.grid = Grid(self, queue)
        self.player_manager = PlayerManager(self, queue, board, self.grid)
        self.player_manager = PlayerManager(self, queue, self.grid)
        self.console_manager = ConsoleManager(self, queue)
        self.player_manager.pack(side=tk.LEFT, fill=tk.Y)
        self.grid.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.console_manager.pack(side=tk.LEFT, fill=tk.Y)
        self.intro_button.pack_forget()

    def finish_initialisation(self):
        self.player_manager.finish_initialisation()
        self.grid.cell_function = lambda coordinates: (
            self.queue.append("bb " + str(coordinates[0]) + " " + str(coordinates[1]))
        )


class IntroButton(tk.Button):
    def __init__(self, master, after_intro):
        self.counter = 1
        self.after_intro = after_intro
        self.loading_screen = tk.PhotoImage(file=absolute_path("/intro_images/loading_screen.png"))
        self.loading_screen = self.loading_screen.zoom(2)
        self.intro_images = []
        for i in range(1, 8):
            image_path = absolute_path("/intro_images/" + str(i) + ".png")
            file = tk.PhotoImage(file=image_path)
            file = file.zoom(2)
            self.intro_images.append(file)
        self.title_screen = tk.PhotoImage(file=absolute_path("/intro_images/title_screen.png"))
        self.title_screen = self.title_screen.zoom(2)
        tk.Button.__init__(self, master, image=self.title_screen, padx=0, pady=0, bd=0, relief=tk.FLAT,
                           highlightthickness=0, command=self.button_pressed)

    def button_pressed(self):
        if self.counter < 7:
            self.configure(image=self.intro_images[self.counter])
            self.counter += 1
        else:
            self.configure(image=self.loading_screen)
            self.after_intro





if __name__ == "__main__":
    """for testing only"""
    new_window = MainWindow(None, None)
    new_window.mainloop()

