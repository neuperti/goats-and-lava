import tkinter as tk


class Cell(tk.Button):
    def __init__(self, master, image: tk.PhotoImage, coordinates, callable_if_clicked):
        tk.Button.__init__(self, master, image=image, padx=0, pady=0, bd=0, relief=tk.FLAT,
                           highlightthickness=0, command=callable_if_clicked)
        self.coordinates = coordinates
        self.click_funcion = callable_if_clicked
            
#### to send to grid
if __name__ == "__main__":
    def test_function():
        print("YAY!")
    import os
    from pathlib import Path
    base_folder = os.path.dirname(__file__)
    base_folder = Path(base_folder).parent
    base_folder = str(base_folder)
    image_path = base_folder + "/images/goat.png"
    root = tk.Tk()
    image = tk.PhotoImage(file=image_path)
    new_cell = Cell(root, image, (1, 2), test_function)
    new_cell.pack()
    root.mainloop()
    