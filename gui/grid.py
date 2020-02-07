import tkinter as tk
import os
from pathlib import Path
from gui.cells import Cell


IMAGE_WIDH = 1000


def absolute_path(relative_path):
    """turns a relative path (with leading '/') into an absolute one"""
    base_folder = os.path.dirname(__file__)
    base_folder = str(Path(base_folder).parent)
    absolute_path = base_folder + relative_path
    return absolute_path

class Grid(tk.Frame):
    def __init__(self, master, queue, size=10):
        tk.Frame.__init__(self, master)
        self.cell_function = None
        self.cells = dict()
        self.size = size
        #os.
        self.queue = queue
        self.images = dict()
        # Images
        self.screen_width = master.winfo_screenwidth()
        self.screen_height = master.winfo_screenheight()
        print(self.screen_height)
        image_filenames = os.listdir(absolute_path("/images"))
        for filename in image_filenames:
            image = tk.PhotoImage(file=absolute_path("/images/" + filename))
            image = image.zoom(int(self.screen_height * .9) // 100)
            image = image.subsample(size//100*IMAGE_WIDH)  # adapts image depending on grid size and screen size
            self.images[filename] = image
        print(self.images)
        self.update_size(size)

    def update_size(self, size):
        """generates grid of cells"""
        for cell in list(self.cells.keys()):  # remove old cells
            self.cells[cell].grid_remove()
            del self.cells[cell]    
        self.size = size
        for x in range(1, size + 1):
            for y in range(1, size + 1):
                self.cells[(x, y)] = Cell(self, self.images["goat.png"], (x, y), self.cell_function)
                self.cells[(x, y)].grid(row=x-1, column=y-1)

    def change_function_of_cells(self, function):
        """changes the cell function when pressed"""
        # ändert die an jede Zelle angebundene Funktion zu function
        # platzieren (init), nichts (defensiver modus), "bb " + "".join(coordinate)
        # in queue reihen (offensiver modus)
        self.cell_function = function

    def draw(self, size,  standard_image: str, *set_image_doubles):
        # set_image_doubles are
        """for x in range(1, size + 1):
            for y in range(1, size + 1):"""
        pass

    def update_cell(self, coordinates, image):
        """updates the state of one cell"""
        self.cells[coordinates].image = image

    def test_function(self):
        """for testing only"""
        print("YAY!")


if __name__ == "__main__":
    """for testing only"""
    root = tk.Tk()
    image = tk.PhotoImage(file=absolute_path("/images/goat.png"))
    test_grid = Grid(root, None)
    test_grid.pack()
    root.mainloop()
