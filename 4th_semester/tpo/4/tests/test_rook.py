# тесты для лальи

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from chess.rook import TRook
from chess.field import TChessField
from chess.chessman import ESide
from chess.move import TChessMove
from chess.pawn import TPawn


class TestRook(unittest.TestCase):

    def setUp(self):
        self.rook = TRook(position=TChessField('a', '1'), side=ESide.WHITE)

    def test_move_vertical_up(self):
        new_position = TChessField('a', '5')
        self.rook.go_to_position(new_position)
        self.assertEqual(self.rook.get_position().get_row(), 'a')
        self.assertEqual(self.rook.get_position().get_col(), '5')

    def test_move_horizontal_right(self):
        new_position = TChessField('h', '1')
        self.rook.go_to_position(new_position)
        self.assertEqual(self.rook.get_position().get_row(), 'h')
        self.assertEqual(self.rook.get_position().get_col(), '1')

    def test_invalid_move_diagonal(self):
        new_position = TChessField('c', '3')
        with self.assertRaises(ValueError):
            self.rook.go_to_position(new_position)

    def test_invalid_move_knight_like(self):
        new_position = TChessField('b', '3')
        with self.assertRaises(ValueError):
            self.rook.go_to_position(new_position)

    def test_invalid_random_move(self):
        new_position = TChessField('e', '3')
        with self.assertRaises(ValueError):
            self.rook.go_to_position(new_position)

    def test_invalid_stay_in_place(self):
        same_position = TChessField('a', '1')
        with self.assertRaises(ValueError):
            self.rook.go_to_position(same_position)

    def test_rook_captures_pawn(self):
        attacker = TRook(TChessField('a', '1'), ESide.WHITE)
        victim_pos = TChessField('a', '4')
        victim = TPawn(victim_pos, ESide.BLACK)
        victim_pos.set_occupied(victim)

        move = TChessMove(
            chessman=attacker,
            start_field=attacker.get_position(),
            end_field=victim_pos,
            captured=victim
        )

        attacker.go_to_position(victim_pos)
        self.assertEqual(attacker.get_position(), victim_pos)
        self.assertEqual(move.asString(), "a1-a4")

    def test_rook_cannot_capture_ally(self):
        ally_pawn = TPawn(TChessField('a', '4'), ESide.WHITE)
        ally_pos = ally_pawn.get_position()
        ally_pos.set_occupied(ally_pawn)
        with self.assertRaises(ValueError):
            self.rook.go_to_position(ally_pos)


if __name__ == '__main__':
    unittest.main()
