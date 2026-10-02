"""Rivales de IA: cada uno recibe un tablero y devuelve una casilla (0-8)."""

from __future__ import annotations

import random
from functools import lru_cache

from .board import EMPTY, LINES, O, X, Board


def pollito(board: Board) -> int:
    """Juega al azar."""
    return random.choice(board.legal_moves())


def _completing_move(board: Board, player: str) -> int | None:
    """Casilla con la que `player` completaría una línea, si existe."""
    for line in LINES:
        marks = [board.cells[i] for i in line]
        if marks.count(player) == 2 and marks.count(EMPTY) == 1:
            return line[marks.index(EMPTY)]
    return None


def zorro(board: Board) -> int:
    """Gana si puede, bloquea si debe, prefiere centro y esquinas; no ve trampas."""
    me = board.turn
    rival = O if me == X else X
    for player in (me, rival):
        move = _completing_move(board, player)
        if move is not None:
            return move
    legal = board.legal_moves()
    for preferred in (4, 0, 2, 6, 8):
        if preferred in legal:
            return preferred
    return random.choice(legal)


@lru_cache(maxsize=None)
def _minimax(cells: str, me: str) -> tuple[int, int | None]:
    """Devuelve (valor, mejor jugada) desde la vista de `me`.

    La caché evita recalcular posiciones repetidas: en 3x3 hay solo unas
    pocas miles, así que no hace falta poda alfa-beta todavía.
    """
    board = Board(cells)
    winner = board.winner()
    if winner:
        return (1 if winner == me else -1), None
    if board.is_draw():
        return 0, None
    maximizing = board.turn == me
    best_value, best_move = (-2 if maximizing else 2), None
    for move in board.legal_moves():
        child = board.copy()
        child.play(move)
        value, _ = _minimax("".join(child.cells), me)
        if (maximizing and value > best_value) or (not maximizing and value < best_value):
            best_value, best_move = value, move
    return best_value, best_move


def minimax(board: Board) -> int:
    """Juego perfecto: nunca pierde."""
    _, move = _minimax("".join(board.cells), board.turn)
    assert move is not None
    return move


RIVALS = {
    "pollito": pollito,
    "zorro": zorro,
    "minimax": minimax,
}
