import tkinter as tk

from gui.options_window import OptionsWindow

__author__ = "6666888, Neuperti, 7157367, Seiffert"
__credit__ = "immense time pressure"
__email__ = "s8978466@stud.uni-frankfurt.de"


class PlayerAdder(tk.Frame):
    """A class for adding players"""
    def __init__(self, master, queue):
        """Initializes the class"""
        tk.Frame.__init__(self, master)
        text_field = tk.Entry(self)
        text_field.pack(side=tk.LEFT, fill=tk.X, expand=1)
        text_validator = tk.Button(
            self,
            text="Add Player",
            command=lambda *args: master.player_sidebar.add_player(
                text_field.get()
            ) or text_field.delete(0, tk.END)
        )
        text_validator.pack(side=tk.LEFT)


class StoppingManager(tk.Frame):
    """A class for exiting or restarting the game"""
    def __init__(self, master, queue):
        """Initializes the class"""
        tk.Frame.__init__(self, master)
        tk.Button(
            self,
            text="Exit",
            command=lambda *args: queue.append("gq")
        ).pack(side=tk.LEFT, fill=tk.X, expand=.5)
        tk.Button(
            self,
            text="Restart",
            command=lambda *args: queue.append("gr")
        ).pack(side=tk.LEFT, fill=tk.X, expand=.5)


class SetupFinisher(tk.Frame):
    """A class for finishing the setting-up-process"""
    def __init__(self, master, queue):
        """Initializes the class"""
        tk.Frame.__init__(self, master)
        setup_finisher = tk.Button(
            self,
            text="Finish setting up the neighborhood",
            command=lambda *args: (
                master.master.finish_initialisation() if queue.append("if") else None
            )
        )
        setup_finisher.pack(side=tk.TOP, fill=tk.X)


class SizeChanger(tk.Frame):
    """A class for changing the dimensions of the grid"""
    def __init__(self, master, queue):
        """Initializes the class"""
        tk.Frame.__init__(self, master)
        confirm_size = tk.Button(self, text="Change size:")
        confirm_size.pack(side=tk.LEFT)
        size_input_field = tk.Entry(self)
        size_input_field.pack(side=tk.LEFT, fill=tk.X, expand=1)
        confirm_size.configure(
            command=lambda *args: queue.append("bs " + size_input_field.get())
        )


class PlayerSwitcher(tk.Frame):
    """A class for switching betwween players by clicking on their buttons"""
    def __init__(self, master, player_name):
        """Initializes the class"""
        tk.Frame.__init__(self, master)
        name_viewer = tk.Button(self, text=player_name, command=lambda *args: master.switch_player(
            player_name
        ))
        name_viewer.pack(side=tk.LEFT, fill=tk.X, expand=1)
        delete_button = tk.Button(self, text="X", command=lambda *args: master.remove_player(
            player_name
        ))
        delete_button.pack(side=tk.LEFT)
        self.delete_button = delete_button
        self.name_viewer = name_viewer


class ViewSwitcher(tk.Frame):
    """A class for switching betweeen offensive and defensive mode via button"""
    def __init__(self, master, queue):
        """Initializes the class"""
        self.view_mode = tk.StringVar()
        self.queue = queue
        tk.Frame.__init__(self, master)
        draw_defensive_mode = tk.Button(
            self,
            text="defensive mode",
            command=lambda *args: queue.append("dd")
        )
        draw_offensive_mode = tk.Button(
            self,
            text="offensive mode",
            command=lambda *args: queue.append("do")
        )
        draw_defensive_mode.pack(side=tk.LEFT, fill=tk.X, expand=.5)
        draw_offensive_mode.pack(side=tk.LEFT, fill=tk.X, expand=.5)


class PlayerSidebar(tk.Frame):
    """A class managing the sidebar of players"""
    def __init__(self, master, queue, grid, board):
        """Initializes the class"""
        tk.Frame.__init__(self, master)
        self.queue = queue
        self.board = board
        self.grid = grid
        self.player_switchers = dict()

    def give_focus_to_player(self, player_switcher):
        """Switches the visual focus when player button is pressed"""
        for switcher in self.player_switchers.values():
            switcher.name_viewer.config(relief=tk.RAISED)
            switcher.name_viewer.config(state=tk.NORMAL)
        try:
            player_switcher.name_viewer.config(relief=tk.FLAT)
            player_switcher.name_viewer.config(state=tk.DISABLED)
        except:
            pass

    def update_player_switches(self):
        """Removes players who have been deleted behind the scenes from the player sidebar."""
        active_player = set(self.board.player_fleets.keys())
        deleted_players = set(self.player_switchers.keys()) - active_player
        for deleted_player in deleted_players:
            self.player_switchers[deleted_player].pack_forget()
            del self.player_switchers[deleted_player]
            self.give_focus_to_player(PlayerSwitcher(self, ""))

    # verwaltet Liste von Spielernamen und Buttons
    # Bei klick von button: self.queue.append("ps " + button.text)
    def add_player(self, player_name):
        """Adds a new player in the setup process"""
        if self.queue.append("p+ " + player_name):
            player_switcher = PlayerSwitcher(self, player_name)
            player_switcher.pack(side=tk.TOP, fill=tk.X)
            self.player_switchers[player_name] = player_switcher
            self.give_focus_to_player(player_switcher)

    def remove_player(self, player_name):
        """removes a player in the setup process"""
        if self.queue.append("p- " + player_name):
            self.player_switchers[player_name].pack_forget()
            del self.player_switchers[player_name]
            self.give_focus_to_player(PlayerSwitcher(self, ""))

    def switch_player(self, player_name):
        """switches between players in the setup process"""
        if self.queue.append("ps " + player_name):
            self.give_focus_to_player(self.player_switchers[player_name])


class PlayerManager(tk.Frame):
    """A class for managing the player sidebar and the buttons below"""
    def __init__(self, master, queue, board, grid):
        """Initializes the class"""
        tk.Frame.__init__(self, master)
        self.grid = grid
        self.queue = queue
        self.board = board
        self.player_sidebar = PlayerSidebar(self, queue, grid, board)
        self.player_sidebar.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.add_button = PlayerAdder(self, queue)
        self.add_button.pack(side=tk.TOP, fill=tk.X)
        self.size_changer = SizeChanger(self, queue)
        self.size_changer.pack(side=tk.TOP, fill=tk.X)
        self.view_switcher = ViewSwitcher(self, queue)
        self.view_switcher.pack(side=tk.TOP, fill=tk.X)
        self.setup_finisher = SetupFinisher(self, queue)
        self.setup_finisher.pack(side=tk.TOP, fill=tk.X)
        self.stop_manager = StoppingManager(self, queue)
        self.stop_manager.pack(side=tk.TOP, fill=tk.X)
        self.options_caller = tk.Button(
            self,
            text="Options...",
            command=lambda *args: OptionsWindow(self.queue)
        )
        self.options_caller.pack(side=tk.TOP, fill=tk.X)
        self.countdown = tk.Label(text="remaining time: 30 secs")
        self.countdown.pack(side=tk.TOP, fill=tk.X)

    def finish_initialisation(self):
        """Is called by the SetupFinisher and removes the initialization buttons"""
        self.add_button.pack_forget()
        self.setup_finisher.pack_forget()
        self.size_changer.pack_forget()
        self.options_caller.pack_forget()
        for player_switcher in self.player_sidebar.player_switchers.values():
            player_switcher.delete_button.pack_forget()
