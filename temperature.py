# todo: explain and maybe refactor

class Conversion:
    def __init__(self, from_unit, to_unit, before, after):
        self.from_unit = from_unit
        self.to_unit = to_unit
        self.before = before
        self.after = after

history = []
def log_history():
    global history
    if len(history) == 0:
        print("You haven't converted anything")
        return 

    # Sort by kelvin temperature
    to_kelvin = lambda h : convert(h.to_unit, "K", h.after)
    history.sort(key=to_kelvin)

    print("\nYour conversions: ")
    for h in history:
        print(f"{h.before} °{h.from_unit} = {h.after} °{h.to_unit}")

def get_conversion_units(input_choice):
    if input_choice == "a":
        return "C", "F"
    elif input_choice == "b":
        return "C", "K"

    if input_choice == "c":
        return "F", "C"
    elif input_choice == "d":
        return "F", "K"

    if input_choice == "e":
        return "K", "C"
    elif input_choice == "f":
        return "K", "F"

def convert(from_unit, to_unit, value):
    if from_unit == "F" and to_unit == "C":
        return (value - 32) * (5/9)
    elif from_unit == "F" and to_unit == "K":
        return (value - 32) * (5/9) + 273.15

    if from_unit == "C" and to_unit == "F":
        return (value * (9/5)) + 32
    elif from_unit == "C" and to_unit == "K":
        return value + 273.15

    if from_unit == "K" and to_unit == "C":
        return value - 273.15
    elif from_unit == "K" and to_unit == "F":
        return (value - 273.15) * (9/5) + 32

    return value

def is_too_cold(unit, temperature):
    if unit == "K" and temperature < 0:
        return True
    elif unit == "C" and temperature < -273.15:
        return True
    elif unit == "F" and temperature < -459.67:
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
    print("This is a temperature conversion program. Do you want to ...")
    print("(a) Convert from Celcius to Farenheit?")
    print("(b) Convert from Celcius to Kelvin?")
    print("(c) Convert from Farenheit to Celcius?")
    print("(d) Convert from Farenheit to Kelvin?")
    print("(e) Convert from Kelvin to Celcius?")
    print("(f) Convert from Kelvin to Farenheit?\n")

    while True:
        msg = "Your choice (a, b, c, d, e, f, or quit): "
        choice = sanitize(input(msg))
        if choice == "q" or choice == "quit":
            break

        temperature = input_num("Your temperature: ")
        if temperature == -1:
            print("You need to need to enter a number.")
            continue 

        from_unit, to_unit = get_conversion_units(choice)
        if is_too_cold(from_unit, temperature):
            print("That's too cold!")
            continue

        converted = convert(from_unit, to_unit, temperature)
        conversion = Conversion(from_unit, to_unit, temperature, converted)
        history.append(conversion)

        print(f"{temperature} °{from_unit} = {converted} °{to_unit}\n")

    log_history()

if __name__ == "__main__":
    run()
