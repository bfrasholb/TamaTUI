# TamaTUI - Build your own terminal application!

------------------------------------------------

## TamaTUI - Snake

As a demonstration of python curses, I wrote the game Snake in python using curses! This is a very simple game that I will be using throughout this project and document to explain concepts related to both game loops and curses. A demonstration of this game will be shown (during our first TamaTUI session), but you can come see what the game looks like by asking me when you see me around campus. It even has score leaderboards so make sure you practice your snake skills at home before trying for that #1 spot!

## Curses

Curses is a library available in both python and C. We will be using curses throughout this project to render a program in the terminal, using a (y, x) point based system.

## Getting Started

All of the information in this document can be found in the two links below:

1. [Python Documentation](https://docs.python.org/3/)
2. [Python Curses](https://docs.python.org/3/howto/curses.html)

### Initialise the app

1. Import the curses module: `import curses`
2. Initialise the screen: `stdscr = curses.initscr()`
3. Change settings to the more familiar game-style input capture:

```PYTHON
import curses

curses.noecho() # Turn off key echoing
curses.cbreak() # Turn off buffered input
curses.curs_set(0) # Set cursor visibility to off
stdscr.keypadmode(True) # Turn on keypad mode
```

Printing text to the screen is the only way for your TUI program to interact with the user, so it is important to create reusable systems which accurately print the desired text.
Printing in curses is done with strings, while a single character can be printed, it is best to think of all prints as character arrays to assist with visualising behaviour.

### Exiting

Much like turning on a computer (or a lightswitch for example), to turn it off, or exit the curses application we flip the switches back:

```PYTHON
curses.echo() # Turn on key echoing
curses.cbreak() # Turn on buffered input
curses.curs_set(1) # Set cursor visibility to on
stdscr.keypadmode(False) # Turn off keypad mode
curses.endwin() # Close the program
```

All of this however can cause issues in your terminal if done incorrectly (such as; leaving the terminal in keypad mode when exiting, or continuing to not echo keypresses which makes typing into a terminal very difficult). So for safety, and simplicity just know that `curses.wrapper(main)` will return an initialised screen to the function `main()`.

This means that the bare minimum curses application looks vaguely like:

```PYTHON
#!/usr/bin/env python3

import curses


def main(window: curses.window):
    window.keypad(True) # Turn on keypad mode
    curses.noecho() # Turn off key echoing
    curses.curs_set(0) # Set cursor visibility
    curses.cbreak() # Turn off buffered input

    window.addstr(0, 0, "Hello World!") # Print a String at  (0, 0)

    while 1: # Loop so the game doesn't exit instantly
        window.refresh() # Refresh

if __name__ == '__main__':
    curses.wrapper(main) # Initialise and return the window to main()

```

### Printing

To print to a window we use the method, `window.addstr(y, x, str)`.
All curses coordinates use (y, x) syntax, and (0, 0) begins at the upper-left corner of the screen, meaning x increases to the right, and y increases moving down.
Creating good handler functions for calculating coordinates can make rendering a curses application very easy, and hard-coding print coordinates can make behaviour unpredictable.

### Refreshing or Drawing

After printing a string to the screen, curses needs to be told to reflect changes to the screen. There are two main ways to do this and they use varying amounts of resources dependent on how much is being updated on screen.

1. `window.refresh()` - has it's moments

    - refreshes every point on the window
    - removing old draws
    - update new draws
    - resource intensive

2. `window.noutrefresh()` - more on this one below

    - 'draws' in a buffer file
    - overwrites previous draws
    - does NOT remove previous draws
    - less resource intensive, as no graphical rendering takes place until `curses.doupdate()` called

## Pads and Windows

Curses will error if the entirety of a window is not able to be displayed within the terminal window.

- width is determined by the number of characters that can fit on one line and is represented by `curses.COLS`
- height is determined by the number of lines that can fit on screen and is represented by `curses.ROWS`
- can have multiple windows (IF they can all be displayed simultaneously without overlap)

Curses can also print to a pad. All, part or none of a pad may be visible in a window. Curses can create as many pads in a program as you need and they can be created and used like this:

```PYTHON
new_pad = curses.newpad(height, width)
new_pad.addstr(0, 0, "Hello World!")
new_pad.noutrefresh(0, 0, 0, 0, 0, 0)
```

As printing outside the bounds of the terminal window produces an index range error, it is important to make sure your program does not try to print outside the bounds of the screen.
You should also know that curses can be picky with what it considers in bounds of the screen, for example `(max_y, max_x)` can be incredibly inconsistent to print at.
We do this by printing to our pads using the `.addstr()` method, and then update the screen with the `.noutrefresh()` and `curses.doupdate()` methods.

The `.refresh()` and `.noutrefresh()` methods can both be used with no arguments, defaulting to printing the full pad or window onto the window (yes, the window behaves exactly like a pad). Using the arguments however, you can control strict bounds on the screen, and avoid writing the entire screen every refresh. Both methods take identical arguments, with the two main differences between them being:

- `.noutrefresh()` is buffered, and requires `curses.doupdate()`
- `.refresh()` is not buffered, and writes immediately

Both methods take arguments of the form of three co-ordinate pairs:

```PYTHON
new_pad.noutrefresh(pad_y, pad_x, start_y, start_x, end_y, end_x)
```

Where:

- `pad_y, pad_x` are the coordinates to read from in the pad (typically (0, 0) is desired)
- `start_y, start_x` and `end_y, end_x` are the coordinate bounds WITHIN the window.

Basically, the refresh methods say 'read the pad buffer from `pad_y, pad_x`, and write the contents that will be visible in the `(start_x, start_y), (end_x, end_y)` section of the window'
So the character at (0, 0) in the pad, will be written to `start_y, start_x` on the window.

A pad may be ANY size relative to the window. To avoid complex calculations for coordinate rendering, print everything in pads relative to (0, 0), then use each pad as a section of the screen. Just because the section of the pad being drawn, is being drawn onto a small segment of the window, does not mean that there is wasted space. The window coordinates passed to refresh methods should realistically never change per pad, however depending on your use case this may be helpful.

### Capturing Input

Curses has several methods for caputring input.

1. `window.getch()`

    - returns ASCII key-codes
    - easy to use for input binding
    - frustrating to use for string input

2. `window.getkey()`

    - returns a string representation of the key
    - excellent for string input

3. `window.get_wch()`

    - almost the same as getkey(), but returns key codes in bytes instead

### App Logic / Game Logic

Congratulations, you've now made it to the part of the project where you get to venture off on your own and fill your curses window with whatever you please.
I highly recommend organising your code strictly by file, class, and role. Some key functions and categories are:

- Rendering
- Object Classes (Player, Timer)
- Menu Classes/Functions
- Input Handling
- Movement
- Coordinate Systems

The goal of this project is for you to invent your own systems and structures, that help you to produce a very basic but functional program!
However you would like to do this, please go for it. Just remember, this is meant to be an enjoyable project that keeps you invested.

Whether you are writing a game or a more 'serious' app, it is helpful to understand [game loops](https://gamedesigning.org/learn/game-loop/).
A game loop is an order of repetitive steps, that when looked at from a broader perspective forms an enjoyable repetitive activity (game). Good examples include:

- collecting blocks, then building with those blocks, to collect better blocks (Minecraft, Terraria)
- completing puzzles to unlock more puzzles to complete to unlock more puzzles (puzzle apps, sudoku.com)
- ...viewing files and directories in a directory, to then change into a parent or child directory and continue...

The most resource intensive part of your curses game loop will likely always be drawing, and so it is important to draw (remembering that drawing is painting changes onto the window, not the pad) as little as possible.
Your game loop should probably look something like:

1. Game Checks (Is the snake dead?)
2. Game Rules (Snake always moves forward)
3. Render the bottom layer first, then the top (Score, Food, Snake)
4. Draw All Changes! This does not mean draw an entire pad- this will likely cause a flicker in your final program
5. Handle input
