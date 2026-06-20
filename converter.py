import sys
import subprocess
from time import sleep
from pathlib import Path

try:
    import requests
except ModuleNotFoundError:
    print("\nDOWNLOADING REQUIRED FILES...")
    print("PLEASE WAIT...\n")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'requests'])
    import requests

try:
    import tkinter as tk
except ModuleNotFoundError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'tkinter'])
    import tkinter as tk
import tkinter.messagebox


class Converter:
    """A class to convert currency from different countries."""

    class InvalidAccessKey(Exception):
        pass

    def __init__(self):
        """Initialize attributes and access key

        Then fetch exchange rate data.
        """
        self.file_path = Path('access_key.txt')

        self.access_key = '84692a9e7f563bcebe3bde27cb2a16a1'
        self.url = f"https://data.fixer.io/api/latest?access_key={self.access_key}"

        try:
            response = requests.get(self.url)
            self.data = response.json()
        except requests.exceptions.ConnectionError:
            print("\nUnable to connect to the Internet. Please check your Wi-Fi "
                  "connection before using the program.")
            tkinter.messagebox.showinfo("ERROR :(",
                                        "Unable to connect to the Internet."
                                        "\n\nPlease check your Wi-Fi connection "
                                        "before using the program."
                                        )
            sys.exit(1)

    def check_success(self) -> None:
        """Check if exchange rate data was successfully retrieved.

        Raises:
            Converter.InvalidAccessKey: If the access key is not valid.
            RuntimeError: Any other error returned by the API.
        """
        if not self.data['success']:
            if self.data['error']['code'] in [401, 101]:
                raise self.InvalidAccessKey("Unable to retrieve exchange rate data "
                                            "(invalid API access key).")
            elif self.data['error']['code'] == 429:
                raise RuntimeError("Sorry, the maximum allowed API amount of monthly API "
                                   "requests has been reached. Please try again the "
                                   "following month")
            else:
                raise RuntimeError(f"Unable to retrieve exchange rate data. ("
                                   f"{self.data['error']['type']}) "
                                   f"Please try "
                                   f"again. ({self.data['error']['code']})")

    def convert(self,
                base_currency: str,
                target_currency: str,
                base_amount: float,
                round_result=True) -> float:
        """Convert currency, base to target (returns target value result)."""
        eur_to_base_rate = self._get_multiplier(base_currency)
        eur_to_target_rate = self._get_multiplier(target_currency)

        # First convert base to EUR, then convert EUR to target
        # So to invert our EUR to base multiplier, ths formula is used:
        # Inverted Multiplier = 1 / Known Multiplier
        base_to_eur_rate = 1 / eur_to_base_rate

        # Convert base to EUR, then EUR to target currency
        base_as_eur = base_amount * base_to_eur_rate
        target_result = base_as_eur * eur_to_target_rate

        if round_result:
            target_result = round(target_result, 3)

        return target_result

    def _get_multiplier(self, code: str) -> float:
        """Get the conversion multiplier from EUR.

        The fixer.io API returns exchange rates relative to EUR by default.
        """
        return self.data['rates'][code]

    def _prompt_new_access_key(self) -> str:
        """Guide the user to get and input a new access key."""
        print("\nTry using a new API access key from https://fixer.io")
        sleep(2)
        while True:
            choice = input("Would you like to be guided to do so? (Y/N): ").upper()
            if choice not in ['Y', 'YES']:
                sys.exit(1)
            print("\nSTEP 1: Open your Web Browser and search: 'https://fixer.io'.")
            print("STEP 2: Click 'Sign Up Free'. Choose a suitable plan (the Free plan is "
                  "\n\t\trecommended for general use) and enter the required personal "
                  "\n\t\tinformation. You can fill in your Address, Postal code and Company "
                  "\n\t\tdetails with a dash ('-') is you are unable to provide one.")
            print("STEP 3: On the 'Thank You' page, click 'Visit Dashboard'.")
            print("STEP 4: Copy your API access key.")
            new_access_key = input("STEP 5: Paste your access key here: ")

            if self._check_access_key(new_access_key):
                break

            print("\nInvalid access key. Try again.\n")
            sleep(2)

        return new_access_key

    def _check_access_key(self, access_key: str) -> bool:
        """Return if the access key is valid."""
        if len(access_key) != 32:
            return False

        new_url = self.url.replace(self.access_key, access_key)
        response = requests.get(new_url)
        data = response.json()

        if not data['success']:
            return False

        return True

    def _save_access_key(self, new_access_key: str):
        """Set a new access key for the API, which be used instead of
        the default if the default does not work and if the TXT fil
        exists.
        """
        print("\nPlease wait...")
        sleep(3.14159265387)

        with open(self.file_path, 'w') as file:
            file.write(new_access_key)

        print("\nNew access key successfully set!")
