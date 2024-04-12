"""
5.9 Turtle Assignment One - Drawing Shapes
Abigail Adegbiji, April 12 2024
"""

import turtle

"""
https://stackoverflow.com/questions/36964337/how-to-draw-smily-arc-using-python-turtle
Must have author, pseudocode and inline comments
Must clearly draw your first name using turtle in block letters
Must successfully draw all objects including an exceptional object on the bottom right.  It must include one of the images from the attached document and must be drawn using functions with loops.
Must create and use your own functions that take parameters [example: drawTriangle(direction, side_length, color)]
Objects are drawn using calculations done in the code as opposed to drawing based on hard coded values
Allows for the objects to be scaled larger or smaller based on user input from a GUI (Graphical User Interface - a window input)
Allows for the user to determine the color of each object drawn immediately before drawing it, using input from a graphical window (not from command line)
Includes at least 2 other creative or dynamic features. This does not mean you need another object but that could be something you choose to do.
"""

window = turtle.Screen()
window.screensize(600, 600)
window.bgcolor("black")

t = turtle.Turtle()
t.pensize(1)
t.speed(1)
t.pencolor("white")
def teleport(t, x, y):
    t.penup()
    t.goto(x, y)
    t.pendown()

def draw_hexagon(t):
    side_length = 100
    angle = 360 // 6
    for i in range(6):
        t.forward(side_length)
        t.left(angle)

def draw_triangle(t, angle, side_length):
    t.setheading(angle)
    for i in range(3):
        t.forward(side_length)
        t.left(120)

def draw_square(t, angle, width, height):
    t.setheading(angle)
    for i in range(4):
        side = width if i % 2 == 0 else height
        t.forward(side)
        t.left(90)

def draw_shapes():
    # Draw hexagon
    teleport(t, -300, 200)
    draw_hexagon(t)

    # Draw composite triangle
    teleport(t, 0, 200)
    num_triangles = 10
    for i in range(0, 360, 360 // num_triangles):
        draw_triangle(t, i, 100)

    # Draw squares
    teleport(t, 300, 200)
    angles = [90, 0, 270, 180]
    width, height = 80, 40
    for a in angles:
        draw_square(t, a, width, height)

    window.exitonclick()