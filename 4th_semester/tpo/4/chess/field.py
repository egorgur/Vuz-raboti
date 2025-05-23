# класс поля доски

class TChessField:
    
    def __init__(self, row: str, col: str):
        self.row = row.lower()
        self.col = col

        if not self.is_valid():
            raise ValueError(f"Invalid field: {self.row}{self.col}")

        self._occupied_by = None

    def get_row(self):
        return self.row

    def get_col(self):
        return self.col

    def is_valid(self):
        return self.row in 'abcdefgh' and self.col in '12345678'

    def is_busy(self):
        return self._occupied_by is not None

    def set_occupied(self, chessman):
        self._occupied_by = chessman

    def clear(self):
        self._occupied_by = None

    def __str__(self):
        return f"{self.row}{self.col}"
    