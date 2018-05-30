import random
import copy
import curses
import time
from collections import deque
from functools import reduce

# Game Settings
PLAYERS = 2

# Immutability Aides, I am doing everything in tuples
def shuffle(tup):
    col = list(tup)
    random.shuffle(col)
    return tuple(col)

def reverse(tup):
    col = list(tup)
    col.reverse()
    return tuple(col)

# Creating a deck
PLAINS = tuple(range(1,11))
ROYALS = ('J', 'Q', 'K', 'A')
RANKS = PLAINS + ROYALS
SUITS = ('S', 'C', 'D', 'H')
FRESH_DECK = tuple({'rank': r, 'suit': s} for s in SUITS for r in RANKS)


# Game Rules
# Helpers:
def nextTurn(turn):
    turn = turn + 1
    if turn < PLAYERS:
        return turn
    else:
        return 0

def prevTurn(turn):
    turn = turn - 1
    if turn >= 0:
        return turn
    else:
        return PLAYERS - 1

def isRoyal(card):
    if card['rank'] in ROYALS:
        return True
    else:
        return False

def isLastNCardsRoyal(n, stack):
    return reduce(
        lambda acc, card: acc and isRoyal(card),
        stack[-n:],
        True)

def createStandardAction(nBefore, rank):
    def action(game):
        (players, stack, turn) = game
        players = list(players)

        # print('Standard Action Test:', nBefore, rank, ':', len(stack) > nBefore, len(stack) > nBefore and stack[-(nBefore + 1)]['rank'] == rank, len(stack) > nBefore and not isLastNCardsRoyal(nBefore, stack))
        if len(stack) > nBefore and stack[-(nBefore + 1)]['rank'] == rank and not isLastNCardsRoyal(nBefore, stack):
            print('Action:', rank)
            winningPlayer = prevTurn(turn)
            # PROBLEM: terminology mix up between turn and players, a deck of cards vs a number
            players[winningPlayer] = list(players[winningPlayer]) + list(reverse(stack))
            return (tuple(players), (), turn)
        else:
            return game
    return action

# Action: list of functions to run on the game
ACTIONS = (
    createStandardAction(1, 'J'),
    createStandardAction(2, 'Q'),
    createStandardAction(3, 'K'),
    createStandardAction(4, 'A'),
)


# A game state will be a tupple of (players (P0, P1), stack, turn)

def newGame():
    deck = shuffle(FRESH_DECK)
    p0 = tuple(deck[0:26])
    p1 = tuple(deck[26:52])
    stack = ()
    turn = 0
    return ((p0, p1), stack, turn)

def step(game):
    (players, stack, turn) = game
    players = list(players)
    stack = list(stack)
    activePlayer = deque(players[turn])

    # Lets place a card down
    # KEYPOINT The stack datastructure has its base to the left, and top to the right.
    stack.append(activePlayer.popleft())
    players[turn] = tuple(activePlayer)

    game =  (tuple(players), stack, turn)

    # Lets check for actions
    game = reduce(lambda game, action: action(game), ACTIONS, game)

    (players, stack, turn) = game

    # Finally increment the turn
    game =  (players, stack, nextTurn(turn))

    return game

# Printing

UNICODE_SUITS = {
    'S': '\u2660',
    'C': '\u2663',
    'D': '\u2662',
    'H': '\u2661',
}

def formatCard(c):
    # return str(c['rank']) + UNICODE_SUITS[c['suit']]
    return str(c['rank']) + c['suit']

def formatCards(cards):
    # PROBLEM Extra space at the beginning
    return reduce(
        lambda acc, cur: acc + " " + cur,
        map(formatCard, cards),
        ""
    )

def formatGame(game):
    (players, stack, turn) = game
    outLines = []
    outLines.append(' '.join(['Up to play: Player', str(turn)]))
    outLines.append(' '.join(['Stack:', formatCards(reverse(stack)[0:5]), '(...)']))
    for i, cards in enumerate(players):
        outLines.append(' '.join(['Player', str(i), ':', formatCards(cards[0:5]), '(...)']))
    return '\n'.join(outLines)

def reset():
    global game
    global history
    game = newGame()
    history = [game]
    return formatGame(game)

def n():
    global game
    game = step(game)
    history.append(game)
    return formatGame(game)

def p():
    return formatGame(game)

def repl(stdscr):
    reset()
    stdscr.keypad(True)
    stdscr.addstr(0,0, 'Press a key: Reset (r), Print (p), Next (n), Quit (q)')
    stdscr.refresh()
    gamePad = curses.newpad(10, 50)

    def display(str):
        gamePad.addstr(0, 0, str)
        gamePad.refresh(0, 0, 2, 0, 12, 50)

    display(formatGame(game))

    keyBindings = {
        'n': lambda: n(),
        'p': lambda: p(),
        'r': lambda: reset(),
    }

    while True:
        k = stdscr.getkey()
        if (k == 'q'):
            break
        display(keyBindings[k]())

curses.wrapper(repl)

