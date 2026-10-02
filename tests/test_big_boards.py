import random
import unittest

from triqui.ai import minimax, pollito, zorro
from triqui.board import MODES, Board, O, X


def play_out(board, player_x, player_o) -> Board:
    while not board.is_over():
        board.play((player_x if board.turn == X else player_o)(board))
    return board


class BigBoardTests(unittest.TestCase):
    def test_modes(self):
        self.assertEqual(MODES["gran5"], (5, 4))
        b = Board.from_mode("gran7")
        self.assertEqual((b.size, b.win_length, len(b.cells)), (7, 5, 49))

    def test_four_in_a_row_wins_on_5x5(self):
        b = Board.from_mode("gran5")
        for i in (0, 1, 2, 3):
            b.cells[i] = X
        self.assertEqual(b.winner(), X)
        self.assertEqual(b.winning_line(), (0, 1, 2, 3))

    def test_three_in_a_row_is_not_enough_on_5x5(self):
        b = Board.from_mode("gran5")
        for i in (0, 1, 2):
            b.cells[i] = X
        self.assertIsNone(b.winner())

    def test_no_wraparound_across_rows(self):
        b = Board.from_mode("gran5")
        for i in (3, 4, 5, 6):  # termina una fila y sigue en la siguiente
            b.cells[i] = X
        self.assertIsNone(b.winner())

    def test_diagonals(self):
        b = Board.from_mode("gran5")
        for i in (1, 7, 13, 19):
            b.cells[i] = O
        self.assertEqual(b.winner(), O)
        b = Board.from_mode("gran5")
        for i in (4, 8, 12, 16):
            b.cells[i] = X
        self.assertEqual(b.winner(), X)

    def test_ai_wins_and_blocks_on_5x5(self):
        def make(x_cells, o_cells):
            b = Board.from_mode("gran5")
            for i in x_cells:
                b.cells[i] = X
            for i in o_cells:
                b.cells[i] = O
            return b

        # X tiene 0,1,2 y le toca: gana en 3
        win = make([0, 1, 2], [10, 11, 12])
        self.assertEqual(win.turn, X)
        self.assertEqual(zorro(win), 3)
        self.assertEqual(minimax(win), 3)
        # O tiene 15,16,17 y amenaza ganar en 18; a X le toca y debe bloquear
        block = make([0, 6, 24], [15, 16, 17])
        self.assertEqual(block.turn, X)
        self.assertEqual(zorro(block), 18)
        self.assertEqual(minimax(block), 18)
        # misma posición pero le toca a O: completa su línea
        attack = make([0, 6, 24, 4], [15, 16, 17])
        self.assertEqual(attack.turn, O)
        self.assertEqual(minimax(attack), 18)

    def test_minimax_beats_random_on_big_boards(self):
        random.seed(3)
        for mode in ("gran5", "gran7"):
            for _ in range(3):
                game = play_out(Board.from_mode(mode), minimax, pollito)
                self.assertNotEqual(game.winner(), O)
                game = play_out(Board.from_mode(mode), pollito, minimax)
                self.assertNotEqual(game.winner(), X)


if __name__ == "__main__":
    unittest.main()
