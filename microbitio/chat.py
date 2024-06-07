# Chat app
#import microbit
#import threading

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
            if channel == "Not Found" or user in users:
                continue
            if user == recipient or user == sender:
                users[user] = int(channel)
                if len(users.keys()) == 2:
                    break
        microbit.sleep(1000)

    return users

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

# Get the offset from the letter 'a' to the character, where 'a' is 0
def get_offset(character):
    ascii_index = ord(character)

    # Letters 'a' to 'z', 0 - 26
    if ascii_index >= 97 and ascii_index <= 122:
        return ascii_index - 97

    # Letter 'A' to 'Z', 27 - 53
    if ascii_index >= 65 and ascii_index <= 90:
        return ascii_index - 38

    # Every other ascii character, 54 - 86
    offsets = { ' ': 54, '!': 55, '@' : 56, '#': 57, '$': 58, '%': 59, '^': 60,
                '&': 61, '*': 62, '(' : 63, ')': 64, '-': 65, '+': 66, '_': 67,
                '=': 68, '{': 69, '}' : 70, '[': 71, ']': 72, ':': 73, ';': 74,
                '"': 75, "'": 76, '\\': 77, '|': 78, '`': 79, '~': 80, ',': 81,
                '<': 82, '.': 83,  '>': 84, '/': 85, '?': 86 }
    return offsets[character]

# Get the character from the offset going from 0 to 86
def get_character(offset):
    if offset <= 26:
        return chr(offset + 97)

    if offset >= 27 and offset <= 53:
        return chr(offset + 38)

    characters = { 54: ' ',  55: '!',  56: '@',  57: '#',  58: '$',  59: '%',  60: '^',
                   61: '&',  62: '*',  63: '(',  64: ')',  65: '-',  66: '+',  67: '_',
                   68: '=',  69: '{',  70: '}',  71: '[',  72: ']',  73: ':',  74: ';',
                   75: '"',  76: "'",  77: '\\', 78: '|',  79: '`',  80: '~',  81: ',',
                   82: '<',  83: '.',  84: '>',  85: '/',  86: '?' }
    return characters[offset]

def process(msg, key, encrypt):
    max_offset = 87
    key_index = 0
    new_msg = ""

    for character in msg:
        key_offset = get_offset(key[key_index])

        key_index += 1
        if key_index >= len(key):
            key_index = 0

        # Shift the character in the message by the
        # offset of the corresponding character in the key
        # If we're encrypting, we shift forwards to get a
        # substituted character. If we're decrypting,
        # we shift backwards to get our original character
        char_offset = get_offset(character)
        shifted_char = char_offset + key_offset
        if encrypt == False:
            shifted_char = char_offset - key_offset

        # Make the shifted character within the range of 0 to 86
        shifted_char %= max_offset
        new_msg += get_character(shifted_char)

    return new_msg

# 75 character key
key = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/*-()&^%$#@!~"
msg = "hello world! how are you doing today?"

encrypted = process(msg, key, encrypt=True)
decrypted = process(encrypted, key, encrypt=False)