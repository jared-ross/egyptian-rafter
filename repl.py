"""REPL Module

Used for visualising a single game.
For testing and debugging.
"""

import curses
import datetime
import time
import numpy

from game import last_royal, is_winner
from game_runner import GameRunner
from format import format_game


class Repl:
    PAD_HEIGHT = 30
    PAD_WIDTH = 100

    IDEAL_FPS = 30

    stdscr = None
    contents_pad = None

    fps = 0

    game_runner = None

    key_bindings = {
        'n': lambda self: (self.game_runner.step(), self.latest_history()),
        'r': lambda self: self.reset(),
        'p': lambda self: (self.game_runner.play(), self.latest_history()),
        '.': lambda self: self.next_in_history(),
        ',': lambda self: self.prev_in_history(),
    }

    monitors = {
        'Last Royal': lambda self: last_royal(self.game_runner.history[self.history_pos]),
        'Counter': lambda self: str(self.game_runner.count),
        'Position in History': lambda self: str(self.history_pos),
        'Frames per second': lambda self: str(self.fps),
        'Winner': lambda self: self.game_runner.history[self.history_pos].winner,
        # 'Time': lambda _: str(datetime.datetime.time(datetime.datetime.now()))
    }

    def __init__(self, stdscr):
        self.contents_pad = curses.newpad(self.PAD_HEIGHT, self.PAD_WIDTH)
        self.refresh_pad()

        self.game_runner = GameRunner()
        self.history_pos = 0

        self.stdscr = stdscr
        self.stdscr.nodelay(True)

        self.run()

    def reset(self):
        self.game_runner = GameRunner()
        self.history_pos = self.game_runner.count

    def next_in_history(self):
        self.history_pos = min(self.history_pos + 1, self.game_runner.count)

    def prev_in_history(self):
        self.history_pos = max(self.history_pos - 1, 0)

    def latest_history(self):
        self.history_pos = self.game_runner.count

    def get_monitor_lines(self):
        return [(str(desc) + ": " + str(val(self))) for (desc, val) in self.monitors.items()]

    def refresh_pad(self):
        self.contents_pad.noutrefresh(0, 0, 1, 1, self.PAD_HEIGHT, self.PAD_WIDTH)

    def render(self, help_lines, game_lines, monitor_lines):
        """Takes lines of different sections and puts them onto pads on the screen."""

        lines = []
        lines = lines + ["Egyptian Rafter Simulator"]
        lines = lines + ["-------------------------"]
        lines = lines + [""]
        lines = lines + game_lines
        lines = lines + [""]
        lines = lines + [""]
        lines = lines + monitor_lines
        lines = lines + [""]
        lines = lines + help_lines

        self.contents_pad.erase()
        self.contents_pad.addstr(0, 0, '\n'.join(lines))
        self.refresh_pad()
        curses.doupdate()


    def run(self):
        last_frame = datetime.datetime.now()
        self.last5_fps = [0 for i in range(0, 200)]

        # (More like prel)
        while True:
            # Make sure my loops aren't running too fast
            # This works but not accurately
            self.fps = numpy.mean(self.last5_fps)
            delta = max(1/self.IDEAL_FPS - 1/self.fps, 0.0)
            # Sleep is not sleeping enough?
            time.sleep(delta)

            help_lines = ['Press a key: Reset (r), Next (n), Quit (q), Play(p)']
            game_lines = format_game(self.game_runner.history[self.history_pos])
            monitor_lines = self.get_monitor_lines()

            self.render(help_lines, game_lines, monitor_lines)

            try:
                k = self.stdscr.getkey()
                if (k == 'q'):
                    break
                try:
                    self.key_bindings[k](self)
                except KeyError:
                    pass
            except curses.error:
                pass

            self.last5_fps.append(1 / (datetime.datetime.now() - last_frame).total_seconds())
            self.last5_fps.pop(0)
            last_frame = datetime.datetime.now()



if __name__ == "__main__":
    repl = curses.wrapper(Repl)
