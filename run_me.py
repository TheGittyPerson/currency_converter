import sys
import tkinter.messagebox

try:
    from currency_converter_gui import ConverterGUI
except ModuleNotFoundError:
    tkinter.messagebox.showinfo(
        "ERROR :(",
        "Please Download 'currency_converter_gui.py' before use"
    )

if __name__ == '__main__':
    try:
        currency_converter = ConverterGUI()
        currency_converter.run()
    except KeyboardInterrupt:
        print("\nProgram stopped.")
        sys.exit(0)
    except Exception as e:
        tkinter.messagebox.showinfo("ERROR :(",
                                    "An unexpected error occurred:"
                                    f"\n{e}"
                                    "\n\nPlease try again."
                                    )
        sys.exit(1)
