# Communicating with the GNS
import microbit

microbit.radio.on()
microbit.radio.config(channel=1, group=1, queue=10, length=251)

name = input("Who do you want to talk to (first.last)?")
print("Searching...")

while True:
    request = f"GET_GROUP:{name}"
    microbit.radio.send(request)

    response = microbit.radio.receive()
    if response != "None":
        parts = response.split(":")
        user = parts[0]
        if user == name:
            user_parts = user.split(".")
            print("Found", user_parts[0], user_parts[1], parts[1])
            break

    microbit.sleep(1000)