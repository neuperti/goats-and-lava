import tkinter as tk
import os
from pathlib import Path
from gui.cells import Cell


IMAGE_WIDTH = 1000


def absolute_path(relative_path):
    """turns a relative path (with leading '/') into an absolute one"""
    base_folder = os.path.dirname(__file__)
    base_folder = str(Path(base_folder).parent)
    absolute_path_name = base_folder + relative_path
    return absolute_path_name


class Grid(tk.Frame):
    """a class which manages the visual appearence of the grid"""
    def __init__(self, master, queue, size=10):
        """initializes the class"""
        tk.Frame.__init__(self, master)
        self.cell_function = None
        self.cells = dict()
        self.size = size
        self.queue = queue
        self.images = dict()
        self.screen_width = master.winfo_screenwidth()
        self.screen_height = master.winfo_screenheight()
        image_filenames = os.listdir(absolute_path("/images"))
        for filename in image_filenames:
            image = tk.PhotoImage(file=absolute_path("/images/" + filename))
            image = image.zoom(int(self.screen_height * .9) // 100)
            image = image.subsample(size*IMAGE_WIDTH//100)  # adapts image depending on grid size and screen size
            self.images[filename] = image
        print(self.images)
        self.update_size(size)
        self.after(1000, self.check_print_queue)

    def check_print_queue(self):
        draw_queue_content = self.queue.draw_queue.get(wait_for_content=False)
        print("checked!")
        if draw_queue_content:
            print("checked successfully!")
            self.draw(*draw_queue_content[0])
        self.after(1000, self.check_print_queue)

    def update_size(self, size):
        """generates grid of cells"""
        for cell in list(self.cells.keys()):  # remove old cells
            self.cells[cell].grid_remove()
            del self.cells[cell]
        self.size = size
        for x in range(0, size + 1):
            for y in range(0, size + 1):
                if x == 0 and y != 0:
                    self.cells[(x, y)] = tk.Label(self, text=str(y))
                elif y == 0 and x != 0:
                    self.cells[(x, y)] = tk.Label(self, text=str(x))
                elif x == 0 and y == 0:
                    self.cells[(x, y)] = tk.Label(self, text=str())
                else:
                    self.cells[(x, y)] = Cell(self, self.images["goat.png"], (x, y), self.cell_function)
                self.cells[(x, y)].grid(row=x, column=y)

    def change_function_of_cells(self, function):
        """changes the cell function when pressed"""
        self.cell_function = function

    def draw(self, standard_image: str, *set_image_doubles):
        """updates the images of cells which changed"""
        print("wuwu", self, standard_image, set_image_doubles)
        all_cell_coordinates = set()
        standard_image = self.images[standard_image]
        # set_image_doubles are
        for image_name, coordinates in set_image_doubles:
            all_cell_coordinates |= coordinates
            for coordinate in coordinates:
                if 0 not in coordinate:  # assuring, that labels are not regarded as proper cells
                    if self.cells[coordinate].image is not self.images[image_name]:
                        self.cells[coordinate].update_image(self.images[image_name])
        for coordinate in set(self.cells.keys()) - all_cell_coordinates:
            if 0 not in coordinate:  # assuring, that labels are not regarded as proper cells
                self.cells[coordinate].update_image(standard_image)



if __name__ == "__main__":
    """for testing only"""
    root = tk.Tk()
    test_grid = Grid(root, None)
    test_grid.pack()
    test_grid.draw("grass.png", ("goat.png", {(2, 4), (8, 2)}), ("stone_grass.png", {(1, 1), (5, 5)}),
                   ("lava.png", {(3, 4), (3, 5), (3, 7)}), ("stone_lava.png", {(3, 6)}))
    root.mainloop()