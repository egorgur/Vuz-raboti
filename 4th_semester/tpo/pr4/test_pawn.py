from .entities import Pawn, Rook, TChessField
import pytest



def test_white_pawn_single_forward(board):
    start = board[1][0]
    pawn = Pawn(start, "White")
    target = board[2][0]
    move = pawn.goToPosition(target, board)
    assert move.asString() == "a3"


def test_white_pawn_invalid_backward(board):
    start = board[2][0]
    pawn = Pawn(start, "White")
    target = board[1][0]
    with pytest.raises(ValueError):
        pawn.goToPosition(target, board)


def test_white_pawn_capture(board):
    start = board[1][0]
    pawn = Pawn(start, "White")
    target = board[2][1]
    target.setBusy(Pawn(target, "Black"))
    move = pawn.goToPosition(target, board)
    assert move.asString() == "axb3"


def test_white_pawn_initial_double_move(board):
    start = board[1][0]
    pawn = Pawn(start, "White")
    target = board[3][0]
    move = pawn.goToPosition(target, board)
    assert move.asString() == "a4"


def test_white_pawn_double_move_not_initial(board):
    start = board[2][0]
    pawn = Pawn(start, "White")
    pawn.has_moved = True
    target = board[4][0]  # a5
    with pytest.raises(ValueError):
        pawn.goToPosition(target, board)


def test_white_pawn_diagonal_no_capture(board):
    start = board[1][0]  # a2
    pawn = Pawn(start, "White")
    target = board[2][1]  # b3 (пустое поле)
    with pytest.raises(ValueError):
        pawn.goToPosition(target, board)


def test_white_pawn_side_move(board):
    start = board[1][0]  # a2
    pawn = Pawn(start, "White")
    target = board[1][1]  # b2
    with pytest.raises(ValueError):
        pawn.goToPosition(target, board)


def test_white_pawn_promotion(board):
    start = board[6][0]  # a7
    pawn = Pawn(start, "White")
    target = board[7][0]  # a8
    move = pawn.goToPosition(target, board)
    assert move.asString() == "a8=Q"


def test_white_pawn_capture_own_color(board):
    start = board[1][0]
    pawn = Pawn(start, "White")
    target = board[2][1]
    target.setBusy(Pawn(target, "White"))
    with pytest.raises(ValueError):
        pawn.goToPosition(target, board)


def test_black_pawn_capture_own_color(board):
    start = board[6][1]
    pawn = Pawn(start, "Black")
    target = board[5][2]
    target.setBusy(Pawn(target, "Black"))
    with pytest.raises(ValueError):
        pawn.goToPosition(target, board)
