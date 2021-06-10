from lucky_number.model import Card, CardsIsSorted, Color
from typing import List, Tuple
from random import shuffle

class Board(dict):
    n: int
    def __init__(self, n):
        self.n = n
        self.ai = None

    def SetAI(self, ai):
        self.ai = ai

    def MakeAMove(b, card: Card, x: int, y: int, dry_run=False) -> Tuple[Card, bool]:
        if not (0 <= x < b.n and 0 <= y < b.n):
            print(f"{x} {y} is out of board")
            return None, False
        replaced_card = b[x][y]
        b[x][y] = card
        if b.Fit():
            if dry_run: # dry run need restore
                b[x][y] = replaced_card
            return replaced_card, True
        b[x][y] = replaced_card
        return None, False
    
    def Fit(b) -> bool:
        for i in range(b.n):
            cards = [b[i][j] for j in range(b.n) if b[i][j].c != Color.EMPTY]
            if not CardsIsSorted(cards):
                return False
            cards = [b[j][i] for j in range(b.n) if b[j][i].c != Color.EMPTY]
            if not CardsIsSorted(cards):
                return False
        return True
    
    def Win(b) -> bool:
        for i in range(b.n):
            for j in range(b.n):
                if b[i][j].c == Color.EMPTY:
                    return False
        return True
    
    def __repr__(b) -> str:
        ret = ""
        for i, row in b.items():
            ret += "\t".join([str(card) for (j, card) in row.items()]) + "\n"
        return ret

class Game(object):
    #n: int
    player_num: int
    deck: List[Card]
    boards: List[Board]
    cur_player: int
    drawn_card: bool
    public: List[Card]

    def Setup(self, n: int, player_num: int):
        if n > 10 or n < 2:
            print("n is invalid, should be [2,10]")
            return
        if player_num < 1 or player_num > Color.TOTAL:
            print("player_num should be [1,4]")
            return
        #self.n = n
        self.player_num = player_num
        
        self.deck = [Card(Color(c), i) for i in range(1, n*(n+1)+1) for c in range(1, player_num+1)]
        shuffle(self.deck)
        self.boards = []
        for i in range(player_num):
            board = Board(n)
            for i in range(n):
                board[i] = {i: Card() for i in range(n)}
            cards = sorted([card for card in self.Draw(n)])
            for i, card in enumerate(cards):
                board.MakeAMove(card, i, i)
            print(board)
            self.boards.append(board)
        self.cur_player = 0
        self.drawn_card = None
        self.public = []

    def Draw(self, n=1) -> Card:
        for i in range(n):
            yield self.deck.pop(0)
    
    def Win(self) -> bool:
        return any([board.Win() for board in self.boards])

    def Turn(self):
        card = None
        while True:
            print(self.boards[self.cur_player])
            print(f"\npublic: {self.public}")
            if self.boards[self.cur_player].ai is None:
                cmd = input(f"player {self.cur_player} input your choice:\nm(ove) num x y\nd(raw)\np(ass)\n")
            else:
                command = self.boards[self.cur_player].ai.BuildCmd(self)
                print(command)
                cmd = command.ToCmd()
            if len(cmd) == 0:
                continue
            if cmd[0] == 'm':
                words = cmd[1:].strip().split(' ')
                try:
                    num, x, y = list(map(int, words))
                except Exception as e:
                    print(f"invalid {cmd}")
                    continue
                print("="*10)
                print(self.drawn_card)
                card = self.drawn_card
                if self.drawn_card is None: # hasn't drawn card
                    for i, pc in enumerate(self.public):
                        if pc.n == num:
                            card = self.public.pop(i)
                            break
                if card is None:
                    print(f"you choice no card, input again")
                    continue
                replaced_card, succ = self.boards[self.cur_player].MakeAMove(card, x, y)
                if not succ:
                    if self.drawn_card is None: # put card back to public
                        self.public.append(card)
                    print(f"bad move")
                    continue
                if replaced_card.c != Color.EMPTY:
                    self.public.append(replaced_card)
                break
            if cmd[0] == 'd':
                if self.drawn_card is not None:
                    print(f"you has drawn")
                    print(f"{self.drawn_card}")
                    continue
                if len(self.deck) == 0:
                    print(f"draw empty")
                    continue
                self.drawn_card = list(self.Draw())[0]
                print(f"draw {self.drawn_card}")
                if not self.TryAnyFit(self.drawn_card):
                    self.public.append(self.drawn_card)
                    # can't move, finish turn
                    break
            if cmd[0] == 'p':
                if self.drawn_card is not None:
                    self.public.append(self.drawn_card)
                else:
                    print(f"must draw first")
                    continue
                break
        print(f"{self.cur_player} is done")
        self.cur_player = (self.cur_player + 1) % self.player_num
        self.drawn_card = None

    def TryAnyFit(self, card: Card, player: int=None) -> bool:
        if player is None:
            player = self.cur_player
        board = self.boards[player]
        for i in range(board.n):
            for j in range(board.n):
                _, succ = board.MakeAMove(card, i, j, dry_run=True)
                if succ:
                    return True
        return False
