import sys
import subprocess
import re
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


class CurrencyConverter:
    """A class to convert currency from different countries."""

    class InvalidAccessKey(Exception):
        pass

    def __init__(self):
        """Initialize attributes and access key, and fetch exchange rate data"""
        print('\n*--CURRENCY CONVERTER--*\n')
        self.version = '2024.1.4'

        self.file_path = Path('access_key.txt')

        self.access_key = '84692a9e7f563bcebe3bde27cb2a16a1'
        self.url = f"https://data.fixer.io/api/latest?access_key={self.access_key}"

        try:
            response = requests.get(self.url)
            self.data = response.json()
        except requests.exceptions.ConnectionError:
            print("\nUnable to connect to the Internet. Please check your Wi-Fi "
                  "connection before using the program.")
            sys.exit(1)

    def run(self):
        """Run CurrencyConverter."""
        while True:
            self._check_success()
            self._display_info()
            sleep(1)
            while True:
                try:

                    base_currency = self._prompt_base_currency()
                    target_currency = self._prompt_target_currency()
                    base_value = self._prompt_base_value()
                    result = self._convert(base_currency, target_currency, base_value)

                    print("\nRESULT:"
                          f" {base_value} {base_currency} = {result} {target_currency}")
                    sleep(2)

                except self.InvalidAccessKey as e:
                    if self.file_path.exists():
                        self.access_key = self.file_path.read_text()
                        continue
                    print(f"ERROR: {e}")
                    sleep(2)
                    new_access_key = self._prompt_new_access_key()
                    self._save_access_key(new_access_key)
                    sleep(2)
                    continue

                except KeyboardInterrupt:
                    print("\n\nUser stopped the program.")
                    sys.exit(0)
                except Exception as e:
                    print(f"\n:( An unexpected error occurred: {e}.")
                    sys.exit(1)

    def _check_success(self):
        """
        Check if exchange rate data was successfully retrieved,
        and raise an error if unsuccessful.
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
                                   f"Please try again. "
                                   f"({self.data['error']['code']})")

    def _display_info(self):
        """Display info about the program."""
        print(f"- version {self.version}")
        print("- Over 170 different currencies available")
        print("- Live exchange rates that update every 1 hour")
        print("- Powered by 15+ exchange rate data sources")
        print("- Try the Currency Converter GUI version!")

    def _prompt_base_currency(self) -> str:
        """Prompt user for the base currency."""
        while True:
            base_currency = (input("\n(Enter currency code) CONVERT FROM: ").upper()
                             .strip())
            valid = self._check_code(base_currency)
            if valid:
                break
            print("\nERROR: Sorry, the currency code you entered is not recognized. "
                  "Try again.")
            sleep(2)
        return base_currency

    def _prompt_target_currency(self) -> str:
        """Prompt the user for the target currency."""
        while True:
            target_currency = input("(Enter currency code) CONVERT TO: ").upper().strip()
            valid = self._check_code(target_currency)
            if valid:
                break
            print("\nERROR: Sorry, the currency code you entered is not recognized. "
                  "Try again.")
            sleep(2)
        return target_currency

    @staticmethod
    def _prompt_base_value() -> float:
        """Prompt the user for base amount."""
        while True:
            try:
                # Input amount and remove any symbols or letters
                raw_input = input("(Enter an integer/decimal) AMOUNT: ").strip()
                cleaned_input = re.sub(r'[^\d.]', '', raw_input)

                # Convert the cleaned input to a float
                base_value = float(cleaned_input)
            except ValueError:
                print("\nERROR: Please enter a number only.\n")
                sleep(2)
            except OverflowError:
                print("\nERROR: The amount you entered is too large.\n")
                sleep(2)
            else:
                return base_value

    def _convert(self,
                 base_currency: str,
                 target_currency: str,
                 base_value: float,
                 round_result=True) -> float:
        """Convert currency, base to target (returns target value result)."""
        eur_to_base_rate = self._get_multiplier(base_currency)
        eur_to_target_rate = self._get_multiplier(target_currency)

        # First convert base to EUR, then convert EUR to target
        # So to invert our EUR to base multiplier, ths formula is used:
        # Inverted Multiplier = 1 / Known Multiplier
        base_to_eur_rate = 1 / eur_to_base_rate

        # Convert base to EUR, then EUR to target currency
        base_as_eur = base_value * base_to_eur_rate
        target_value = base_as_eur * eur_to_target_rate

        if round_result:
            target_value = round(target_value, 5)

        return target_value

    def _get_multiplier(self, code: str) -> float:
        """Get the conversion multiplier from EUR."""
        return self.data['rates'][code]

    def _check_code(self, code: str) -> bool:
        """Return True if the currency code is valid, False if otherwise."""
        if len(code) != 3:
            return False
        if code not in self.data['rates']:
            return False
        if any(char.isdigit() for char in code):
            return False
        return True

    def _prompt_new_access_key(self) -> str:
        """
        Guide the user to get and input a new access key
        (if they would like to be).
        """
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
        """
        Set a new access key for the API, which be used instead of
        the default if the default does not work and if
        the file (access_key.txt) exists.
        """
        print("\nPlease wait...")
        sleep(3.14159265387)

        with open(self.file_path, 'w') as file:
            file.write(new_access_key)

        print("\nNew access key successfully set!")


if __name__ == "__main__":
    converter = CurrencyConverter()
    converter.run()
