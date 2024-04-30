# Madlibs
# By Abigail Adegbiji, April 26, 2024
import copy
import PySimpleGUI as gui

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

def build_story_ui(text_id_prefix, prompts, story):
    inputs = []
    labels = []
    # Render each input labels on column and all input fields in another column
    for p in prompts:
        labels.append([gui.Text(p)])
        inputs.append([gui.InputText(size=25, key=p)])

    left_side = [
        [gui.Column(labels), gui.Column(inputs)],
        [gui.Button("Generate")]
    ]

    right_side = []
    # Render each line of the story on different lines
    for i in range(len(story)):
        line = " ".join(story[i])
        right_side.append([gui.Text(line, key=f"{text_id_prefix}{i}")])

    right_side.append([
        gui.Button("Normal version"), gui.Button("Weird version"), gui.Button("Reversed version")
    ])

    return [[gui.Column(left_side), gui.Column(right_side)]]

# Generate the new story by replacing some words with user inputted words
# Generate a "weird" version of the story by making each word in the story
# uppercase and replacing each 'a' with 'o'
# Generate a "reversed" version of the story by making each user inputted word reversed
def generate_stories(prompts, words, story):
    reversed_story = copy.deepcopy(story)
    for label in prompts:
        for index in prompts[label]:
            x, y = index[1], index[0]
            story[y][x] = words[label]
            reversed_story[y][x] = words[label][::-1]

    weird_story = copy.deepcopy(story)
    for y in range(len(weird_story)):
        line = weird_story[y]
        for x in range(len(line)):
            weird_story[y][x] = weird_story[y][x].replace("a", "o").upper()

    return story, reversed_story, weird_story

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
A big fat hen!
"""
shoe_prompts = {
    "Object (footwear)": [[1, 2]],
    "Object (something house related)": [[3, 3]],
    "Noun": [[5, 2]],
    "Direction": [[7, 2]],
    "Animal": [[9, 3]]
}
shoe_id = "p0-"

humpty_dumpty = """
Humpty Dumpty sat on a wall,
Humpty Dumpty had a great fall.
All the king's horses and all the king's men

Couldn't put Humpty together again. 
"""
dumpty_prompts = {
    "Person's First Name": [[0, 0], [1, 0], [3, 2]],
    "Person's Last Name": [[0, 1], [1, 1]],
    "Verb (past tense action)": [[1, 5]],
    "Job Title": [[2, 2], [2, 7]],
    "Animal (plural)": [[2, 3]],
}
dumpty_id = "p1-"

ui1 = build_story_ui(dumpty_id, list(dumpty_prompts.keys()), split_story(humpty_dumpty))
ui2 = build_story_ui(shoe_id, list(shoe_prompts.keys()), split_story(buckle_my_shoe))

# GUI layout for the main menu
menu_layout = [
    [gui.Text("Which story do you want?")],
    [gui.Button("Humpty Dumpty"), gui.Button("Buckle My Shoe")]
]

# All the different column layouts in the gui
# For context, PySimpleGUI stores layouts as nested lists:
# https://docs.pysimplegui.com/en/latest/documentation/module/layouts/
# Start with only having the main menu visible
layouts = [[
    gui.Column(menu_layout, key="Main Menu", visible=True),
    gui.Column(ui1, key="UI-1", visible=False),
    gui.Column(ui2, key="UI-2", visible=False),
]]
window = gui.Window("Madlibs", layouts)

# Update the displayed text
def update_text(id_prefix, text):
    for i in range(len(text)):
        line = " ".join(text[i])
        window[f"{id_prefix}{i}"].update(line)

# Map inputs to the indexes of the words they'll replace
# The indexes are the line index, then the index of the word within the line
prompts = {}
story = []
weird_story = []
reversed_story = []
text_prefix = ""

while True:
    event, values = window.read()
    if event == gui.WINDOW_CLOSED:
        break

    # Change layout based on button click
    if event == "Humpty Dumpty" or event == "Buckle My Shoe":
        window["Main Menu"].update(visible=False)
        if event == "Humpty Dumpty":
            story = split_story(humpty_dumpty)
            prompts = dumpty_prompts
            window["UI-1"].update(visible=True)
            text_prefix = dumpty_id
        else:
            story = split_story(buckle_my_shoe)
            prompts = shoe_prompts
            window["UI-2"].update(visible=True)
            text_prefix = shoe_id

    # Generate the madlibs when the "Generate" button is clicked
    if "Generate" in event:
        story, reversed_story, weird_story = generate_stories(prompts, values, story)
        update_text(text_prefix, story)

    # Switch to different versions of the story on button click
    if "Weird version" in event:
        update_text(text_prefix, weird_story)
    elif "Reversed version" in event:
        update_text(text_prefix, reversed_story)
    elif "Normal version" in event:
        update_text(text_prefix, story)

window.close()