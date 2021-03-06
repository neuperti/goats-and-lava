import tkinter as tk
import threading
from logic.main_cmd import start_game

from gui.grid import Grid
from gui.player_manager import PlayerManager
from gui.grid import absolute_path
from gui.console_manager import ConsoleManager
from gui.grid import image_in_good_size
from gui.place_lava_dialog import crack_lava_rim

__author__ = "6666888, Neuperti, 7157367, Seiffert"
__credit__ = "immense time pressure"
__email__ = "s8978466@stud.uni-frankfurt.de"


class MainWindow(tk.Tk):
    """A class for the main Window"""
    def __init__(self, board, queue):
        """Initializes the class"""
        tk.Tk.__init__(self)
        self.board = board
        board.window = self
        self.queue = queue
        self.player_manager = None
        self.console_manager = None
        self.tk.call('wm', 'iconphoto', self._w, tk.PhotoImage(
            file=absolute_path('/images/goat_icon.png')
        ))
        self.title("Goats & Lava")
        self.intro_button = IntroButton(self, lambda: self.after_intro(board, queue))
        self.intro_button.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.skip_intro_button = SkipIntroButton(self, lambda: self.after_intro(board, queue))
        self.skip_intro_button.pack(fill=tk.X)

    def after_intro(self, board, queue):
        """The part of __init__ which launches after the intro is displayed"""
        self.grid = Grid(self, queue)
        self.grid.cell_function = lambda coordinates: crack_lava_rim(coordinates, self.queue)
        self.player_manager = PlayerManager(self, queue, board, self.grid)
        self.console_manager = ConsoleManager(self, queue)
        self.player_manager.pack(side=tk.LEFT, fill=tk.Y)
        self.grid.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.console_manager.pack(side=tk.LEFT, fill=tk.Y)
        self.intro_button.pack_forget()
        threading.Thread(target=lambda *args: start_game(queue, board)).start()
        tk.Toplevel().destroy()  # to can use tk.Toplevel in other threads, we must use it from
        # main thread once.

    def finish_initialisation(self):
        """Handles the finishing of the initialization process"""
        self.player_manager.finish_initialisation()
        self.grid.cell_function = lambda coordinates: (
            self.queue.append("bb " + str(coordinates[0]) + " " + str(coordinates[1]))
        )


class IntroButton(tk.Button):
    """A class for the button which displayes the intro images"""
    def __init__(self, master, after_intro):
        self.counter = 0
        self.after_intro = after_intro
        self.loading_screen = tk.PhotoImage(file=absolute_path("/intro_images/loading_screen.png"))
        self.loading_screen = image_in_good_size(self.loading_screen, self.loading_screen.height(),
                                                 master.winfo_screenheight()*.9)
        self.intro_images = []
        for i in range(1, 8):
            image_path = absolute_path("/intro_images/" + str(i) + ".png")
            file = tk.PhotoImage(file=image_path)
            file = image_in_good_size(file, file.height(), master.winfo_screenheight()*.9)
            self.intro_images.append(file)
        self.title_screen = tk.PhotoImage(file=absolute_path("/intro_images/title_screen.png"))
        self.title_screen = image_in_good_size(self.title_screen, self.title_screen.height(),
                                               master.winfo_screenheight()*.9)
        tk.Button.__init__(self, master, image=self.title_screen, padx=0, pady=0, bd=0,
                           relief=tk.FLAT, highlightthickness=0, command=self.button_pressed)

    def button_pressed(self):
        """Handles the transition of images of the button"""
        if self.counter < 7:
            self.configure(image=self.intro_images[self.counter])
            self.counter += 1
        else:
            self.configure(image=self.loading_screen)
            self.master.skip_intro_button.pack_forget()
            self.master.update()
            self.after_intro()


class SkipIntroButton(tk.Button):
    """Lets the user skip the intro"""
    def __init__(self, master, after_intro):
        self.after_intro = after_intro
        tk.Button.__init__(self, master, text="I am impatient and want to skip the intro. :(",
                           command=self.button_pressed)

    def button_pressed(self):
        """Is called when button is pressed"""
        self.master.intro_button.counter = 7
        self.master.intro_button.button_pressed()


if __name__ == "__main__":
    """For testing only"""
    new_window = MainWindow(None, None)
    new_window.mainloop()

