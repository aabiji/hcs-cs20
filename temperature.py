"""
Temperature Conversion Assignment
Author: Abigail Adegbiji
Date: March 25

Ask the user for a input choice (a to f, quit or q).
If the user quits, print all the conversions from our history list and exit.
Else, map that input choice to a unit we'll convert from and a unit we'll convert to.
Use those from and to units to compute the converted temperature.
Append the conversion to a history list. And print the conversion.
"""

HISTORY = []
CELSIUS = "c"
FAHRENHEIT = "f"
KELVIN = "k"

class Conversion:
    def __init__(self, from_unit, to_unit, temperature):
        self.from_unit = from_unit
        self.to_unit = to_unit
        self.before = temperature
        self.after = 0

    def output(self):
        print(f"{self.before} °{self.from_unit.upper()} = {self.after} °{self.to_unit.upper()}\n")

    def convert(self):
        if self.from_unit == FAHRENHEIT and self.to_unit == CELSIUS:
            self.after = (self.before - 32) * (5 / 9)
        elif self.from_unit == FAHRENHEIT and self.to_unit == KELVIN:
            self.after = (self.before - 32) * (5 / 9) + 273.15

        if self.from_unit == CELSIUS and self.to_unit == FAHRENHEIT:
            self.after = (self.before * (9 / 5)) + 32
        elif self.from_unit == CELSIUS and self.to_unit == KELVIN:
            self.after = self.before + 273.15

        if self.from_unit == KELVIN and self.to_unit == CELSIUS:
            self.after = self.before - 273.15
        elif self.from_unit == KELVIN and self.to_unit == FAHRENHEIT:
            self.after = (self.before - 273.15) * (9 / 5) + 32


# If the unit we are converting to in not kelvin, convert it on the fly
def kelvin_convert(conversion):
    conversion.convert(conversion.to_unit, KELVIN, conversion.after)
    return conversion.after

def log_history():
    global HISTORY
    if len(HISTORY) == 0:
        print("You haven't converted anything")
        return

    print("\nYour conversions: ")
    HISTORY.sort(key=kelvin_convert)
    for conversion in HISTORY:
        conversion.output()

def is_too_cold(unit, temperature):
    if unit == KELVIN and temperature < 0:
        return True
    elif unit == CELSIUS and temperature < -273.15:
        return True
    elif unit == FAHRENHEIT and temperature < -459.67:
        return True
    return False

def input_num(prompt):
    value = input(prompt)
    try:
        return float(value)
    except:
        return -1 # Casting failed

def sanitize(user_input):
    return user_input.strip().lower()

def run():
    print("This is a temperature conversion program. Enter 'q', 'Q', or 'quit' at any time to quit.")
    while True:
        from_unit = sanitize(input("Which unit do you want to convert from: (C, F, K)? "))
        if from_unit == "q" or from_unit == "quit":
            break
        elif len(from_unit) > 1:
            print("You need to enter C, F, or K.")
            continue

        to_unit = sanitize(input("Which unit do you want to convert to: (C, F, K)? "))
        if to_unit == "q" or to_unit == "quit":
            break
        elif len(from_unit) > 1:
            print("You need to enter C, F, or K.")
            continue

        temperature = 0
        prompt = sanitize(input("Your temperature: "))
        if prompt == "q" or prompt == "quit":
            break
        try:
            temperature = float(prompt)
        except:
            print("You need to need to enter a number.")
            continue 

        if is_too_cold(from_unit, temperature):
            print("That's too cold!")
            continue

        conversion = Conversion(from_unit, to_unit, temperature)
        conversion.convert()
        HISTORY.append(conversion)
        conversion.output()

    log_history()

if __name__ == "__main__":
    run()