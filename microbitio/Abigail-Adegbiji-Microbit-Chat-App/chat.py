# Chat app
#import microbit
#import threading

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

# Find the channel and group the user is on
# Return -1 to signal an error
def find_user_channel(user):
    microbit.radio.config(channel=1, group=1, queue=10, length=251)

    while True:
        request = f"GET_GROUP:{user}"
        microbit.radio.send(request)
        response = microbit.radio.receive()
        if response != "None":
            user_id = response.split(":")[0]
            channel = response.split(":")[1]
            if channel == "Not found":
                return -1
            if user_id == user:
                return int(channel)
        microbit.sleep(1000)

def connect_to_user(user, users, current_channel):
    # Only do user lookup if the user's channel isn't already cached
    if user not in users:
        users[user] = find_user_channel(user)

    # The channel we'll connect to needs to be the bigger one
    channel = users[user]
    if current_channel > channel:
        channel = current_channel

    microbit.radio.config(channel=channel, group=channel)
    return users

def send(encryption_key):
    while True:
        message = input(">")
        encrypted = process(message, encryption_key, encrypt=True)
        microbit.radio.send(encrypted)
        microbit.sleep(1000)

def receive(decryption_key):
    while True:
        message = microbit.radio.receive()
        if message != "None":
            decrypted = process(message, decryption_key, encrypt=False)
            print("Received:", decrypted)
        microbit.sleep(1000)

microbit.radio.on()

me = "abigail.adegbiji"
users = connect_to_user(me, {}, 0)
users = connect_to_user("kevin.riffle", users, users[me])

# 75 character key
key = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/*-()&^%$#@!~"

send_thread = threading.Thread(target=send, args=(key,))
recv_thread = threading.Thread(target=send, args=(key,))

send_thread.start()
recv_thread.start()

# Wait for the threads to finish (they never actually do)
send_thread.join()
recv_thread.join()

# TODO: sender and recipient name validation with regex
#sender = input("Who are you (first.last)?")
#recipient = input("Who do you want to talk to (first.last)?")