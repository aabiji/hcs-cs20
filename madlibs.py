# Madlibs
# By Abigail Adegbiji, April 26, 2024
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

# Build a the story ui. The inputs go on the left
# and the text itself goes on the right
def build_story_ui(prompts, story):
    inputs = []
    for p in prompts:
        layout = [gui.Text(p), gui.InputText(size=25, key=p)]
        inputs.append(layout)

    buttons = [gui.Button("Generate")]
    inputs.append(buttons)

    text = [[gui.Text(" ".join(line))] for line in story]

    return [[gui.Column(inputs), gui.Column(text, id="Text")]]

humpty_dumpty = """
Humpty Dumpty sat on a wall,
Humpty Dumpty had a great fall.
All the king's horses and all the king's men

Couldn't put Humpty together again. 
"""
story = split_story(humpty_dumpty)
prompts = ["First name", "Last name", "Verb" + " " * 8]
story1 = build_story_ui(prompts, story)

# GUI layout for the main menu
menu_layout = [
    [gui.Text("Which story do you want?")],
    [gui.Button("Humpty Dumpty"), gui.Button("Something else")]
]

# All the different column layouts in the gui
# For context, PySimpleGUI stores layouts as nested lists:
# https://docs.pysimplegui.com/en/latest/documentation/module/layouts/
# Start with only having the main menu visible
layouts = [[
    gui.Column(menu_layout, key="Main-Menu"),
    gui.Column(story1, key="Layout-1", visible=False),
]]
window = gui.Window("Madlibs", layouts)

while True:
    event, values = window.read()
    if event == gui.WINDOW_CLOSED:
        break

    # Main menu button click
    if event == "Humpty Dumpty":
        window["Main-Menu"].update(visible=False)
        window["Layout-1"].update(visible=True)

    # Generate mad libs button click
    if event == "Generate":
        print("hello!")

window.close()