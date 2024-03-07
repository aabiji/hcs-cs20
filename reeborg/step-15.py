import library as lib

move()
lib.turn_right()
move()

while not at_goal():
    if wall_in_front():
        turn_left()
    move()
    if not wall_on_right():
        lib.turn_right()
        build_wall()
        turn_left()
