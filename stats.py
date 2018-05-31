from game_runner import GameRunner

def gen_stats(n_runs):
    wins = [0, 0]
    lengths = []
    for i in range(0, n_runs):
        gr = GameRunner()
        gr.play()
        wins[gr.game().winner] = wins[gr.game().winner] + 1
        lengths.append(gr.count)
    print(wins)
