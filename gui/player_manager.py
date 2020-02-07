import tkinter as tk


class PlayerAdder(tk.Frame):
    def __init__(self, master, queue):
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


class SetupFinisher(tk.Frame):
    def __init__(self, master, queue):
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
    def __init__(self, master, queue):
        tk.Frame.__init__(self, master)
        confirm_size = tk.Button(self, text="Change size:")
        confirm_size.pack(side=tk.LEFT)
        size_input_field = tk.Entry(self)
        size_input_field.pack(side=tk.LEFT, fill=tk.X, expand=1)
        confirm_size.configure(
            command=lambda *args: queue.append("bs " + size_input_field.get())
        )


class PlayerSwitcher(tk.Frame):
    def __init__(self, master, player_name):
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
    def __init__(self, master, queue):
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
    def __init__(self, master, queue, grid, board):
        tk.Frame.__init__(self, master)
        self.queue = queue
        self.board = board
        self.grid = grid
        self.player_switchers = dict()

    def give_focus_to_player(self, player_switcher):
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
        if self.queue.append("p+ " + player_name):
            player_switcher = PlayerSwitcher(self, player_name)
            player_switcher.pack(side=tk.TOP, fill=tk.X)
            self.player_switchers[player_name] = player_switcher
            self.give_focus_to_player(player_switcher)

    def remove_player(self, player_name):
        if self.queue.append("p- " + player_name):
            self.player_switchers[player_name].pack_forget()
            del self.player_switchers[player_name]
            self.give_focus_to_player(PlayerSwitcher(self, ""))

    def switch_player(self, player_name):
        if self.queue.append("ps " + player_name):
            self.give_focus_to_player(self.player_switchers[player_name])


class PlayerManager(tk.Frame):
    # Bekommt queue übergeben und gibt die an PlayerSidebar weiter
    # Enthält PlayerSidebar
    # Ethält Eingabefeld und Plus-Button
    # Bei Klick auf Plus:
    #    add "p+ " + eingabewert in queue.
    def __init__(self, master, queue, board,  grid):
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
        self.countdown = tk.Label(text="remaining time: 30 secs")
        self.countdown.pack(side=tk.TOP, fill=tk.X)

    def finish_initialisation(self):
        self.add_button.pack_forget()
        self.setup_finisher.pack_forget()
        self.size_changer.pack_forget()
        for player_switcher in self.player_sidebar.player_switchers.values():
            player_switcher.delete_button.pack_forget()
        # entfert add button
        # fügt stattdessen eine checkbox hinzu, die angibt, ob man im offensiven Modus ist
        # Hacken setzen:
        #    add "do" to queue
        # Hacken entfernen:
        #    add "dd" to queue
        # Muss grid beim wechseln des Modus ändern
        pass
