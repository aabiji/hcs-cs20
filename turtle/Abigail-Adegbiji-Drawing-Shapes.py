"""
5.9 Turtle Assignment One - Drawing Shapes
Abigail Adegbiji, April 15 2024

Features:
- Draw any text (a-z)
"""

import math
import turtle

def teleport(t, x, y):
    t.penup()
    t.goto(x, y)
    t.pendown()

def draw_hexagon(t, side_length, color):
    angle = 360 // 6
    t.pencolor(color)
    for i in range(6):
        t.forward(side_length)
        t.left(angle)

def draw_square(t, angle, width, height, color):
    t.setheading(angle)
    t.pencolor(color)
    for i in range(4):
        length = width if i % 2 == 0 else height
        t.forward(length)
        t.left(90)

def draw_triangle(t, angle, side_length, color, start_in_middle=False):
    t.setheading(angle)
    t.pencolor(color)

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
def draw_a(t, length, color):
    length = length + 10
    inner_length = length / 2
    base_length = length / 5
    bridge_length = length / 10
    arch_angles = [60, 300]
    previous_x, previous_y = t.xcor(), t.ycor()

    t.pencolor(color)

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
    draw_triangle(t, 0, bridge_length, color, start_in_middle=True)

    # Return the width of the rendered letter
    return half_length * 2

# Draw a capital 'b' and return the width of the rendered letter
def draw_b(t, length, color):
    x, y = t.xcor(), t.ycor()
    top_radius = length / 4
    bottom_radius = length / 3
    hole_radius = length // 11

    t.pencolor(color)

    # Draw line going up
    t.setheading(90)
    t.forward(length)

    # Our "curves" are just circles rendered up to
    # a certain angle. Here we draw the bottom and top curves:
    teleport(t, x, y)
    t.setheading(-30)
    t.circle(bottom_radius, 180)

    ## Determine the tilt of the upper semi circle
    # Since the radians stays the same anywhere on the circumference
    # of the circle, we can get the center of the circle by subtracting the radius
    cx, cy = t.xcor() - top_radius, t.ycor() + top_radius
    # Next we can determine the angle from our current position to the center position
    angle = math.atan2(t.ycor() - cy, t.xcor() - cx)
    # Our "tilt" will now be the absolute angle in degrees
    tilt = abs(math.degrees(angle))

    t.setheading(tilt)
    t.circle(top_radius, 180)

    # Draw inner holes
    teleport(t, x + 15, y + (length - 15))
    t.circle(hole_radius)
    teleport(t, x + top_radius * 2, y + (length - top_radius * 2))
    t.circle(hole_radius)

    return bottom_radius + top_radius

# Draw a capital 'g' and return the width of the rendered letter
# TODO: properly scale this
def draw_g(t, size, color):
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
def draw_i(t, size, color):
    width, height = size / 4, size
    draw_square(t, 0, width, height, color)
    return width

# Draw a capital 'l' and return the width of the rendered letter
def draw_l(t, size, color):
    t.pencolor(color)

    edge_size = size / 4
    outer_length = size
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

# Draw a capital 'c' and return the width of the rendered letter
def draw_c(t, size, color):
    ratio = 8
    tilt, angle = 170, 210
    outer_edge_size, inner_edge_size = size / 10, size / 6
    outer_radius, inner_radius = size, size - size / ratio
    x, y = t.xcor(), t.ycor()

    t.pencolor(color)
    t.setheading(tilt)
    t.circle(outer_radius, angle)

    teleport(t, x, y)
    t.setheading(270)
    t.forward(outer_edge_size)

    t.setheading(tilt)
    t.circle(inner_radius, angle)

    t.setheading(270)
    t.forward(inner_edge_size)

    # We won't return the outer_radius since we end at the bottom
    # right of the letter
    return outer_edge_size

def draw_d(t, size, color):
    t.pencolor(color)
    radius = size / 2

    t.setheading(270)
    t.forward(size)

    t.setheading(0)
    t.circle(radius, 180)

    teleport(t, t.xcor() + radius / 3, t.ycor() - size / 3)
    t.setheading(270)

    inner_size = size / 4
    t.forward(inner_size)

    inner_radius = radius / 8
    t.setheading(0)
    t.circle(inner_radius, 180)

