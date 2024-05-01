# Madlibs
# By Abigail Adegbiji, April 26, 2024
import copy
import PySimpleGUI as gui

# Read a file and returns all the lines it contains
def read_file(filename):
    contents = ""
    with open(filename, "r") as file:
        contents = file.read()
    lines = contents.split("\n")
    return lines

# Return false if we don't have the required text
# files that we'll randomly select words from
def should_auto_generate():
    required_files = ["nouns.txt", "names.txt", "past-tense-verbs.txt"]
    for filename in required_files:
        try:
            read_file(filename)
        except:
            return False
    return True

print(should_auto_generate())

# Return a 2d array containing each word in each sentence
def split_story(story_str):
    story = []
    lines = story_str.strip().split("\n")
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            continue
        words = line.split(" ")
        story.append(words)
    return story

# Return all indexes of a word in a text
def get_occurences(text, word):
    indexes = []
    for y in range(len(text)):
        line = text[y]
        for x in range(len(line)):
            if text[y][x] == word:
                indexes.append([x, y])
    return indexes

class Story:
    def __init__(self, text_str, replacements, id):
        self.id = id
        self.story = split_story(text_str)
        self.reversed_story = []
        self.weird_story = []

        # Replacements map the user inputted word with the word
        # in the story it's supposed to replace
        self.prompts = {}
        for key in replacements:
            self.prompts[key] = get_occurences(self.story, replacements[key])

    # Generate the new story by replacing some words with user inputted words
    # Generate a "weird" version of the story by making each word in the story
    # uppercase and replacing each 'a' with 'o'
    # Generate a "reversed" version of the story by making each user inputted word reversed
    def generate_madlibs(self, words):
        self.reversed_story = copy.deepcopy(self.story)
        for label in self.prompts:
            for index in self.prompts[label]:
                x, y = index[0], index[1]
                self.story[y][x] = words[label]
                self.reversed_story[y][x] = words[label][::-1]

        self.weird_story = copy.deepcopy(self.story)
        for y in range(len(self.weird_story)):
            line = self.weird_story[y]
            for x in range(len(line)):
                self.weird_story[y][x] = self.weird_story[y][x].replace("a", "o").upper()

    def build_ui(self):
        inputs = []
        labels = []

        # Render each input labels on column and all input fields in another column
        for p in self.prompts:
            labels.append([gui.Text(p)])
            inputs.append([gui.InputText(size=25, key=p)])

        left_side = [
            [gui.Column(labels), gui.Column(inputs)],
            [gui.Button("Generate")]
        ]

        right_side = []
        # Render each line of the story on different lines
        for i in range(len(self.story)):
            line = " ".join(self.story[i])
            # The text_id_prefix is used to differentiate between text from
            # the different stories
            right_side.append([gui.Text(line, key=f"{self.id}{i}")])

        right_side.append([
            gui.Button("Normal version"), gui.Button("Weird version"), gui.Button("Reversed version")
        ])

        return [[gui.Column(left_side), gui.Column(right_side)]]

# Update the displayed text
def update_text(window, id_prefix, text):
    for i in range(len(text)):
        line = " ".join(text[i])
        window[f"{id_prefix}{i}"].update(line)

humpty_dumpty = """
Humpty Dumpty sat on a wall,
Humpty Dumpty had a great fall.
All the king's horses and all the king's men.
Couldn't put Humpty together again. 
"""
replacements = {
    "Person's First Name": "Humpty",
    "Person's Last Name": "Dumpty",
    "Verb (past tense action": "sat",
    "Job Title": "king's",
    "Animal (plural)": "horses"
}
story1 = Story(humpty_dumpty, replacements, "p1-")

buckle_my_shoe = """
One, two
Buckle my shoe
Three, four
Knock at the door
Five, six
Pick up sticks
Seven, Eight
Lay them straight
Nine, ten
A big fat hen
"""
replacements = {
    "Object (footwear)": "shoe",
    "Object (something inside a house)": "door",
    "Noun": "sticks",
    "Direction": "straight",
    "Animal": "hen"
}
story2 = Story(buckle_my_shoe, replacements, "p0-")

# Gui layout for the main menu
menu_layout = [
    [gui.Text("Which story do you want?")],
    [gui.Button("Humpty Dumpty"), gui.Button("Buckle My Shoe")]
]

# The different "screens" in the gui
layouts = [[
    gui.Column(menu_layout, key="Main Menu", visible=True),
    gui.Column(story1.build_ui(), key="UI-1", visible=False),
    gui.Column(story2.build_ui(), key="UI-2", visible=False),
]]

window = gui.Window("Madlibs", layouts)
story = None # Will be a Story object when we choose which story in the main menu

# TODO: handle punctuation

while True:
    event, values = window.read()
    if event == gui.WINDOW_CLOSED:
        break

    # Change layout based on button click
    if event == "Humpty Dumpty" or event == "Buckle My Shoe":
        window["Main Menu"].update(visible=False)
        if event == "Humpty Dumpty":
            story = story1
            window["UI-1"].update(visible=True)
        else:
            story = story2
            window["UI-2"].update(visible=True)

    # Generate the madlibs when the "Generate" button is clicked
    if "Generate" in event:
        # Only generate when all fields are filled in
        should_generate = True
        for key in story.prompts:
            if values[key] == "":
                should_generate = False
                break
        if should_generate:
            story.generate_madlibs(values)
            update_text(window, story.id, story.story)

    # Switch to different versions of the story on button click
    if "Weird version" in event:
        update_text(window, story.id, story.weird_story)
    elif "Reversed version" in event:
        update_text(window, story.id, story.reversed_story)
    elif "Normal version" in event:
        update_text(window, story.id, story.story)

window.close()