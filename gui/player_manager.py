import tkinter as tk


class CommandRunner(tk.Frame):
    def __init__(self, master, queue):
        tk.Frame.__init__(self, master)
        text_field = tk.Entry(self)
        text_field.pack(side=tk.LEFT, fill=tk.X, expand=1)
        text_validator = tk.Button(
            self,
            text="Run Command (e.g. ?c)",
            command=lambda *args: (
                queue.append(text_field.get()) or text_field.delete(0, tk.END)
            )
        )
        text_validator.pack(side=tk.LEFT)


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
        self.name_viewer = name_viewer


class PlayerSidebar(tk.Frame):
    def __init__(self, master, queue, grid):
        tk.Frame.__init__(self, master)
        self.queue = queue
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

    # verwaltet Liste von Spielernamen und Buttons
    # Bei klick von button: self.queue.append("ps " + button.text)
    def add_player(self, player_name):
        player_switcher = PlayerSwitcher(self, player_name)
        player_switcher.pack(side=tk.TOP, fill=tk.X, expand=1)
        self.player_switchers[player_name] = player_switcher
        self.queue.append("p+ " + player_name)
        self.give_focus_to_player(player_switcher)

    def remove_player(self, player_name):
        self.player_switchers[player_name].pack_remove()
        del self.player_switchers[player_name]
        self.queue.append("p- " + player_name)
        self.give_focus_to_player(None)

    def switch_player(self, player_name):
        # highlighted selected player
        self.give_focus_to_player(self.player_switchers[player_name])
        self.queue.append("ps " + player_name)


class PlayerManager(tk.Frame):
    # Bekommt queue übergeben und gibt die an PlayerSidebar weiter
    # Enthält PlayerSidebar
    # Ethält Eingabefeld und Plus-Button
    # Bei Klick auf Plus:
    #    add "p+ " + eingabewert in queue.
    def __init__(self, master, queue, grid):
        tk.Frame.__init__(self, master)
        self.grid = grid
        self.queue = queue
        self.player_sidebar = PlayerSidebar(self, queue, grid)
        self.player_sidebar.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.command_runner = CommandRunner(self, queue)
        self.command_runner.pack(side=tk.TOP, fill=tk.X)
        self.add_button = PlayerAdder(self, queue)
        self.add_button.pack(side=tk.TOP, fill=tk.X)

    def hide_add_button(self):
        # entfert add button
        # fügt stattdessen eine checkbox hinzu, die angibt, ob man im offensiven Modus ist
        # Hacken setzen:
        #    add "do" to queue
        # Hacken entfernen:
        #    add "dd" to queue
        # Muss grid beim wechseln des Modus ändern
        pass
