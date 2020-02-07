import tkinter as tk
from tkinter import messagebox
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
