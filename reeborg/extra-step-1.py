"""
Solution for "Extra - Star Tower 1"
Help Reeborg build a star tower by going in 3 rows,
placing stars on the grid when x is uneven.

Author: Abigail Adegbiji
Date: March 13
"""

import library as lib

def is_even(n):
    return n % 2 == 0

grid_width = 0
def place_star_row():
    global grid_width

    # Offset x in the case where
    # the grid's width is uneven 
    # to deter star placement
    x = 0 if is_even(grid_width) else 1

    while not wall_in_front():
        if is_even(x):
            put()
        move()
        x += 1

    if is_even(x):
        put()
    grid_width = x

for y in range(3):
    place_star_row()
    if is_even(y): # Wall's on right
        turn_left()
        move()
        turn_left()
    else:
        lib.turn_right()
        move()
        lib.turn_right()
