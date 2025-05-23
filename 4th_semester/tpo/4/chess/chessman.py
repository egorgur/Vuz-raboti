# базовый класс фигур

from enum import Enum
from chess.field import TChessField


class EChessmanType(Enum):
    PAWN = 'Pawn'
    ROOK = 'Rook'
    QUEEN = 'Queen'
    BISHOP = 'Bishop'
    KNIGHT = 'Knight'

class ESide(Enum):
    WHITE = 'White'
    BLACK = 'Black'

class TChessman:
    
    def __init__(self, chessman_type: EChessmanType, position: TChessField, side: ESide):
        self.chessman_type = chessman_type
        self.position = position
        self.side = side

    def get_position(self):
        return self.position
    
    def go_to_position(self, new_position: TChessField):
        if not isinstance(new_position, TChessField):
            raise ValueError("Invalid position")
        if self.position.get_row() == new_position.get_row() and \
           self.position.get_col() == new_position.get_col():
            raise ValueError("Figure must move to a new position")
        self.position = new_position 
