# Egyptian Rafter

A simulator of a card game I used to play as a child, also known as
"Egyptian Ratscrew", similar to "Beg My Neighbour".

To do still is adding simulated snaps to the game, the part that
differentiates it from "Beg My Neighbour". (Right now it is just "Beg
My Neighbour")


## Description of Files

- `game.py`: This is contains the main logic of the game.

- `cards.py`: This contains an overly general abstraction of a pack of
  cards with some simple utilities.

- `game_runner.py`: This contains an object used for running an
  abstracted game. It keeps track of the game length and the whole
  history of the game.

- `format.py`: This contains formating functions for displaying a
  card, cards, and a game.

- `repl.py`: Contains a curses repl for processing and viewing a
  single game, useful for debugging and verifying the game is working.


# Copyright, Licensing and Warranty

Copyright © 2018 Jared Ross &lt;<jared.b.ross@gmail.com>&gt;
All Rights Reserved

Additionally this code is provided under the Mozilla Public License
2.0 For more information see LICENSE.txt

Use this code at your own risk.
