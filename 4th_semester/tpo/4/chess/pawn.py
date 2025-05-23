# класс пешки

from chess.chessman import TChessman, EChessmanType, ESide
from chess.field import TChessField
from chess.move import TChessMove


class TPawn(TChessman):

    def __init__(self, position: TChessField, side: ESide):
        super().__init__(EChessmanType.PAWN, position, side)
        self.promoted_to = None

    def go_to_position(
        self,
        new_position: TChessField,
        promotion: EChessmanType = None,
        last_move: TChessMove = None
    ):
        if self.position.get_row() == new_position.get_row() and \
           self.position.get_col() == new_position.get_col():
            raise ValueError("Pawn must move to a new position")

        start_row = int(self.position.get_col())
        end_row = int(new_position.get_col())
        start_col = ord(self.position.get_row())
        end_col = ord(new_position.get_row())

        direction = 1 if self.side == ESide.WHITE else -1

        row_diff = end_row - start_row
        col_diff = end_col - start_col
        abs_col_diff = abs(col_diff)

        valid = False

        if col_diff == 0 and row_diff == direction and not new_position.is_busy():
            valid = True

        elif col_diff == 0 and row_diff == 2 * direction and not new_position.is_busy():
            if (self.side == ESide.WHITE and start_row == 2) or (self.side == ESide.BLACK and start_row == 7):
                valid = True

        elif abs_col_diff == 1 and row_diff == direction and new_position.is_busy():
            if new_position._occupied_by.side == self.side:
                raise ValueError("Cannot capture ally")
            valid = True

        elif abs_col_diff == 1 and row_diff == direction and not new_position.is_busy():
            if last_move and last_move.chessman.chessman_type == EChessmanType.PAWN:
                from_field = last_move.start_field
                to_field = last_move.end_field

                last_row_diff = int(to_field.get_col()) - int(from_field.get_col())

                if abs(last_row_diff) == 2 and to_field.get_row() == new_position.get_row():
                    if int(to_field.get_col()) == start_row:
                        valid = True

        if not valid:
            raise ValueError("Invalid pawn move")

        if (self.side == ESide.WHITE and end_row == 8) or (self.side == ESide.BLACK and end_row == 1):
            if promotion is None:
                raise ValueError("Promotion required")
            if promotion not in [EChessmanType.QUEEN, EChessmanType.ROOK, EChessmanType.BISHOP, EChessmanType.KNIGHT]:
                raise ValueError("Invalid promotion type")
            self.promoted_to = promotion

        super().go_to_position(new_position)
