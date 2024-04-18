"""
5.9 Turtle Assignment One - Drawing Shapes
Abigail Adegbiji, April 15 2024
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

def draw_square(t, angle, width, height, color, start_in_middle=False):
    t.setheading(angle)
    t.pencolor(color)

    # Move halfway back
    if start_in_middle:
        t.left(180)
        t.forward(width / 2)
        t.left(180)

    for i in range(4):
        length = width if i % 2 == 0 else height
        t.forward(length)
        t.left(90)

    # Move back to the center position
    if start_in_middle:
        t.forward(width / 2)

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
    t.fillcolor(color)
    t.begin_fill()

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

    t.end_fill()

    # Draw the right letter base
    t.setheading(0)
    t.forward(base_length)

    t.fillcolor("black")
    t.begin_fill()

    # We want to find the width of the area under the angled line
    half_length = length * math.cos(math.radians(arch_angles[0]))

    teleport(t, previous_x + half_length, previous_y + half_length)
    draw_triangle(t, 0, bridge_length, color, start_in_middle=True)

    t.end_fill()

    # Return the width of the rendered letter
    return half_length * 2

# Draw a capital 'b' and return the width of the rendered letter
def draw_b(t, length, color):
    x, y = t.xcor(), t.ycor()
    top_radius = length / 4
    bottom_radius = length / 3
    hole_radius = length // 11

    t.pencolor(color)
    t.fillcolor(color)

    # Draw line going up
    t.setheading(90)
    t.forward(length * 0.9)

    # Our "curves" are just circles rendered up to
    # a certain angle. Here we draw the bottom and top curves:
    teleport(t, x, y)
    t.begin_fill()
    t.setheading(-30)
    t.circle(bottom_radius, 180)

    t.setheading(45) # 45 degree tilt
    t.circle(top_radius, 180)
    t.end_fill()

    # Draw inner holes
    t.fillcolor("black")
    x, y = t.xcor(), t.ycor()
    hole_x = [
        x + top_radius / 2,  # Top hole
        x + top_radius / 1.5 # Bottom hole
    ]
    hole_y = [
        y - top_radius / 2, # Top hole
        (y - length) + bottom_radius * 1.25 # Bottom hole
    ]
    for i in range(2):
        t.begin_fill()
        teleport(t, hole_x[i], hole_y[i])
        t.circle(hole_radius)
        t.end_fill()

    return bottom_radius + top_radius

# Draw a capital 'g' and return the width of the rendered letter
def draw_g(t, size, color):
    edge_width = size / 5
    edge_height = size / 10
    outer_radius = size / 2
    inner_radius = size / 2.5
    outer_tilt, inner_tilt = 150, 145

    # Move right and upwards to preserve the position of the letter
    teleport(t, t.xcor() + outer_radius * 1.8, t.ycor() + outer_radius * 1.8)
    x, y = t.xcor(), t.ycor()

    t.fillcolor(color)
    t.pencolor(color)
    t.begin_fill()

    # Draw outer curve
    t.setheading(outer_tilt)
    t.circle(outer_radius, 310)
    edge_x, edge_y = t.xcor(), t.ycor()

    # Draw top edge
    teleport(t, x, y)
    t.setheading(270)
    t.forward(edge_height)

    # Draw inner curve
    t.setheading(inner_tilt)
    t.circle(inner_radius, 300)

    # Draw inner edge
    t.setheading(180)
    t.forward(edge_width)
    t.setheading(90)
    t.forward(edge_y - t.ycor())
    t.setheading(0)
    t.forward(edge_x - t.xcor())

    t.end_fill()
    return outer_radius * 2

# Draw a capital 'i' and return the width of the rendered letter
def draw_i(t, size, color):
    t.fillcolor(color)
    t.begin_fill()
    width, height = size / 4, size
    draw_square(t, 0, width, height, color)
    t.end_fill()
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

    t.fillcolor(color)
    t.begin_fill()

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

    t.end_fill()

    return outer_length

def draw_text(text, size, color):
    # Map letters to drawing functions
    drawers = {
        "a": draw_a,
        "b": draw_b,
        "g": draw_g,
        "i": draw_i,
        "l": draw_l,
    }

    spacing = 20
    x, y = t.xcor(), t.ycor()
    for c in text:
        width = drawers[c.lower()](t, size, color)
        x += width + spacing
        teleport(t, x, y)

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

def draw_tesselation2(t, size, color):
    line_length = size / 3
    triangle_size = line_length / 3
    center_x, center_y = t.xcor(), t.ycor()

    for angle in range(0, 360, 360 // 8):
        offset_angle = angle - 90
        teleport(t, center_x, center_y)
        t.setheading(angle)

        t.forward(line_length / 2)
        draw_triangle(t, offset_angle, triangle_size, color, start_in_middle=True)

        t.setheading(angle)
        t.penup()
        t.forward(triangle_size)
        t.pendown()

        t.forward(line_length)
        width = line_length * 1.5
        height = line_length / 2
        draw_square(t, offset_angle, width, height, color, start_in_middle=True)

        t.setheading(angle)
        t.penup()
        t.forward(height)
        t.pendown()

        t.left(45)
        t.forward(height)
        t.left(45)
        t.forward(height)
        t.right(10)
        t.forward(height)
        t.left(45)
        t.forward(height)

# Return the user inputted shape size and color
def get_shape_info():
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
    size, color = get_shape_info()
    draw_hexagon(t, size, color)

    # Draw composite triangle shape
    # For each of the 10 triangles, we'll draw them at the
    # different spots angled successively at (360 / 10) degrees
    teleport(t, -80, 200)
    num_triangles = 10
    size, color = get_shape_info()
    for i in range(0, 360, 360 // num_triangles):
        draw_triangle(t, i, size, color)

    # Draw star shape
    # For each of the 5 triangles, we'll draw them at the
    # same spot angled successively at (360 / 5) degrees
    teleport(t, 120, 200)
    num_triangles = 5
    size, color = get_shape_info()
    for i in range(0, 360, 360 // num_triangles):
        draw_triangle(t, i, size, color, True)

    # Draw composite square shape by drawing squares at different angles
    teleport(t, -200, 0)
    angles = [90, 0, 270, 180]
    size, color = get_shape_info()
    for a in angles:
        draw_square(t, a, size, size / 2, color)

    teleport(t, 100, 0)
    size, color = get_shape_info()
    draw_tesselation(t, size, color)

    teleport(t, -300, -300)
    size, color = get_shape_info()
    teleport(t, -300, 0)
    draw_text("abigail", size, color)
    """

    draw_tesselation2(t, 100, "white")

    window.exitonclick()

window = turtle.Screen()
window.setup(650, 650)
window.bgcolor("black")

t = turtle.Turtle()
t.pensize(1)
t.speed("slowest")
t.pencolor("white")

draw_shapes(t)