# Chat app
import microbit
import threading

# Find the channel you and your recipient is on
def find_channels(sender, recipient):
    microbit.radio.config(channel=1, group=1, queue=10, length=251)
    users = {}

    while True:
        request = f"GET_GROUP:{recipient}"
        microbit.radio.send(request)
        response = microbit.radio.receive()
        if response != "None":
            user = response.split(":")[0]
            channel = response.split(":")[1]
            if channel == "Not Found" or user in channels:
                continue
            if user == recipient or user == sender:
                users[user] = int(channel)
                if len(channels.keys()) == 2:
                    break
        microbit.sleep(1000)

    return channels

"""
microbit.radio.on()


# TODO: sender and recipient name validation with regex
#sender = input("Who are you (first.last)?")
#recipient = input("Who do you want to talk to (first.last)?")

# Connect on the larger of the two group ids
# channels = find_channels(sender, recipient)
channels = {
    "abigail.adegbiji": 0,
    "kevin.riffle": 46
}
num = max(channels.values())
microbit.radio.config(channel=num, group=num)

def send():
    while True:
        message = input(">")
        microbit.radio.send(message)
        microbit.sleep(1000)

def receive():
    while True:
        message = microbit.radio.receive()
        if message != "None":
            print("Received:", message)
        microbit.sleep(1000)

# Dispatch threads
threads = [
    threading.Thread(target=send, args=()),
    threading.Thread(target=receive, args=())
]
for thread in threads:
    thread.start()

for thread in threads:
    thread.join()
"""

#key = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
# key needs to be all lowercase
key = "this tool is used to detect radiation"
msg = "hello i am having a good day"

def encrypt(msg, key):
    key_index = 0
    encrypted_msg = ""
    for character in msg:
        key_char = key[key_index]
        key_offset = ord(key_char) - 97
        if key_char == "":
            key_offset = 26 # Spaces are 26 away from 'a'
        key_offset += 1

        key_index += 1
        if key_index >= len(key):
            key_index = 0

        ascii_char = ord(character) - 97 # TODO: what about capital letters and punctuation???
        shifted_char = (ascii_char + key_offset) % 27
        if shifted_char == 26:
            encrypted_msg += " "
        else:
            encrypted_msg += chr(97 + shifted_char)

    return encrypted_msg

print(encrypt(msg, key))