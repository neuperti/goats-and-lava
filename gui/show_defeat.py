import tkinter as tk
from tkinter import messagebox
import sys

from gui.grid import absolute_path


class DeathScreen(tk.Toplevel):
    def __init__(self, message, extended_message, image_path):
        tk.Toplevel.__init__(self)
        self.wm_title(message)
        self.image = tk.PhotoImage(file=absolute_path("/" + image_path))
        tk.Label(self, image=self.image).pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        tk.Label(self, text=extended_message).pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        tk.Button(self, text="Yay!", command=self.destroy).pack(side=tk.TOP, fill=tk.X)


def die_from_timer(player_name):
    DeathScreen(
        "A slug has ended.",
        str(player_name) + " took so long to take their turn that god decided it might be enough.",
        "icon/slug.png"
    )


def die_from_being_killed(player_name):
    DeathScreen(
        str(player_name) + " died!",
        str(player_name) + " died from being stoned. Such a stoner!",
        "icon/stoner.png"
    )


def die_from_being_a_coward(player_name):
    screen = DeathScreen(
        str(player_name) + " is a coward worth spitting at!",
        (
            str(player_name) + " is a looser because they couldn't stand the preasure and thus\
stopped!\nEveryone but this monster thus is a winner and allowed to celebrate!"
        ),
        "icon/coward.png"
    )
    screen.after(10_000, lambda *args: sys.exit())