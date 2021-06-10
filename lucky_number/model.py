from enum import IntEnum
from typing import List, Union, NewType
class Color(IntEnum):
    EMPTY = 0
    RED = 1
    BLUE = 2
    GREEN = 3
    YELLOW = 4
    TOTAL = 5

class Card(object):
    c: Color
    n: int
    def __init__(self, color: Color=Color.EMPTY, num: int=0):
        self.c = color
        self.n = num
    def __lt__(self, rhs):
        if self.n == rhs.n:
            return self.c < rhs.c
        return self.n < rhs.n

    def __repr__(self):
        return f"({repr(self.c)}, {self.n})"

def CardsIsSorted(cards: List[Card]) -> bool:
    if len(cards) > 0:
        for j in range(len(cards)-1):
            if not cards[j] < cards[j+1]:
                return False
    return True

class Move(object):
    card: Card
    x: int
    y: int
    def __init__(self, c: Card, x, y:int):
        self.card = c
        self.x, self.y = x, y

    def ToCmd(self) -> str:
        return f"m {self.card.n} {self.x} {self.y}"

    def __repr__(self):
        return self.ToCmd()

class Draw(object):
    def ToCmd(self) -> str:
        return f"d"
    
    def __repr__(self):
        return self.ToCmd()

class Pass(object):
    def ToCmd(self) -> str:
        return f"p"
    
    def __repr__(self):
        return self.ToCmd()


Command = NewType('Command', Union[Pass, Draw, Move])
