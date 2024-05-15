"""
Author: Abigail Adegbiji
Date: May 11, 2024

Description:
A recreation of Simon Says. A sequence of images will be shown to
the player and the player needs to play back those images in the
same order they appeared. If the user fails to do so, the game is restarted
from the beginning. If they succeed, the game progresses to the next level.
The game gets harder with each level with there being longer sequences
of images and faster playback times.

Exceptional features:
- Playing sound effects
  These docs will help: https://microbit.org/projects/make-it-code-it/make-some-noise
- Game progression with levels
- Extend the microbit library to support detecting when the microbit logo is touched
  This implementation might help: https://github.com/bbcmicrobit/micropython

Pseudocode:
say "Simon Says. Press the A button to start the game"

loop forever:
    if the player hasn't started the game and the a button is pressed:
        start the game

    if the game hasn't been started:
        keep saying "Simon Says. Press the A button to start the game"
        jump to the next iteration of the loop

    if it's the player's turn:
        if the a button is pressed:
            display the corresponding image
            add that image to the player's inputted sequence of images

        if the b button is pressed:
            display the corresponding image
            add that image to the player's inputted sequence of images

        if the microbit logo is touched:
            it's our turn now

    if it's our turn:

        if the player has previously inputted a sequence:
            if the player's sequence is not the same as the sequence we showed them
                play the failure sound effect
                say "Game over"
                reset the playback speed back to normal
                reset the game (go back to the first level)
            else:
                progress to the next level (ex: level += 1)
                decrease the playback speed
                play the success sound effect
                say "Next level"

        say what level it is (ex: "Level 1")
        say "Simon Says"

        determine the length of the sequence based on the level

        generate a random sequence of images of that length:
            we have 2 different images we could choose from,
            so just iterate from 0 to the length of the sequence
            and add a randomly chosen image to our sequence each time

        for each image in our sequence:
            display the image
            pause for however many miliseconds our playback speed is

        it's the player's turn now
"""

import microbit
import random

def logo_was_touched():
    """
    The "command" were sending to the repl is just python code.
    Under the hood microbit uses a fork of micropython to compile
    and execute a subset of python directly.
    Touch detection of the logo is already implemented in microbit for us.
    See this commit: https://github.com/bbcmicrobit/micropython/commit/9ddc573245e9ce9f9d6c0b847b6597fece877af9
    """
    command = "print(pin_logo.is_touched())"
    microbit.repl.send_command(command)
    response = microbit.repl.wait_response()
    return eval(response) # True or False

def generate_sequence(level, images):
    sequence = []
    length = 2 * level
    for i in range(0, length + 1):
        sequence.append(random.choice(images))
    return sequence

def equals(a, b):
    if len(a) != len(b):
        return False
    for i in range(len(a)):
        if b[i] != a[i]:
            return False
    return True

game_has_started = False
is_players_turn = False

playback_speed = 1000
level = 0

our_sequence = []
player_sequence = []
possible_images = [microbit.Image.YES, microbit.Image.NO]

# Reset the button caches
microbit.button_a.was_pressed()
microbit.button_b.was_pressed()

microbit.display.show("Simon Says. Press the A button to start")

while True:
    if not game_has_started:
        if microbit.button_a.was_pressed():
            game_has_started = True
        microbit.display.clear()
        continue

    if is_players_turn:
        image_index  = -1

        if microbit.button_a.was_pressed():
            image_index = 0
        if microbit.button_b.was_pressed():
            image_index = 1

        if image_index != -1:
            image = possible_images[image_index]
            microbit.display.show(image)
            player_sequence.append(image)

        if logo_was_touched():
            is_players_turn = False

    else: # It's our turn

        if len(player_sequence) > 0: # Player inputted a sequence
            if not equals(our_sequence, player_sequence):
                print("Play failure sound effect")
                microbit.display.show("Game over")
                player_sequence = []
                playback_speed = 1000
                level = 0
            else:
                print("Play success sound effect")
                playback_speed = max(playback_speed - 50, 100)
                level += 1

        microbit.display.show(f"Level {level}. Simon Says:")

        our_sequence = generate_sequence(level, possible_images)
        for image in our_sequence:
            microbit.display.show(image)
            microbit.sleep(playback_speed)
            microbit.display.clear()
            microbit.sleep(playback_speed)

        is_players_turn = True