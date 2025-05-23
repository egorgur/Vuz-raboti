from .entities import Pawn, Rook, TChessField
import pytest


def test_rook_horizontal_move(board):
    start = board[0][0]
    rook = Rook(start, "White")
    target = board[0][3]
    move = rook.goToPosition(target, board)
    assert move.asString() == "Rd1"


def test_rook_capture(board):
    start = board[0][0]
    rook = Rook(start, "White")
    target = board[0][3]
    target.setBusy(Rook(target, "Black"))
    move = rook.goToPosition(target, board)
    assert move.asString() == "Rxd1"


def test_rook_blocked_path(board):
    start = board[0][0]
    rook = Rook(start, "White")
    block = board[0][1]
    block.setBusy(Pawn(block, "White"))
    target = board[0][2]
    with pytest.raises(ValueError):
        rook.goToPosition(target, board)


def test_rook_diagonal_move(board):
    start = board[0][0]
    rook = Rook(start, "White")
    target = board[3][3]
    with pytest.raises(ValueError):
        rook.goToPosition(target, board)


def test_rook_move_out_of_bounds(board):
    start = board[0][0]
    rook = Rook(start, "White")
    with pytest.raises(ValueError):
        invalid_field = TChessField(8, 0)
        rook.goToPosition(invalid_field, board)


def test_rook_capture_own_color_white(board):
    start = board[0][0]
    rook = Rook(start, "White")
    target = board[0][3]
    target.setBusy(Rook(target, "White"))
    with pytest.raises(ValueError):
        rook.goToPosition(target, board)


def test_rook_capture_own_color_black(board):
    start = board[7][7]
    rook = Rook(start, "Black")
    target = board[7][4]
    target.setBusy(Rook(target, "Black"))
    with pytest.raises(ValueError):
        rook.goToPosition(target, board)
