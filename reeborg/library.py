
def turn_right():
    for i in range(3):
        turn_left()

def step(num_steps):
    for i in range(num_steps):
        move()

def plant(num_steps):
    for i in range(num_steps):
        move()
        put()
        
def discard(num_items):
    for i in range(num_items):
        put()
