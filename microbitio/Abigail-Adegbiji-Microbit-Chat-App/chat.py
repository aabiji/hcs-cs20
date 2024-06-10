import microbit
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame

# TODO: receive threads and connect thread
# TODO: refactor -- almost done

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

# Encrypt or decrypt a message based on an encryption key
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

class Connection:
    def __init__(self):
        self.channel = -1
        self.messages = []

class Messager:
    def __init__(self):
        self.connections = {} # Map user ids to connections
        self.encryption_key = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/*-()&^%$#@!~"
        self.current_recipient = ""
        self.current_channel = 0

    # Return a hashmap that maps all the users on the GNS
    # to chat data
    def load_user_base(self):
        with open("users.txt", "r") as file:
            for line in file.read().split("\n"):
                self.connections[line] = Connection()

    # Find the channel and group the user is on
    # Return -1 to signal an error
    def find_user_channel(self, user):
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

    def connect_to_user(self, user):
        # Only do user lookup if the user's channel isn't already cached
        if user not in self.connections or self.connections[user].channel == -1:
            self.connections[user].channel = self.find_user_channel(user)

        # The channel we'll connect to needs to be the bigger one
        channel = self.connections[user].channel
        if self.current_channel > channel:
            channel = self.current_channel
        else:
            self.current_channel = channel

        microbit.radio.config(channel=channel, group=channel)

    def change_recipient(self, user):
        self.current_recipient = user
        self.connect_to_user(self.current_recipient)

    def send_message(self, text):
        encrypted = process(text, self.encryption_key, encrypt=True)
        microbit.radio.send(encrypted)

        msg = Message(True, encrypted)
        self.connections[self.current_recipient].messages.append(msg)

    def get_current_messages(self):
        return self.connections[self.current_recipient].messages

class App:
    def __init__(self):
        self.messanger = Messager()
        self.message_container = None

    def add_message_element(self, container, text, sent_by_user):
        style = "inverse-light" if sent_by_user else "inverse-primary"
        align_direction = W if sent_by_user else E
        label = ttk.Label(container, text=text, bootstyle=style, font=("Arial", 12))
        label.pack(anchor=align_direction, padx=10, pady=10)

    def change_recipient(self, user):
        self.messanger.connect_to_user(user)

        # Clear the container
        for child in self.message_container.winfo_children():
            child.destroy()

        for msg in self.messanger.get_current_messages():
            self.add_message_element(self.message_container, msg.input_text, msg.sent_by_user)

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