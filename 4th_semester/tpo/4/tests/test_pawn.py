# тесты для пешки

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from chess.pawn import TPawn
from chess.field import TChessField
from chess.chessman import ESide, EChessmanType
from chess.move import TChessMove


class TestPawn(unittest.TestCase):

    def setUp(self):
        self.pawn = TPawn(position=TChessField('e', '2'), side=ESide.WHITE)

    def test_move_one_step_forward(self):
        new_position = TChessField('e', '3')
        self.pawn.go_to_position(new_position)
        self.assertEqual(self.pawn.get_position().get_row(), 'e')
        self.assertEqual(self.pawn.get_position().get_col(), '3')

    def test_move_to_steps_from_start(self):
        pawn = TPawn(position=TChessField('d', '2'), side=ESide.WHITE)
        new_position = TChessField('d', '4')
        pawn.go_to_position(new_position)
        self.assertEqual(pawn.get_position().get_row(), 'd')
        self.assertEqual(pawn.get_position().get_col(), '4')

    def test_capture_diagonal(self):
        new_position = TChessField('d', '3')
        enemy_pawn = TPawn(position=new_position, side=ESide.BLACK)
        new_position.set_occupied(enemy_pawn)  # чтобы поле считалось занятым

        self.pawn.go_to_position(new_position)
        self.assertEqual(self.pawn.get_position().get_row(), 'd')
        self.assertEqual(self.pawn.get_position().get_col(), '3')

    def test_invalid_move_backward(self):
        new_position = TChessField('e', '1')
        with self.assertRaises(ValueError):
            self.pawn.go_to_position(new_position)

    def test_invalid_move_sideways(self):
        new_position = TChessField('f', '2')
        with self.assertRaises(ValueError):
            self.pawn.go_to_position(new_position)

    def test_invalid_move_jump(self):
        new_position = TChessField('e', '5')
        with self.assertRaises(ValueError):
            self.pawn.go_to_position(new_position)

    def test_invalid_two_steps_not_from_start(self):
        self.pawn.go_to_position(TChessField('e', '3'))  
        with self.assertRaises(ValueError):
            self.pawn.go_to_position(TChessField('e', '5'))

    def test_invalid_stay_in_place(self):
        same_position = TChessField('e', '2')
        with self.assertRaises(ValueError):
            self.pawn.go_to_position(same_position)

    def test_invalid_field_position(self):
        with self.assertRaises(ValueError):
            TChessField('z', '5')


    def test_pawn_promotion_success(self):
        pawn = TPawn(position=TChessField('a', '7'), side=ESide.WHITE)
        new_pos = TChessField('a', '8')
        pawn.go_to_position(new_pos, promotion=EChessmanType.QUEEN)
        self.assertEqual(pawn.get_position().get_col(), '8')
        self.assertEqual(pawn.promoted_to, EChessmanType.QUEEN)

    def test_pawn_promotion_missing(self):
        pawn = TPawn(position=TChessField('b', '7'), side=ESide.WHITE)
        new_pos = TChessField('b', '8')
        with self.assertRaises(ValueError):
            pawn.go_to_position(new_pos) 

    def test_pawn_invalid_promotion_type(self):
        pawn = TPawn(position=TChessField('c', '7'), side=ESide.WHITE)
        new_pos = TChessField('c', '8')
        with self.assertRaises(ValueError):
            pawn.go_to_position(new_pos, promotion=EChessmanType.PAWN)

    def test_en_passant(self):
        black_pawn = TPawn(TChessField('e', '7'), ESide.BLACK)
        from_field = TChessField('e', '7')
        to_field = TChessField('e', '5')
        last_move = TChessMove(black_pawn, from_field, to_field)

        white_pawn = TPawn(TChessField('d', '5'), ESide.WHITE)
        new_pos = TChessField('e', '6')
        white_pawn.go_to_position(new_pos, last_move=last_move)

        self.assertEqual(white_pawn.get_position().get_row(), 'e')
        self.assertEqual(white_pawn.get_position().get_col(), '6')

    def test_pawn_cannot_capture_ally(self):
        ally = TPawn(TChessField('d', '3'), ESide.WHITE)
        pos = ally.get_position()
        pos.set_occupied(ally)
        with self.assertRaises(ValueError):
            self.pawn.go_to_position(pos)


if __name__ == '__main__':
    unittest.main()
