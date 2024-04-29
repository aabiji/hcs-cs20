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
    labels = []
    for p in prompts:
        labels.append([gui.Text(p)])
        inputs.append([gui.InputText(size=25, key=p)])

    aligned = [[gui.Column(labels), gui.Column(inputs)]]

    buttons = [gui.Button("Generate")]
    aligned.append(buttons)

    text = []
    for i in range(len(story)):
        line = " ".join(story[i])
        text.append([gui.Text(line, key=f"p-{i}")])

    return [[gui.Column(aligned), gui.Column(text)]]

humpty_dumpty = """
Humpty Dumpty sat on a wall,
Humpty Dumpty had a great fall.
All the king's horses and all the king's men

Couldn't put Humpty together again. 
"""
story = split_story(humpty_dumpty)

# Map inputs to the indexes of the words they'll replace
# The indexes are the line index, then the index of the word within the line
prompts = {
    "Person's First Name": [[0, 0], [1, 0], [3, 2]],
    "Person's Last Name": [[0, 1], [1, 1]],
    "Verb (past tense action)": [[1, 5]],
    "Job Title": [[2, 2], [2, 7]],
    "Animal (plural)": [[2, 3]],
}

story_ui = build_story_ui(list(prompts.keys()), story)

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
    gui.Column(story_ui, key="Layout-1", visible=False),
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
        # Replace words in the story with user inputted words
        for label in prompts:
            for index in prompts[label]:
                story[index[0]][index[1]] = values[label]

        # Update the displayed text
        for i in range(len(story)):
            line = " ".join(story[i])
            element = window[f"p-{i}"].update(line)

window.close()