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


class ConsoleManager(tk.Frame):
    def __init__(self, master, queue):
        tk.Frame.__init__(self, master)
        self.console_field = tk.Text(self, state=tk.DISABLED)
        self.console_field.pack(side=tk.TOP, fill=tk.Y, expand=1)
        self.command_runner = CommandRunner(self, queue)
        self.command_runner.pack(side=tk.TOP, fill=tk.X)
        self.queue = queue
        self.after(1000, lambda: self.load_from_queue())

    def load_from_queue(self):
        new_printable = self.queue.print_queue.get(wait_for_content=False)
        if new_printable:
            self.console_field.insert(tk.END, new_printable)
            print("successfully called!")
        self.after(1000, lambda: self.load_from_queue())
        print("called!")