import tkinter as tk


class PlayerSidebar(tk.Frame):
    def __init__(self, queue, grid):
        tk.Frame.__init__(self)
        self.queue = queue
        self.grid = grid

    # verwaltet Liste von Spielernamen und Buttons
    # Bei klick von button: self.queue.append("ps " + button.text)
    def add_player(self, player_name):
        pass

    def remove_player(self, player_name):
        pass

    def update_current_player(self, player_name):
        # highlighted selected player
        pass


class PlayerManager(tk.Frame):
    # Bekommt queue übergeben und gibt die an PlayerSidebar weiter
    # Enthält PlayerSidebar
    # Ethält Eingabefeld und Plus-Button
    # Bei Klick auf Plus:
    #    add "p+ " + eingabewert in queue.

    def hide_add_button(self):
        # entfert add button
        # fügt stattdessen eine checkbox hinzu, die angibt, ob man im offensiven Modus ist
        # Hacken setzen:
        #    add "do" to queue
        # Hacken entfernen:
        #    add "dd" to queue
        # Muss grid beim wechseln des Modus ändern
        pass
