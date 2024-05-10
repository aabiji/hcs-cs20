"""
Description:
A recreation of Simon Says. There will be 2 different patterns that are used.
A sequence of patterns will be shown to the player. The player needs to play
back those patterns in the same order they appeared using the A and B buttons.
The player's turn is over when they touch the microbit logo.
If the player successfully plays back the pattern, the game progresses to the
next level and a sound effect is played. The game gets harder with each level
with longer sequences of patterns and faster playback times.
When the user fails, a sound effect is played and the game is restarted from the beginning.

Exceptional features:
- Playing sound effects
  These docs will help: https://microbit.org/projects/make-it-code-it/make-some-noise
- Game progression with levels
- Extend the microbit library to support detecting when the microbit logo is touched
  This implementation might help: https://github.com/bbcmicrobit/micropython

Pseudocode:
```
# TODO: Be as vague as possible!!!!!!

import microbit

def generate_sequence(length, possible_images):
    # Generate a random sequence of images
    sequence = []
    for i in 0..possible_images:
        choice = #random element from possible_images
        #append choice to sequence
    return sequence

def get_sequence_length(level):
    #The sequence length grows using this formula:
    length = 0.5 * (2 ** level)
    #We're multiplying by 0.5 so that the difficulty doesn't increase
    #too sharply.
    return length

# Check if the player's sequence is the same as our sequence
def same_sequence(a, b):
    if len(a) != len(b): return False
    for i in range(len(a)):
        if a[i] != b[i]:
            return False
    return True

# We can use microbit.display.show("text") here.
def display_text(text):
    pass # TODO

# The image is a 2d array of ints (0-9)
# We iterate over each element in the array
# and use those "pixels" to construct a microbit
# image. Then we use the microbit library to
# render the image.
def display_image(image):
    pass

def play_sound_effect(type):
    pass # TODO We'll need more docs to figure this out

level = 0
game_has_started = False
player_turn = False
playback_time = 1000
user_sequence = []
our_sequence = []

# Create a list containing our 2 images:
possible_images = [microbit.Image(), microbit.Image()]

# Reset the button caches
display_text("Simon says. Press A to start")

while True:
    if not game_has_started:
        if button a is pressed:
            game_has_started = True
        continue

    # From now on we assume the game has started
    if not player_turn:

        # We respond to the player's inputted sequence
        if len(user_sequence) > 0:
            if not same_sequence(our_sequence, player_sequence):
                display_text("Loser. Game over")
                play_sound_effect("failure")
                level = 0 # Reset game
            else:
                display_text("Good! Next level")
                play_sound_effect("success")
                level += 1 # Go to the next level
                playback_time -= 10
            user_sequence = []
            continue
            # Next iteration player_turn is still False and we execute the following code

        # It's the start of a new level and we show our sequence
        display_text("Level {level}")
        length = get_sequence_length(level)
        our_sequence = generate_sequence(length, possible_images)
        for image in our_sequence:
            display_image(image)
            microbit.sleep(playback_time)
        player_turn = True
        # Clear the display

    else: # The player plays back a sequence
        if button a is pressed:
            display_image(possible_images[0])
            user_sequence.append(possible_images[0])

        if button b is pressed:
            display_image(possible_images[1])
            user_sequence.append(possible_images[1])

        if we detect touch input (touching the logo):
            player_turn = False # Now it's our turn again

    microbit.sleep(1000) # 1 second
```
"""