import random
import unittest

from triqui.ai import minimax, pollito, zorro
from triqui.board import Board, O, X


def play_out(player_x, player_o) -> Board:
    b = Board()
    while not b.is_over():
        b.play((player_x if b.turn == X else player_o)(b))
    return b


class AITests(unittest.TestCase):
    def test_zorro_takes_the_win(self):
        self.assertEqual(zorro(Board("XX OO    ")), 2)

    def test_zorro_blocks(self):
        self.assertEqual(zorro(Board("OO  X   X")), 2)

    def test_minimax_never_loses_to_random(self):
        random.seed(0)
        for _ in range(200):
            self.assertNotEqual(play_out(minimax, pollito).winner(), O)
            self.assertNotEqual(play_out(pollito, minimax).winner(), X)

    def test_minimax_vs_minimax_is_a_draw(self):
        self.assertTrue(play_out(minimax, minimax).is_draw())


if __name__ == "__main__":
    unittest.main()
