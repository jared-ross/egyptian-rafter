"""Game Module.

Contains the core game code.
"""

import copy
from collections import namedtuple
from functools import reduce
from typing import Any, NamedTuple

from cards import Card, Cards, is_royal, is_last_n_royal


# Game Settings
PLAYERS = 2

# Helpers:
def inc_player(turn):
    return (turn + 1) % PLAYERS

def dec_player(turn):
    return (turn - 1) % PLAYERS

# Python doesn't have compose?
def compose(f, g):
    return lambda x: f(g(x))

# Game State Representation
class Game(NamedTuple):
    player_cards: Any
    stack: Any
    next_player: Any
    winner: Any = None

def new_game(deck = None):
    """Create a Game State representation of a new game."""
    if not deck:
        deck = Cards.new_deck().shuffle()

    players = []

    # NOTE This only works if there is no remainder, ie number of players is a divisor of . For now.
    cards_per_player = int(len(deck) / PLAYERS)
    for i in range(0, PLAYERS):
        players.append(deck.top_n(cards_per_player))
        deck = deck.top_n_rest(cards_per_player)

    stack = Cards() 
    next_player = 0

    return Game(players, stack, next_player)

# Royal Penaltys
def last_royal(game):
    """Find the last Royal put down in the stack
    
    Returns: (position of Royal, the Card)
    """
    if len(game.stack) > 0:
        try: 
            return next(filter(compose(is_royal, lambda c: c[1]), enumerate(reversed(game.stack))))
        except StopIteration:
            pass
    return None

royal_penalties = {
    'J': 1,
    'Q': 2,
    'K': 3,
    'A': 4,
}

# Game Operations
def flip_card(game):
    """Have the active player put a card down. Nonmutating."""
    (player_cards, stack, next_player, winner) = game
    player_cards = player_cards.copy()
    active_player = player_cards[next_player]

    # Lets place a card down
    stack = Cards(stack + active_player.top())
    player_cards[next_player] = active_player.top_rest()

    return Game(player_cards, stack, next_player)

def stack_won(game):
    """Have the stack be won by the previous player. Nonmutating.

    Additionally, change the next player to the winning player.
    """
    (player_cards, stack, next_player, winner) = game
    player_cards = player_cards.copy()
    winning_player = dec_player(next_player)
    # NOTE The stack is effectively turned upside down and put underneath
    player_cards[winning_player] = Cards(player_cards[winning_player] + stack)
    stack = Cards()

    next_player = winning_player

    return Game(player_cards, stack, next_player)

def next_turn(game):
    """Have the turn move to the next_player. Nonmutating."""
    (player_cards, stack, next_player, winner) = game
    return Game(player_cards, stack, inc_player(next_player))

def skip_out_players(game):
    """Skip players that are 'out'. Nonmutating"""
    (player_cards, stack, next_player, winner) = game

    if len(player_cards[next_player]) == 0:
        return next_turn(game)

    return game

def is_winner(game):
    return reduce(lambda acc, cards: acc or len(cards) == 0, game.player_cards, False)

def apply_wins(game):
    """Have the winner be declared, if any. Nonmutating."""
    if is_winner(game):
        (player_cards, stack, next_player, winner) = game
        winner = next(filter(lambda x: len(x[1]) != 0, enumerate(game.player_cards)))[0]
        return Game(player_cards, stack, next_player, winner)
    return game

def step_game(game):
    """Have the game progress a step. Nonmutating."""
    if game.winner != None:
        return game

    game = skip_out_players(game)
    game = flip_card(game)

    last = last_royal(game)
    if last:
        (pos, c) = last
        if pos == 0:
            game = next_turn(game)
        elif pos == royal_penalties[c.rank]:
            game = stack_won(game)
    else:
        game = next_turn(game)

    game = apply_wins(game)

    return game

def run_tests():
    for i in range(0,100):
        g = new_game()
        # Checking that they don't mutate game
        orig_g = copy.deepcopy(g)

        next_turn(g)
        assert orig_g == g
        skip_out_players(g)
        assert orig_g == g

        flip_card(g)
        assert orig_g == g

        g = flip_card(g)
        orig_g = copy.deepcopy(g)
        stack_won(g)
        assert orig_g == g

        step_game(g)
        assert orig_g == g

        for i in range(0, 10):
            g = step_game(g)
        orig_g = copy.deepcopy(g)

        step_game(g)
        assert orig_g == g
 
        flip_card(g)
        assert orig_g == g

        stack_won(g)
        assert orig_g == g
        
        apply_wins(g)
        assert orig_g == g
    print("Testing game.py: OK")

run_tests()
