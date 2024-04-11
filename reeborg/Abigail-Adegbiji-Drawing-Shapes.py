import math
import turtle

window = turtle.Screen()
window.screensize(600, 600)
window.bgcolor("black")

def teleport(t, x, y):
    t.penup()
    t.goto(x, y)
    t.pendown()

t = turtle.Turtle()
t.pensize(1)
t.speed(1)
t.pencolor("white")
def draw_hexagon(t):
    side_length = 100
    angle = 360 // 6
    for i in range(6):
        t.forward(side_length)
        t.left(angle)

def draw_triangle(t, angle):
    side_length = 100
    t.setheading(angle)
    for i in range(3):
        t.forward(side_length)
        t.left(120)

teleport(t, -300, 200)
draw_hexagon(t)

teleport(t, 0, 200)
for i in range(0, 360, 360 // 8):
    draw_triangle(t, i)
