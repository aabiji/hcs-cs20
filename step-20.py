"""
Same objective as step 15, going around and 
putting walls at the left if there's none.

Author: Abigail Adegbiji
Date: March 12
"""

import library as lib

# Go to the left of the green square
lib.step(3)
lib.turn_right()
move()

while not at_goal():
    if wall_in_front():
        turn_left()
    move()
    if right_is_clear():
        lib.turn_right()
        if front_is_clear(): # how to differentiate between wall and space?
            move()
        else:
            build_wall()
            turn_left()