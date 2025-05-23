# класс для описания хода

from chess.field import TChessField
from chess.chessman import TChessman


class TChessMove:

    def __init__(self, chessman: TChessman, start_field: TChessField, end_field: TChessField, captured: TChessman = None, promotion: str = None):
        self.chessman = chessman            
        self.start_field = start_field      
        self.end_field = end_field          
        self.captured = captured            
        self.promotion = promotion          

    def asString(self):
        move_str = f"{self.start_field}-{self.end_field}"
        if self.promotion:
            move_str += f"={self.promotion}"
        return move_str

    def __str__(self):
        return self.asString()
