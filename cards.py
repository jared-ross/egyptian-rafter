import random
import typing
from collections import namedtuple

from format import format_card

### Abstractions for dealing with cards

#Card = namedtuple('Card', ['rank', 'suit'])

class Card(typing.NamedTuple):
    rank: typing.Any
    suit: typing.Any
    def __str__(self):
        return format_card(self)

PLAINS = list(range(1, 11))
ROYALS = ['J', 'Q', 'K', 'A']
RANKS = PLAINS + ROYALS
SUITS = ['S', 'C', 'D', 'H']
DECK = [Card(r,s) for s in SUITS for r in RANKS]

class Cards(list):
    """A stack of cards.

    Hoisted off of a List, you can use them like lists.
    They face downwards: They have a top and bottom.
    Stack from the bottom end."""

    @classmethod
    def new_deck(cls):
        return cls(DECK)

    # Access
    # There return none if there is nothing to return
    def top_n(self, n):
        l = len(self)
        if l >= n:
            return Cards(self[0:n])
        else:
            return self
    def bot_n(self, n):
        l = len(self)
        if n == 0:
            return Cards()
        if l >= n:
            return Cards(self[-n:])
        else:
            return self
    def top_n_rest(self, n):
        l = len(self)
        if l >= n:
            return Cards(self[n:])
        else:
            return Cards()
    def bot_n_rest(self, n):
        l = len(self)
        if n == 0:
            return self
        elif l >= n:
            return Cards(self[:-n])
        else:
            return Cards()
    def top(self):
        return self.top_n(1)
    def bot(self):
        return self.bot_n(1)
    def top_rest(self):
        return self.top_n_rest(1)
    def bot_rest(self):
        return self.bot_n_rest(1)

    # Special alterations to cards
    # NOTE copy here creates a List, not a Cards
    def shuffle(self):
        copy_cards = self.copy()
        random.shuffle(copy_cards)
        return Cards(copy_cards)
    def reverse(self):
        copy_cards = self.copy()
        copy_cards.reverse()
        return Cards(copy_cards)

# Some nice predicates

def is_royal(card):
    if card.rank in ROYALS:
        return True
    else:
        return False

def is_last_n_royal(n, cards):
    return reduce(
        lambda acc, card: acc and is_royal(card),
        cards.bot_n(n),
        True)

def run_tests():
    # Basic sanity tests
    N = 56
    c = Cards.new_deck()
    assert len(c) == N
    assert len(c.shuffle()) == N
    assert c.shuffle() != c # lol
    assert len(c.reverse()) == N
    assert c == Cards.new_deck()
    assert len(c.top()) == 1
    assert len(c.bot()) == 1
    assert len(c.top_rest()) == N - 1
    assert len(c.bot_rest()) == N - 1
    assert c == Cards.new_deck()
    assert c.top() + c.top_rest() == c
    assert c.bot_rest() + c.bot() == c
    for i in range(0, N + 1):
        assert c.top_n(i) + c.top_n_rest(i) == c
        assert c.bot_n_rest(i) + c.bot_n(i) == c
        assert c.top_n(i) + c.bot_n(N-i) == c
    print("Testing cards.py: OK")

run_tests()
