import tkinter as tk
import os
from pathlib import Path
from gui.cells import Cell
from random import choice, randint


__author__ = "6666888, Neuperti, 7157367, Seiffert"
__credit__ = "immense time pressure"
__email__ = "s8978466@stud.uni-frankfurt.de"


IMAGE_WIDTH = 1000
DEFAULT_IMAGE = "blank.png"


def image_in_good_size(image, pixel_height, screen_height, images_to_fit_in=1):
    image = image.zoom(int(screen_height * .9) // 100)
    image = image.subsample(images_to_fit_in * pixel_height // 100)
    return image


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
        self.cells = dict()
        self.size = size
        self.queue = queue
        self.images = dict()
        self.screen_width = master.winfo_screenwidth()
        self.screen_height = master.winfo_screenheight()
        self.update_size(size)
        self.cell_function = None
        self.after(1000, self.check_print_queue)

    def check_print_queue(self):
        draw_queue_content = self.queue.draw_queue.get(wait_for_content=False)
        if draw_queue_content:
            if type(draw_queue_content) is tuple:
                # draw field:
                self.draw(*draw_queue_content)
            else:
                # change size:
                self.update_size(int(draw_queue_content))
        remaining_time = self.queue.time_queue.get(wait_for_content=False)
        self.queue.time_queue.clear()
        if remaining_time:
            self.master.player_manager.countdown.configure(
                text="remaining time:" + str(remaining_time).split(".")[0] + " secs"
            )
        self.master.player_manager.player_sidebar.update_player_switches()
        self.after(1000, self.check_print_queue)

    def update_size(self, size):
        """generates grid of cells"""
        image_filenames = os.listdir(absolute_path("/images"))
        for filename in image_filenames:
            # adapts image depending on grid size and screen size
            image = tk.PhotoImage(file=absolute_path("/images/" + filename))
            image = image_in_good_size(image, IMAGE_WIDTH, self.screen_height, size)
            self.images[filename] = image
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
                    self.cells[(x, y)] = Cell(self, self.images[DEFAULT_IMAGE], (x, y))
                self.cells[(x, y)].grid(row=x, column=y)

    def draw(self, standard_image: str, *set_image_doubles):
        """updates the images of cells which changed"""
        all_cell_coordinates = set()
        # set_image_doubles are
        for image_name, coordinates in set_image_doubles:
            all_cell_coordinates |= coordinates
            for coordinate in coordinates:
                if 0 not in coordinate:  # assuring, that labels are not regarded as proper cells
                    if self.cells[coordinate].image is not self.get_image(image_name):
                        self.cells[coordinate].update_image(self.get_image(image_name))
        for coordinate in set(self.cells.keys()) - all_cell_coordinates:
            if 0 not in coordinate:  # assuring, that labels are not regarded as proper cells
                self.cells[coordinate].update_image(self.get_image(standard_image))

    def get_image(self, image_class):
        image = self.images["blank.png"]
        grass = [
            self.images["grass1.png"],
            self.images["grass2.png"],
            self.images["grass3.png"],
            self.images["grass4.png"],
        ]
        goat = [
            self.images["goat1.png"],
            self.images["goat2.png"],
            self.images["goat3.png"],
        ]
        lava_horizontal = [self.images["lava.png"]]
        lava_vertical = [self.images["lava.png"]]
        lava_end_up = [self.images["lava.png"]]
        lava_end_down = [self.images["lava.png"]]
        lava_end_right = [self.images["lava.png"]]
        lava_end_left = [self.images["lava.png"]]
        stone_on_grass = [self.images["stone_grass.png"]]
        stone_on_lava = [self.images["stone_lava.png"]]
        stone_on_goat = [self.images["stone_goat.png"]]
        if image_class == "grass":
            if randint(0, 20) == 1:
                image = choice(goat)
            else:
                image = choice(grass)
        elif image_class == "lava":
            image = choice(lava_horizontal)
        elif image_class == "stone_lava":
            image = choice(stone_on_lava)
        elif image_class == "stone_grass":
            image = choice(stone_on_grass)
        return image


if __name__ == "__main__":
    """for testing only"""
    root = tk.Tk()
    test_grid = Grid(root, None)
    test_grid.pack()
    test_grid.draw("grass.png", ("goat.png", {(2, 4), (8, 2)}), ("stone_grass.png", {(1, 1), (5, 5)}),
                   ("lava.png", {(3, 4), (3, 5), (3, 7)}), ("stone_lava.png", {(3, 6)}))
    root.mainloop()
