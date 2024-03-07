import library as lib

num_picked = 0
move()

for i in range(12): # First "repeat"
    move()
    if object_here():
        take()
        num_picked += 1

turn_left()
turn_left()
lib.step(11) # Second repeat
lib.discard(num_picked)
move()
