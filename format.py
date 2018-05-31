from functools import reduce

UNICODE_ON = True;

UNICODE_SUITS = {
    'S': '\u2660',
    'C': '\u2663',
    'D': '\u2662',
    'H': '\u2661',
}

def format_card(card):
    if UNICODE_ON:
        return str(card.rank) + UNICODE_SUITS[card.suit]
    else:
        return str(card.rank) + card.suit

def format_cards(cards):
    # PROBLEM Extra space at the beginning
    return " ".join(map(format_card, cards))

def format_game(game):
    (player_cards, stack, next_player, winner) = game
    out = []
    out.append(' '.join(['Up to play: Player', str(next_player)]))
    out.append(' '.join(['Stack:', format_cards(stack.reverse())]))
    for i, cards in enumerate(player_cards):
        out.append(' '.join(['Player', str(i), ':', format_cards(cards)]))
    return out
