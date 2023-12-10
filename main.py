from random import choices, shuffle
import tkinter as tk
from tkinter import ttk

# Exceptions:
#  - if user add words insted of number in the password_len entry
#  - if user doens't choose any criteria
#  - copy button


class MainFrame(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        ## Basic settings
        # give focus to the frame
        self.focus_set()
        self.master = master
        self.style = ttk.Style(self.master)

        ## Variables
        self.password_len = tk.IntVar(value=8)
        self.password = tk.StringVar(value="Press Generate Password ...")
        self.upper = tk.BooleanVar(value=True)
        self.lower = tk.BooleanVar()
        self.number = tk.BooleanVar()
        self.symbol = tk.BooleanVar()
        # TODO: fix this using string module
        self.lowers = "".join(chr(i) for i in range(97, 123))
        self.uppers = "".join(ch.upper() for ch in self.lowers)
        self.numbers = "".join(chr(i) for i in range(48, 58))
        self.symbols = "@!#$%&^()*+"
        self.criteria = [self.upper, self.lower, self.number, self.symbol]
        # use join to this or maybe some claver way
        self.allchars = self.uppers + self.lowers + self.numbers + self.symbols
        self.strength_number = tk.IntVar(value=0)
        self.strength_status = tk.StringVar(value="weak")

        ## Widgets
        password_frame = ttk.Frame(self, padding=(5, 10))
        password_frame.pack(expand=True, fill=tk.BOTH)

        password_entry = ttk.Entry(password_frame, textvariable=self.password)
        copy_button = ttk.Button(
            password_frame, text="Copy", command=self.copy_password
        )
        password_entry.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)
        copy_button.pack(expand=True, fill=tk.BOTH)

        # Settings for password
        setting_frame = ttk.Frame(self, relief=tk.SUNKEN, padding=(5, 10))
        setting_frame.pack(expand=True, fill=tk.BOTH, pady=10)

        # settings
        uppercase_checkbutton = ttk.Checkbutton(
            setting_frame, variable=self.upper, text="Uppercase"
        )
        lowercase_checkbutton = ttk.Checkbutton(
            setting_frame, variable=self.lower, text="Lowercase"
        )
        number_checkbutton = ttk.Checkbutton(
            setting_frame, variable=self.number, text="Numbers"
        )
        symbol_checkbutton = ttk.Checkbutton(
            setting_frame, variable=self.symbol, text="Symbols"
        )
        password_len_label = ttk.Label(setting_frame, text="Password Length")
        password_len_entry = ttk.Entry(setting_frame, textvariable=self.password_len)
        generate_password_button = ttk.Button(
            self, text="Generate Password", command=self.generate_password
        )
        progressbar = ttk.Progressbar(self, variable=self.strength_number)
        strength_label = ttk.Label(
            self, textvariable=self.strength_status, anchor=tk.CENTER, justify=tk.CENTER
        )

        ## Widgets config
        password_entry.config(font="iosevka 16 bold", state="disabled")
        password_len_entry["font"] = "iosevka 16 bold"

        ## Pack the widgets
        uppercase_checkbutton.pack(expand=True, fill=tk.BOTH)
        lowercase_checkbutton.pack(expand=True, fill=tk.BOTH)
        symbol_checkbutton.pack(expand=True, fill=tk.BOTH)
        number_checkbutton.pack(expand=True, fill=tk.BOTH)
        password_len_label.pack(expand=True, fill=tk.BOTH)
        password_len_entry.pack(expand=True, fill=tk.BOTH)
        generate_password_button.pack(expand=True, fill=tk.BOTH)
        progressbar.pack(expand=True, fill=tk.BOTH)
        strength_label.pack(expand=True, fill=tk.BOTH)

        ## style
        self.style.configure("TFrame", background="#B6BBC4")
        self.style.configure("TLabel", font=("iosevka", 16))
        self.style.configure("TCheckbutton", font=("iosevka", 16))
        self.style.configure("TButton", font=("iosevka", 16), background="#DF826C")
        self.style.map("TButton", background=[("pressed", "#DF826C")])
        self.style.map(
            "TEntry",
            foreground=[("disabled", "black")],
            fieldbackground=[("disabled", "#F2F1EB")],
        )
        print(password_entry.state())
        print("Style password_entry", password_entry["style"])
        print("Style layout for entry", self.style.layout("TEntry"))
        print("Style options for entry", self.style.element_options("TEntry.field"))

        ## binds
        self.bind("<Return>", self.generate_password)
        generate_password_button.bind("<Return>", self.generate_password)

    def copy_password(self):
        print("copy password to clipboard")

    def checked_number(self):
        """Return number of check boxses checked."""
        # TODO: Can you make this in senior way.
        n = 0
        if self.upper.get():
            n += 1
        if self.lower.get():
            n += 1
        if self.number.get():
            n += 1
        if self.symbol.get():
            n += 1
        return n

    def generate_password(self, enve=None):
        password = []
        n, r = divmod(self.password_len.get(), self.checked_number())
        if self.upper.get():
            password.extend("".join(choices(self.uppers, k=n)))
        if self.lower.get():
            password.extend("".join(choices(self.lowers, k=n)))
        if self.number.get():
            password.extend("".join(choices(self.numbers, k=n)))
        if self.symbol.get():
            password.extend("".join(choices(self.symbols, k=n)))
        shuffle(password)
        rem_password = choices(self.allchars, k=r)
        password.extend(rem_password)
        self.password.set("".join(password))
        self.set_progress()

    def get_password_status(self):
        # TODO: Fix this code
        # TODO: Use enum or dicit
        checked_criteria = sum(item.get() for item in self.criteria)
        if checked_criteria <= 1:
            self.strength_status.set("weak")
        if checked_criteria == 2:
            self.strength_status.set("normal")
        if checked_criteria == 3:
            self.strength_status.set("strong")
        if checked_criteria == 4:
            self.strength_status.set("powerful")
        return self.strength_status.get()

    def set_progress(self):
        # TODO: Fix if chain enum instead of string or dict.
        password_status = self.get_password_status()
        if password_status == "weak":
            self.strength_number.set(25)
        elif password_status == "normal":
            self.strength_number.set(50)
        elif password_status == "strong":
            self.strength_number.set(75)
        elif password_status == "powerful":
            self.strength_number.set(100)
        else:
            self.strength_number.set(0)

    def password_strength(self):
        pass


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Password Generator")
        self.minsize(500, 300)
        mainframe = MainFrame(self, padding=(5, 10))
        mainframe.pack(expand=True, fill=tk.BOTH)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)


if __name__ == "__main__":
    app = App()
    app.mainloop()
