# Madlibs
# By Abigail Adegbiji, April 26, 2024

import tkinter as tk

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

humpty_dumpty = """
Humpty Dumpty sat on a wall,
Humpty Dumpty had a great fall.
All the king's horses and all the king's men

Couldn't put Humpty together again. 
"""
story = split_story(humpty_dumpty)

window = tk.Tk()

for line in story:
    line_str = " ".join(line)
    label = tk.Label(text=line_str)
    label.pack()

window.mainloop()