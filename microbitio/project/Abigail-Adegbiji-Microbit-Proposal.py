"""
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
        determine the length of the sequence based on the level
        generate a random sequence of images of that length

        for each image in our random sequence:
            display the image
            pause for however many miliseconds our playback speed is

        it's the player's turn now
"""