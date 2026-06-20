import sys
import subprocess

try:
    import tkinter as tk
except ModuleNotFoundError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'tkinter'])
    import tkinter as tk


class GUISettings:
    """A class to manage window and appearance settings for the GUI."""

    def __init__(self, gui):
        """Initialize window and appearance settings."""
        self.gui = gui

        self.gui.root.title("Currency Converter (GUI version)")

        # Window frame
        self.window = tk.Frame(
            self.gui.root,
            bg='#daf0ff',
            pady=2,
            width=1850,
            height=100,
            relief='ridge'
        )
        self.window.grid(row=0, column=0)

        # Title
        self.headlabel = tk.Label(
            self.window,
            font=('Trebuchet MS', 20, 'bold'),
            text="CURRENCY CONVERTER",
            bg='#daf0ff',
            fg='black'
        )
        self.headlabel.grid(row=1, column=0, sticky=tk.W)

        # Labels
        self.version_label = tk.Label(
            self.gui.root,
            font=('Trebuchet MS', 10, 'bold'),
            text=f" version {self.gui.version}",
            padx=12,
            pady=2,
            bg="#daf0ff",
            fg="black"
        )
        self.version_label.grid(row=1, column=0, sticky=tk.W)

        self.blank_line1 = tk.Label(
            self.gui.root,
            font=('Trebuchet MS', 15, 'bold'),
            text="",
            padx=2,
            pady=2,
            bg="#daf0ff",
            fg="black"
        )
        self.blank_line1.grid(row=1, column=0, sticky=tk.W)

        self.amount_label = tk.Label(
            self.gui.root,
            font=('Trebuchet MS', 15, 'bold'),
            text="\t\tAmount  :  ",
            bg='#daf0ff',
            fg='black'
        )
        self.amount_label.grid(row=2, column=0, sticky=tk.W)

        self.from_label = tk.Label(
            self.gui.root,
            font=('Trebuchet MS', 15, 'bold'),
            text="\t\tFrom: ",
            bg='#daf0ff',
            fg="black"
        )
        self.from_label.grid(row=3, column=0, sticky=tk.W)

        self.to_label = tk.Label(
            self.gui.root,
            font=('Trebuchet MS', 15, 'bold'),
            text="\t\tTo:   ",
            bg='#daf0ff',
            fg='black'
        )
        self.to_label.grid(row=4, column=0, sticky=tk.W)

        self.blank_line2 = tk.Label(
            self.gui.root,
            font=('Trebuchet MS', 7, 'bold'),
            text="",
            padx=2,
            pady=2,
            bg='#daf0ff',
            fg='black'
        )
        self.blank_line2.grid(row=5, column=0, sticky=tk.W)

        self.blank_line3 = tk.Label(
            self.gui.root,
            font=('Trebuchet MS', 7, 'bold'),
            text="",
            padx=2,
            pady=2,
            bg='#daf0ff',
            fg='black'
        )
        self.blank_line3.grid(row=7, column=0, sticky=tk.W)

        self.result_label = tk.Label(
            self.gui.root,
            font=('Trebuchet MS', 15, 'bold'),
            text="\t\tResult:  ",
            bg='#daf0ff',
            fg='black'
        )
        self.result_label.grid(row=8, column=0, sticky=tk.W)

        # Buttons
        self.convert_button = tk.Button(
            self.gui.root,
            font=('Trebuchet MS', 15, 'bold'),
            text="   Convert  ",
            padx=2,
            pady=2,
            bg='blue',
            fg='black',
            command=self.gui.convert
        )
        self.convert_button.grid(row=6, column=4)
        self.gui.root.bind('<Return>', lambda event: self.convert_button.invoke())

        self.blank_line4 = tk.Label(
            self.gui.root,
            font=('Trebuchet MS', 7, 'bold'),
            text="",
            padx=2,
            pady=2,
            bg='#daf0ff',
            fg='black'
        )
        self.blank_line4.grid(row=9, column=0, sticky=tk.W)

        self.clearall_button = tk.Button(
            self.gui.root,
            font=('Trebuchet MS', 15, 'bold'),
            text="   Clear All  ",
            padx=2,
            pady=2,
            bg='blue',
            fg='black',
            command=self.gui.clear_all)
        self.clearall_button.grid(row=10, column=4)
