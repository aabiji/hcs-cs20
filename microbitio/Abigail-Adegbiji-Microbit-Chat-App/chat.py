import microbit
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame

microbit.radio.on()

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

class Message:
    def __init__(self, sent_by_user, text):
        self.text = text
        self.sent_by_user = sent_by_user

class Chat:
    def __init__(self):
        self.channel = -1
        self.messages = []

# Return a hashmap that maps all the users on the GNS
# to chat data
def load_user_base():
    chat = {}
    with open("users.txt", "r") as file:
        for line in file.read().split("\n"):
            chat[line] = Chat()
    return chat

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

def connect_to_user(user, chats, current_channel):
    # Only do user lookup if the user's channel isn't already cached
    if user not in chats or chats[user].channel == -1:
        chats[user].channel = find_user_channel(user)

    # The channel we'll connect to needs to be the bigger one
    channel = chats[user].channel
    if current_channel > channel:
        channel = current_channel

    microbit.radio.config(channel=channel, group=channel)
    return chats

def add_message_element(container, text, sent_by_user):
    style = "inverse-light" if sent_by_user else "inverse-primary"
    align_direction = W if sent_by_user else E
    label = ttk.Label(container, text=text, bootstyle=style, font=("Arial", 12))
    label.pack(anchor=align_direction, padx=10, pady=10)

def load_chat_ui(container, chat):
    # Clear the container
    for child in container.winfo_children():
        child.destroy()

    for msg in chat.messages:
        add_message_element(container, msg.input_text, msg.sent_by_user)

sender = "abigail.adegbiji"
current_recipient = ""
chats = load_user_base()
chats = connect_to_user(sender, chats, -1)
# 75 bit key
key = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/*-()&^%$#@!~"

def change_recipient(user):
    global recipient, chats, messages
    current_recipient = user
    chats = connect_to_user(current_recipient, chats, chats[sender].channel)

    # Clear the messages element
    for child in messages.winfo_children():
        child.destroy()

    # Populate with the corresponding messages sent
    for msg in chats[current_recipient].messages:
        add_message_element(messages, msg.text, msg.sent_by_user)

app = ttk.Window(size=(600, 600))

# Sidebar of users
users_list = ScrolledFrame(app, width=200, autohide=True)
users_list.pack(side=LEFT, fill=BOTH, expand=NO)
for user in chats:
    button = ttk.Button(users_list, text=user, bootstyle="light", width=150, command=lambda x=user : change_recipient(x))
    button.pack(anchor=W)

# Message input
input_text = tk.StringVar(app)
prompt = ttk.Entry(width=200, textvariable=input_text)
prompt.pack(side=BOTTOM, anchor=W)

# List of chat messages
messages = ScrolledFrame(app, width=600, height=600, autohide=True, padding=10)
messages.pack(side=RIGHT)

def send_message(event):
    global messages, input_text, key, current_recipient
    encrypted = process(input_text.get(), key, encrypt=True)
    microbit.radio.send(encrypted)

    msg = Message(True, input_text.get())
    chats[current_recipient].messages.append(msg)

    add_message_element(messages, input_text.get(), True)
    messages.update_idletasks()
    messages.yview_moveto(5.0)
prompt.bind("<Return>", send_message)

app.mainloop()