"""
5.9 Turtle Assignment One - Drawing Shapes
Abigail Adegbiji, April 15 2024

Allows for the objects to be scaled larger or smaller based on user input from a GUI (Graphical User Interface - a window input)
Allows for the user to determine the color of each object drawn immediately before drawing it, using input from a graphical window (not from command line)
Includes at least 2 other creative or dynamic features. This does not mean you need another object but that could be something you choose to do.
"""

import math
import turtle

def teleport(t, x, y):
    t.penup()
    t.goto(x, y)
    t.pendown()

def draw_hexagon(t):
    side_length = 50
    angle = 360 // 6
    for i in range(6):
        t.forward(side_length)
        t.left(angle)

def draw_square(t, angle, width, height):
    t.setheading(angle)
    for i in range(4):
        length = width if i % 2 == 0 else height
        t.forward(length)
        t.left(90)

def draw_triangle(t, angle, side_length, start_in_middle=False):
    t.setheading(angle)

    # Move halfway back
    if start_in_middle:
        t.left(180)
        t.forward(side_length / 2)
        t.left(180)

    for i in range(3):
        t.forward(side_length)
        t.left(120)

    # Move back to the center position
    if start_in_middle:
        t.forward(side_length / 2)

# Draw a capital 'a' and return the width of the rendered letter
def draw_a(t):
    length = 100
    inner_length = length / 2
    base_length = length / 5
    bridge_length = length / 10
    arch_angles = [60, 300]
    previous_x, previous_y = t.xcor(), t.ycor()

    # Draw an outer arch
    for i in range(2):
        t.setheading(arch_angles[i])
        t.forward(length)

    teleport(t, previous_x, previous_y)

    # Draw the left letter base
    t.setheading(0)
    t.forward(base_length)

    # Draw an inner arch with a small bridge in the middle
    for i in range(2):
        t.setheading(arch_angles[i])
        t.forward(inner_length)
        if i == 0:
            t.setheading(0)
            t.forward(bridge_length)

    # Draw the right letter base
    t.setheading(0)
    t.forward(base_length)

    # We want to find the width of the area under the angled line
    half_length = length * math.cos(math.radians(arch_angles[0]))

    teleport(t, previous_x + half_length, previous_y + half_length)
    draw_triangle(t, 0, bridge_length, start_in_middle=True)

    # Return the width of the rendered letter
    return half_length * 2

# Draw a capital 'b' and return the width of the rendered letter
def draw_b(t):
    length = 90
    hole_radius = 8
    top_radius, top_angle = 25, 152
    bottom_radius, bottom_angle = 35, 170
    x, y = t.xcor(), t.ycor()

    # Draw line going up
    t.setheading(90)
    t.forward(length)

    # Our "curves" are just circles rendered up to
    # a certain angle. Here we drawe the bottom and top curves:
    teleport(t, x, y)
    t.setheading(-30)
    t.circle(bottom_radius, bottom_angle)
    t.setheading(62)
    t.circle(top_radius, top_angle)

    # Draw inner holes
    teleport(t, x + 15, y + (length - 15))
    t.circle(hole_radius)
    teleport(t, x + 20, y + 35)
    t.circle(hole_radius)

    return bottom_radius + top_radius

# Draw a capital 'g' and return the width of the rendered letter
def draw_g(t):
    edge_width, edge_height = 25, 15
    outer_radius, inner_radius = 50, 35
    new_x = t.xcor() + outer_radius + edge_width
    new_y = t.ycor() + outer_radius * 2 - edge_height
    teleport(t, new_x, new_y)

    # Draw outer shape
    t.setheading(150)
    t.circle(outer_radius, 300)

    # Draw outer horizantal edge going in
    t.setheading(180)
    t.forward(edge_width)

    teleport(t, new_x, new_y)

    # Draw vertical edge going down
    t.setheading(270)
    t.forward(edge_height)

    # Draw inner shape
    t.setheading(140)
    t.circle(inner_radius, 280)

    # Complete drawing the horizantal edge
    t.setheading(180)
    t.forward(edge_width)
    t.setheading(90)
    t.forward(edge_height)
    t.setheading(0)
    t.forward(edge_width)

    return inner_radius * 2 + edge_height

# Draw a capital 'i' and return the width of the rendered letter
def draw_i(t):
    width, height = 20, 90
    draw_square(t, 0, width, height)
    return width

# Draw a capital 'l' and return the width of the rendered letter
def draw_l(t):
    edge_size = 20
    outer_length = 90
    inner_length = outer_length - edge_size
    angles = [180, 90]

    end_x, end_y = t.xcor() + outer_length, t.ycor()
    teleport(t, end_x, end_y)

    # Draw outer shape
    for a in angles:
        t.setheading(a)
        t.forward(outer_length)

    # Draw bottom right edge
    teleport(t, end_x, end_y)
    t.forward(edge_size)

    # Draw inner shape
    for a in angles:
        t.setheading(a)
        t.forward(inner_length)

    # Draw top edge
    t.setheading(180)
    t.forward(edge_size)

    return outer_length

def draw_text(text):
    # Map letters to drawing functions
    drawers = {
        "A": draw_a,
        "B": draw_b,
        "I": draw_i,
        "G": draw_g,
        "L": draw_l,
    }

    spacing = 20
    x, y = t.xcor(), t.ycor()
    for c in text:
        width = drawers[c.upper()](t)
        x += width + spacing
        teleport(t, x, y)

# Draw an "exceptional" shape (tesselation)
def draw_tesselation(t):
    length = 20
    num_sides = 8
    right_angle = 90
    center_x, center_y = t.xcor(), t.ycor()
    turns = [270, 45, 135, 315, 90, 315, 135, 45]
    for a in range(0, 360, 360 // num_sides):
        teleport(t, center_x, center_y)

        # Draw the inner "crest"
        # Really it's composed of 8 squares connected 
        # to lines oriented at different angles
        t.setheading(a)
        t.forward(length)
        t.left(right_angle // 2)
        for i in range(6):
            t.forward(length)
            t.right(right_angle)

        # Draw the outer "crown" associated to the line
        t.setheading(a)
        t.forward(length + (length / 2))
        for i, turn in enumerate(turns):
            t.left(turn)
            t.forward(length + (length / 5))

def draw_shapes(t):
    teleport(t, -280, 200)
    draw_hexagon(t)

    # Draw composite triangle shape
    # For each of the 10 triangles, we'll draw them at the
    # different spots angled successively at (360 / 10) degrees
    teleport(t, -80, 200)
    num_triangles = 10
    for i in range(0, 360, 360 // num_triangles):
        draw_triangle(t, i, 80)

    # Draw star shape
    # For each of the 5 triangles, we'll draw them at the
    # same spot angled successively at (360 / 5) degrees
    teleport(t, 120, 200)
    num_triangles = 5
    for i in range(0, 360, 360 // num_triangles):
        draw_triangle(t, i, 80, True)

    # Draw composite square shape by drawing squares at different angles
    teleport(t, -200, 0)
    angles = [90, 0, 270, 180]
    width, height = 80, 40
    for a in angles:
        draw_square(t, a, width, height)

    teleport(t, 100, 0)
    draw_tesselation(t)

    teleport(t, -300, -300)
    draw_text("Abigail")

    window.exitonclick()

window = turtle.Screen()
window.setup(650, 650)
window.bgcolor("black")

t = turtle.Turtle()
t.pensize(1)
t.speed("fastest")
t.pencolor("white")

draw_shapes(t)