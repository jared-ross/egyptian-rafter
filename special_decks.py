from cards import Card, Cards, ROYALS, DECK

royals_p0_only = Cards(list(filter(lambda c: c.rank in ROYALS, DECK)) \
               + list(filter(lambda c: not c.rank in ROYALS, DECK)))

royals_p1_only = Cards(list(filter(lambda c: not c.rank in ROYALS, DECK)) \
               + list(filter(lambda c: c.rank in ROYALS, DECK)))


