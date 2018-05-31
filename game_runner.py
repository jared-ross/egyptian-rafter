"""GameRunner Module. 

Runs an implementation of game.
Requires an abstracted game backend
"""

from game import new_game, step_game
import special_decks

KeepStepping = True
StopStepping = False

class GameRunner:
    def __init__(self, deck = None):
        self.history = [new_game(deck = deck)]
        self.count = 0
        self.long_game = False
        self.run()
    def game(self):
        return self.history[-1]
    def step(self):
        if self.game().winner == None:
            self.history.append(step_game(self.game()))
            self.count = self.count + 1
            return KeepStepping
        else:
            return StopStepping
    def run(self):
        while self.step() == KeepStepping:
            if self.count == 10000:
                with open('long-games', 'a') as f:
                    print(self.history[0], file = f)
                self.long_game = True
                break

def run_tests():
    gr = GameRunner(special_decks.royals_p0_only)
    assert gr.game().winner == 0

    gr = GameRunner(special_decks.royals_p1_only)
    assert gr.game().winner == 1

    print("Testing game_runner.py: OK")

run_tests()
