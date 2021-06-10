import random
from lucky_number.game import Game
from lucky_number.ai import DummyAI

if __name__ == '__main__':
    g = Game()
    random.seed(0)
    g.Setup(4,1)
    g.boards[0].SetAI(DummyAI())
    while not g.Win():
        g.Turn()
    last_player = (g.cur_player + g.player_num - 1) % g.player_num
    print(f"player {last_player} win!!!")