def draw_e(t, size, color): pass
def draw_f(t, size, color): pass
def draw_h(t, size, color): pass
def draw_j(t, size, color): pass
def draw_k(t, size, color): pass
def draw_m(t, size, color): pass
def draw_n(t, size, color): pass
def draw_o(t, size, color): pass
def draw_p(t, size, color): pass
def draw_q(t, size, color): pass
def draw_r(t, size, color): pass
def draw_s(t, size, color): pass
def draw_t(t, size, color): pass
def draw_u(t, size, color): pass
def draw_v(t, size, color): pass
def draw_w(t, size, color): pass
def draw_x(t, size, color): pass
def draw_y(t, size, color): pass
def draw_z(t, size, color): pass

def draw_text(text, size, color):
    # Map letters to drawing functions
    drawers = {
        "a": draw_a,
        "b": draw_b,
        "c": draw_c,
        "d": draw_d,
        "e": draw_e,
        "f": draw_f,
        "g": draw_g,
        "h": draw_h,
        "i": draw_i,
        "j": draw_j,
        "k": draw_k,
        "l": draw_l,
        "m": draw_m,
        "n": draw_n,
        "o": draw_o,
        "p": draw_p,
        "q": draw_q,
        "r": draw_r,
        "s": draw_s,
        "t": draw_t,
        "u": draw_u,
        "v": draw_v,
        "w": draw_w,
        "x": draw_x,
        "y": draw_y,
        "z": draw_z,
    }

    spacing = 20
    x, y = t.xcor(), t.ycor()
    for c in text:
        width = drawers[c.lower()](t, size, color)
        x += width + spacing
        teleport(t, x, y)

# Draw an "exceptional" shape (tesselation)
def draw_tesselation(t, length, color):
    t.pencolor(color)

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

# Return the user inputted shape size and color
def configure_shape():
    color = ""
    num = turtle.numinput("Configure shape", "Shape size", default=100, minval=50, maxval=500)

    # Ensure that the user inputs a valid color by continuing to prompt them if they didn't
    while True:
        color = turtle.textinput("Configure shape", "Shape color")
        try:
            turtle.color(color)
            break
        except:
            color = turtle.textinput("Configure shape", "Shape color")

    # Default to white
    if color == "":
        color = "white"

    return int(num), color

def draw_shapes(t):
    """
    teleport(t, -280, 200)
    size, color = configure_shape()
    draw_hexagon(t, size, color)

    # Draw composite triangle shape
    # For each of the 10 triangles, we'll draw them at the
    # different spots angled successively at (360 / 10) degrees
    teleport(t, -80, 200)
    num_triangles = 10
    size, color = configure_shape()
    for i in range(0, 360, 360 // num_triangles):
        draw_triangle(t, i, size, color)

    # Draw star shape
    # For each of the 5 triangles, we'll draw them at the
    # same spot angled successively at (360 / 5) degrees
    teleport(t, 120, 200)
    num_triangles = 5
    size, color = configure_shape()
    for i in range(0, 360, 360 // num_triangles):
        draw_triangle(t, i, size, color, True)

    # Draw composite square shape by drawing squares at different angles
    teleport(t, -200, 0)
    angles = [90, 0, 270, 180]
    size, color = configure_shape()
    for a in angles:
        draw_square(t, a, size, size / 2, color)

    teleport(t, 100, 0)
    size, color = configure_shape()
    draw_tesselation(t, size, color)

    teleport(t, -300, -300)
    size, color = configure_shape()
    draw_text("abigail", size, color)
    """

    draw_d(t, 100, "white")

    window.exitonclick()

window = turtle.Screen()
window.setup(650, 650)
window.bgcolor("black")

t = turtle.Turtle()
t.pensize(1)
t.speed("slowest")
t.pencolor("white")

draw_shapes(t)