import microbit
import threading
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
import re

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
        # Did we send the message?
        self.sent_by_user = sent_by_user

class Connection:
    def __init__(self):
        self.channel = -1
        # List of messages sent between the you and the recipient
        self.messages = []

class Messager:
    def __init__(self):
        # Map user ids to connections
        self.connections = {}

        # 75 bit encryption key
        self.encryption_key = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/*-()&^%$#@!~"

        # Who we're sending messages to
        self.current_recipient = ""

        # Current channel we're using to communicate
        self.current_channel = 0

        self.load_user_base()

    # Return a hashmap that maps all the users on the GNS
    # to chat data
    def load_user_base(self):
        with open("users.txt", "r") as file:
            for line in file.read().split("\n"):
                self.connections[line] = Connection()

    # TODO: spawn thread for this
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
        self.current_recipient = user

        # Only do user lookup if the user's channel isn't already cached
        if user not in self.connections or self.connections[user].channel == -1:
            self.connections[user].channel = self.find_user_channel(user)
            # TODO: show error if channel == -1

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

    # Return the message if we receive it
    def receive_message(self):
        response = microbit.radio.receive()
        if response != "None":
            # Ignore messages that follow the firstname.lastname:id pattern
            user_info_pattern = re.compile(".+:.*")
            if user_info_pattern.match(response):
                return None

            decrypted = process(response, self.encryption_key, encrypt=False)
            msg = Message(False, decrypted)
            self.connections[self.current_recipient].messages.append(msg)
            return msg
        return None

    def get_current_messages(self):
        return self.connections[self.current_recipient].messages

class App:
    def __init__(self, sender):
        self.messanger = Messager()
        self.messanger.connect_to_user(sender)

        self.root = ttk.Window(size=(600, 600), resizable=(False, False))

        # Sidebar of users
        self.users_list_container = ScrolledFrame(self.root, width=200, autohide=True)

        # Input box for typing in message
        self.prompt_container = ttk.Frame(self.root, width=400, height=40, padding=0)

        self.text_input = tk.StringVar(self.root)
        self.message_prompt = ttk.Entry(self.prompt_container, width=41, textvariable=self.text_input)

        # Send button
        self.send_button = ttk.Button(self.prompt_container, text="Send")

        # Container that holds a list of message elements
        self.messages_container = ScrolledFrame(self.root, width=600, height=600, autohide=True, padding=10)

        self.previous_button_element = None

    def add_message_element(self, text, sent_by_user):
        style = "inverse-light" if sent_by_user else "inverse-primary"
        align_direction = W if sent_by_user else E
        label = ttk.Label(self.messages_container, text=text, bootstyle=style, font=("Arial", 12))
        label.pack(anchor=align_direction, padx=10, pady=10)

    def change_recipient(self, user, button):
        self.messanger.connect_to_user(user)

        # Clear the container and repopulate the messages container with
        # messages between the sernder and recipient
        for child in self.messages_container.winfo_children():
            child.destroy()

        for msg in self.messanger.get_current_messages():
            self.add_message_element(msg.text, msg.sent_by_user)

        # Highlight the current recipient
        if self.previous_button_element != None:
            self.previous_button_element.configure(bootstyle="light")
        self.previous_button_element = button
        button.configure(bootstyle="primary")

    def send_message(self, events):
        self.messanger.send_message(self.text_input.get())
        self.add_message(self.text_input.get(), True)

    def add_message(self, text, sent_by_user):
        self.add_message_element(text, sent_by_user)
        # Scroll the container down to the end after a new element is added
        self.messages_container.update_idletasks()
        self.messages_container.yview_moveto(5.0)

    def receive_messages(self):
        while True:
            msg = self.messanger.receive_message()
            if msg != None:
                self.add_message(msg.text, False)
            microbit.sleep(1000)

    def run(self):
        # Populate the side bar with all the users on the gns
        self.users_list_container.pack(side=LEFT, fill=BOTH, expand=NO)
        for user in self.messanger.connections:
            button = ttk.Button(self.users_list_container, text=user, bootstyle="light", width=150)
            button.configure(command=lambda x=user, b=button : self.change_recipient(x, b))
            button.pack(anchor=W)

        self.message_prompt.pack(side=LEFT, anchor=W)
        self.message_prompt.bind("<Return>", self.send_message)

        self.send_button.pack(side=LEFT, anchor=E)
        self.send_button.configure(command=lambda : self.send_message(None))

        self.prompt_container.pack(side=BOTTOM, fill=X)

        self.messages_container.pack(side=RIGHT)

        # Receive messages on a separate thread
        thread = threading.Thread(target=self.receive_messages, args=())
        thread.start()

        self.root.mainloop()
        thread.join()

me = "abigail.adegbiji"
app = App(me)
app.run()