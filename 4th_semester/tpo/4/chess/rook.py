# класс ладьи

from chess.chessman import TChessman, EChessmanType, ESide
from chess.field import TChessField


class TRook(TChessman):

    def __init__(self, position: TChessField, side: ESide):
        super().__init__(EChessmanType.ROOK, position, side)

    def go_to_position(self, new_position: TChessField):
        same_row = self.position.get_row() == new_position.get_row()
        same_col = self.position.get_col() == new_position.get_col()

        if not (same_row or same_col):
            raise ValueError("Invalid rook move")

        if new_position.is_busy():
            occupant = new_position._occupied_by
            if occupant.side == self.side:
                raise ValueError("Cannot capture ally")

        super().go_to_position(new_position)
