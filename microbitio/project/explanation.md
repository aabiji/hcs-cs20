I figured it out!!!!!!

Microbit has this repl and the repl just uses a fork of micropython to execute python code.
Now, when you send a command to the repl really what you're doing is just executing the code
from the library the micropython implements. And so really, the only that's needed is this:
The cs20 wrapper library literally just sends code to the microbit. So really, we can take this demo code:

```py
# Imports go at the top
from microbit import *


# Code in a 'while True:' loop repeats forever
while True:
    display.show(Image.HEART)
    sleep(1000)
    display.scroll('Hello')

    if pin_logo.is_touched():
        display.show(Image.HAPPY)
```

And extract this:

```py
microbit.pin_logo.is_touched()
```

And send that code to the microbit through the repl!!!
