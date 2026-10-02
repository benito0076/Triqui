import unittest

from triqui.board import Board, O, X


class BoardTests(unittest.TestCase):
    def test_x_starts_and_turns_alternate(self):
        b = Board()
        self.assertEqual(b.turn, X)
        b.play(0)
        self.assertEqual(b.turn, O)

    def test_row_win(self):
        b = Board("XXXOO    ")
        self.assertEqual(b.winner(), X)
        self.assertTrue(b.is_over())
        self.assertEqual(b.legal_moves(), [])

    def test_diagonal_win(self):
        self.assertEqual(Board("XO  XO  X").winner(), X)

    def test_draw(self):
        b = Board("XOXXOOOXX")
        self.assertIsNone(b.winner())
        self.assertTrue(b.is_draw())

    def test_illegal_move_rejected(self):
        b = Board()
        b.play(4)
        with self.assertRaises(ValueError):
            b.play(4)


if __name__ == "__main__":
    unittest.main()
