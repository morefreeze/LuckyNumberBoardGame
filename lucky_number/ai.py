import random
from lucky_number.model import Command, Draw, Move, Pass
from lucky_number.game import Game


class DummyAI(object):
    def BuildCmd(self, g: Game) -> Command:
        candidate_cmds = []
        if g.drawn_card is not None:
            candidate_cmds.append(Pass())
        if g.drawn_card is None and len(g.deck) > 0:
            candidate_cmds.append(Draw())
        my_board = g.boards[g.cur_player]
        if g.drawn_card is not None:
            for i in range(my_board.n):
                for j in range(my_board.n):
                    _, succ = my_board.MakeAMove(g.drawn_card, i, j, dry_run=True)
                    if succ:
                        candidate_cmds.append(Move(g.drawn_card, i, j))
        else:
            for pc in g.public:
                for i in range(my_board.n):
                    for j in range(my_board.n):
                        _, succ = my_board.MakeAMove(pc, i, j, dry_run=True)
                        if succ:
                            candidate_cmds.append(Move(pc, i, j))
        return random.choice(candidate_cmds)
