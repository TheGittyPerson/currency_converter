import sys
import subprocess

try:
    import tkinter as tk
except ModuleNotFoundError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'tkinter'])
    import tkinter as tk
import tkinter.messagebox

try:
    from converter import Converter
except ModuleNotFoundError:
    tkinter.messagebox.showinfo("ERROR :(",
                                "Please Download 'converter.py' before use"
                                )
try:
    from gui_settings import GUISettings
except ModuleNotFoundError:
    tkinter.messagebox.showinfo("ERROR :(",
                                "Please Download 'gui_settings.py' before use"
                                )
try:
    from io_fields import IOFields
except ModuleNotFoundError:
    tkinter.messagebox.showinfo("ERROR :(",
                                "Please Download 'io_fields.py' before use"
                                )


class ConverterGUI:
    def __init__(self):
        """Initialize GUI window and settings."""
        self.root = tk.Tk()

        self.version = '2024.1.4'

        self.converter = Converter()
        self.settings = GUISettings(self)
        self.fileds = IOFields(self)

        try:
            self.converter.check_success()
        except self.converter.InvalidAccessKey:
            tkinter.messagebox.showinfo("ERROR :(",
                                        "Invalid API Access Key."
                                        "\nPlease use a new access key in 'converter.py'"
                                        )
            self.exit_all(1)
        except RuntimeError as e:
            tkinter.messagebox.showinfo("ERROR :(",
                                        f"An unexpected error occurred: {e}"
                                        "\n\nPlease try again."
                                        )
            self.exit_all(1)

    def run(self):
        self.root.mainloop()

    def convert(self):
        base_currency = self.fileds.base_currency.get()
        target_currency = self.fileds.target_currency.get()
        base_amount = self.fileds.amount_field.get()

        if tk.Entry == '':
            tkinter.messagebox.showinfo(
                "ERROR :(",
                "Amount Not Entered."
                "\nPlease enter a valid amount."
            )

        elif base_amount == '':
            tkinter.messagebox.showinfo(
                "ERROR :(",
                "Please enter a valid amount"
            )

        elif base_currency == "--Select Currency--" or target_currency == "--Select Currency--":
            tkinter.messagebox.showinfo("ERROR :(",
                                        "Currency not selected."
                                        "\nPlease select FROM and TO Currency from the menu."
                                        )

        else:
            self.clear_result_field()
            amount = self.fileds.amount_field.get()

            try:
                result = self.converter.convert(
                    base_currency,
                    target_currency,
                    float(amount)
                )
            except ValueError:
                tkinter.messagebox.showinfo(
                    "ERROR",
                    "Please enter a valid amount"
                    "\n(Enter digits ONLY."
                    " No letters, punctualtion, or special characters/symbols)"
                )
                return

            self.fileds.result_field.insert(
                0,
                str(result)
            )

    def clear_result_field(self):
        self.fileds.result_field.delete(0, tk.END)

    def clear_all(self):
        self.fileds.amount_field.delete(0, tk.END)
        self.fileds.result_field.delete(0, tk.END)

    def exit_all(self, exit_code):
        self.root.quit()
        self.root.destroy()
        sys.exit(exit_code)
