from tkinter import *
from PIL import Image
from PIL import ImageTk

import random

r = 0
root = Tk()
image = Image.open("images/goat.png")
image = image.resize((50, 50), Image.ANTIALIAS)
photo = ImageTk.PhotoImage(image)

image2 = Image.open("images/goat2.png")
image2 = image2.resize((50, 50), Image.ANTIALIAS)
photo2 = ImageTk.PhotoImage(image2)
print("wuwu")
# photo2 = PhotoImage(file=r"C:\Users\HP\PycharmProjects\battleships\images\goat.png")
# photo = photo.zoom(20, 20)
for x in range(20):
    for y in range(20):
        i = Button(root, image=photo2, padx=0, pady=0, bd=0, relief=FLAT, highlightthickness=0)
        i.grid(row=x, column=y)
        if random.randint(1, 100) < 33:
            i.configure(image=photo)
print("wawa")

root.mainloop()