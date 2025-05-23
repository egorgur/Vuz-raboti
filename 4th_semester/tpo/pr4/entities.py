from abc import ABC, abstractmethod


class TChessField:
    def __init__(self, row: int, col: int):
        if not (0 <= row <= 7) or not (0 <= col <= 7):
            raise ValueError("Invalid field coordinates")
        self.row = row
        self.col = col
        self.busy = None

    def getRow(self):
        return self.row

    def getCol(self):
        return self.col

    def isBusy(self):
        return self.busy is not None

    def setBusy(self, chessman):
        self.busy = chessman


class TChessMove:
    def __init__(
        self,
        piece_type,
        start_field: TChessField,
        end_field: TChessField,
        is_capture=False,
        is_promotion=False,
    ):
        self.piece_type = piece_type
        self.start_field = start_field
        self.end_field = end_field
        self.is_capture = is_capture
        self.is_promotion = is_promotion

    def asString(self):
        cols = ["a", "b", "c", "d", "e", "f", "g", "h"]
        start_col = cols[self.start_field.getCol()]
        end_col = cols[self.end_field.getCol()]
        end_row = self.end_field.getRow() + 1

        if self.piece_type == "Pawn":
            if self.is_promotion:
                promo = "=Q"
            else:
                promo = ""
            if self.is_capture:
                return f"{start_col}x{end_col}{end_row}{promo}"
            else:
                return f"{end_col}{end_row}{promo}"
        elif self.piece_type == "Rook":
            symbol = "R"
            if self.is_capture:
                return f"{symbol}x{end_col}{end_row}"
            else:
                return f"{symbol}{end_col}{end_row}"
        else:
            return ""


class TChessman(ABC):
    @abstractmethod
    def getPosition(self):
        pass

    @abstractmethod
    def goToPosition(self, target_field: TChessField, board):
        pass


class Pawn(TChessman):
    def __init__(self, position: TChessField, side: str):
        self.position = position
        self.side = side
        self.has_moved = False

    def getPosition(self):
        return self.position

    def goToPosition(self, target_field: TChessField, board):
        original_position = self.position
        current_row = original_position.getRow()
        current_col = original_position.getCol()
        target_row = target_field.getRow()
        target_col = target_field.getCol()

        direction = 1 if self.side == "White" else -1
        start_row = 1 if self.side == "White" else 6

        is_promotion = (self.side == "White" and target_row == 7) or (
            self.side == "Black" and target_row == 0
        )

        if is_promotion:
            self.position = target_field
            return TChessMove(
                "Pawn", original_position, target_field, is_promotion=True
            )

        if current_col == target_col:
            if target_row == current_row + direction and not target_field.isBusy():
                self.position = target_field
                self.has_moved = True
                return TChessMove("Pawn", original_position, target_field)
            elif (
                current_row == start_row
                and target_row == current_row + 2 * direction
                and not target_field.isBusy()
            ):
                intermediate_row = current_row + direction
                intermediate_field = board[intermediate_row][current_col]
                if not intermediate_field.isBusy():
                    self.position = target_field
                    self.has_moved = True
                    return TChessMove("Pawn", original_position, target_field)
        elif (
            abs(target_col - current_col) == 1 and target_row == current_row + direction
        ):
            if target_field.isBusy() and target_field.busy.side != self.side:
                self.position = target_field
                self.has_moved = True
                return TChessMove(
                    "Pawn", original_position, target_field, is_capture=True
                )

        raise ValueError("Invalid move for Pawn")


class Rook(TChessman):
    def __init__(self, position: TChessField, side: str):
        self.position = position
        self.side = side

    def getPosition(self):
        return self.position

    def goToPosition(self, target_field: TChessField, board):
        original_position = self.position
        current_row = original_position.getRow()
        current_col = original_position.getCol()
        target_row = target_field.getRow()
        target_col = target_field.getCol()

        if not (0 <= target_row <= 7) or not (0 <= target_col <= 7):
            raise ValueError("Move out of bounds")

        if current_row != target_row and current_col != target_col:
            raise ValueError("Invalid move for Rook")

        if target_field.isBusy() and target_field.busy.side == self.side:
            raise ValueError("Cannot capture own piece")

        if current_row == target_row:
            step = 1 if target_col > current_col else -1
            for col in range(current_col + step, target_col, step):
                field = board[current_row][col]
                if field.isBusy():
                    raise ValueError("Path is blocked")
        else:
            step = 1 if target_row > current_row else -1
            for row in range(current_row + step, target_row, step):
                field = board[row][current_col]
                if field.isBusy():
                    raise ValueError("Path is blocked")

        is_capture = target_field.isBusy() and target_field.busy.side != self.side
        self.position = target_field
        return TChessMove(
            "Rook", original_position, target_field, is_capture=is_capture
        )
