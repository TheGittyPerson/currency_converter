import sys
import subprocess
import json
from pathlib import Path

try:
    import tkinter as tk
except ModuleNotFoundError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'tkinter'])
    import tkinter as tk


class IOFields:
    def __init__(self, gui):
        """Manage and Initialize the settings of the input/output fields."""
        self.gui = gui

        # Currency Selection boxes
        self.base_currency = tk.StringVar(self.gui.root)
        self.target_currency = tk.StringVar(self.gui.root)

        self.base_currency.set("--Select Currency--")
        self.target_currency.set("--Select Currency--")

        self.json_path = Path(__file__).parent.resolve() \
                             / 'ordered_currency_codes.json'
        with open(self.json_path, 'r') as file:
            self.currency_codes = json.load(file)['ordered_currencies']

        self.gui.root.configure(background='#daf0ff')
        self.gui.root.geometry('700x400')

        self.base_currency_ops = tk.OptionMenu(
            self.gui.root,
            self.base_currency,
            *self.currency_codes
        )
        self.to_currency_ops = tk.OptionMenu(
            self.gui.root,
            self.target_currency,
            *self.currency_codes
        )

        self.base_currency_ops.grid(row=3, column=4, ipadx=45, sticky=tk.E)
        self.to_currency_ops.grid(row=4, column=4, ipadx=45, sticky=tk.E)
        self.base_currency_ops.configure(font=('Helvetica', 13))
        self.to_currency_ops.configure(font=('Helvetica', 13))

        # Input/Output Fields
        self.amount_field = tk.Entry(self.gui.root, font=('Helvetica', 14))
        self.amount_field.grid(row=2, column=4, ipadx=28, sticky=tk.E)

        self.result_field = tk.Entry(self.gui.root, font=('Helvetica', 14))
        self.result_field.grid(row=8, column=4, ipadx=31, sticky=tk.E)
