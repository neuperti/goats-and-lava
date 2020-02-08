import tkinter as tk


class OptionsWindow(tk.Toplevel):
    def __init__(self, queue):
        tk.Toplevel.__init__(self)
        self.queue = queue
        self.wm_title("Options for real MONSTERS")
        tk.Label(
            self,
            text="Options:"
        ).pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        one_shoot_per_ship_var = tk.IntVar()
        one_shoot_per_ship = tk.Checkbutton(
            self,
            text="One shoot per Lava rim - you and the boys decided to shoot it up together!",
            variable=one_shoot_per_ship_var
        )
        one_shoot_per_ship.pack(side=tk.TOP, fill=tk.X)
        rock_scattering_var = tk.IntVar()
        rock_scattering = tk.Checkbutton(
            self,
            text="Scattering - Shoot all rocks you got at one and scatter them!",
            variable=rock_scattering_var
        )
        rock_scattering.pack(side=tk.TOP, fill=tk.X)
        tk.Label(self, text="Seconds to think:").pack(side=tk.TOP, fill=tk.X)
        self.thinking_time = tk.Entry(self, text="30")
        self.thinking_time.pack(side=tk.TOP, fill=tk.X)
        close_button = tk.Button(
            self,
            text="Save my preferences.",
            command=lambda *args: self.save_options(
                one_shoot_per_ship=one_shoot_per_ship_var.get(),
                rock_scattering=rock_scattering_var.get()
            )
        )
        close_button.pack(side=tk.TOP, fill=tk.X)

    def save_options(self, one_shoot_per_ship, rock_scattering):
        if one_shoot_per_ship:
            self.queue.append("one_shoot_per_ship True")
        else:
            self.queue.append("one_shoot_per_ship False")
        if rock_scattering:
            self.queue.append("rock_scattering True")
        else:
            self.queue.append("rock_scattering False")
        self.queue.append("thinking_time " + self.thinking_time.get())
        self.destroy()
