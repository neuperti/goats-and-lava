import tkinter as tk

__author__ = "6666888, Neuperti, 7157367, Seiffert"
__credit__ = "immense time pressure"
__email__ = "s8978466@stud.uni-frankfurt.de"


class CommandRunner(tk.Frame):
    """A class which handels input for the comand-line-like interface"""
    def __init__(self, master, queue):
        """Initializes the class"""
        tk.Frame.__init__(self, master)
        text_field = tk.Entry(self)
        text_field.pack(side=tk.LEFT, fill=tk.X, expand=1)
        text_validator = tk.Button(
            self,
            text="Run Command (e.g. ?c)",
            command=lambda *args: (
                queue.append(text_field.get()) and text_field.delete(0, tk.END)
            )
        )
        text_validator.pack(side=tk.LEFT)


class ConsoleManager(tk.Frame):
    """A class which combines the CommandRunner and rest of the interface"""
    def __init__(self, master, queue):
        """Initializes the class"""
        tk.Frame.__init__(self, master)
        self.console_field = tk.Text(self, state=tk.DISABLED)
        self.console_field.pack(side=tk.TOP, fill=tk.Y, expand=1)
        self.command_runner = CommandRunner(self, queue)
        self.command_runner.pack(side=tk.TOP, fill=tk.X)
        self.queue = queue
        self.after(1000, lambda: self.load_from_queue())

    def load_from_queue(self):
        """Handles displaying the queue commands"""
        new_printable = self.queue.print_queue.get(wait_for_content=False)
        if new_printable:
            self.console_field.configure(state=tk.NORMAL)
            self.console_field.insert(tk.END, "\n" + new_printable)
            self.console_field.see(tk.END)
            self.console_field.configure(state=tk.DISABLED)
        self.after(1000, lambda: self.load_from_queue())
