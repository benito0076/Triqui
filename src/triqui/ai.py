"""Rivales de IA: cada uno recibe un tablero y devuelve una casilla."""

from __future__ import annotations

import random

from .board import EMPTY, O, X, Board, windows

WIN_SCORE = 1_000_000

# Profundidad de búsqueda de Minimax según el tamaño del tablero.
# En 3x3 llega hasta el final de la partida, así que juega perfecto.
SEARCH_DEPTH = {3: 9, 5: 4, 7: 3}


def pollito(board: Board) -> int:
    """Juega al azar."""
    return random.choice(board.legal_moves())


def _completing_move(board: Board, player: str) -> int | None:
    """Casilla con la que `player` completaría una línea, si existe."""
    need = board.win_length - 1
    for line in windows(board.size, board.win_length):
        marks = [board.cells[i] for i in line]
        if marks.count(player) == need and marks.count(EMPTY) == 1:
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
    n = board.size
    for preferred in (n * n // 2, 0, n - 1, n * (n - 1), n * n - 1):
        if preferred in legal:
            return preferred
    return random.choice(legal)


class _Search:
    """Negamax con poda alfa-beta sobre un tablero mutable."""

    def __init__(self, board: Board) -> None:
        self.n = board.size
        self.k = board.win_length
        self.cells = list(board.cells)
        self.windows = windows(self.n, self.k)
        self.by_cell: list[list[tuple[int, ...]]] = [[] for _ in self.cells]
        for w in self.windows:
            for i in w:
                self.by_cell[i].append(w)
        centre = (self.n - 1) / 2
        self.centrality = [
            -max(abs(i // self.n - centre), abs(i % self.n - centre))
            for i in range(len(self.cells))
        ]

    def wins_at(self, move: int, player: str) -> bool:
        return any(all(self.cells[i] == player for i in w) for w in self.by_cell[move])

    def candidates(self) -> list[int]:
        empties = [i for i, c in enumerate(self.cells) if c == EMPTY]
        if self.n > 3:
            marked = [i for i, c in enumerate(self.cells) if c != EMPTY]
            if not marked:
                return [len(self.cells) // 2]
            near = [
                i for i in empties
                if any(
                    abs(i // self.n - m // self.n) <= 1 and abs(i % self.n - m % self.n) <= 1
                    for m in marked
                )
            ]
            empties = near or empties
        return sorted(empties, key=lambda i: -self.centrality[i])

    def evaluate(self, player: str) -> int:
        """Puntúa las líneas abiertas: más fichas propias sin bloquear, mejor."""
        score = 0
        for w in self.windows:
            marks = [self.cells[i] for i in w]
            mine, theirs = marks.count(player), marks.count(O if player == X else X)
            if mine and not theirs:
                score += 10 ** mine
            elif theirs and not mine:
                score -= 10 ** theirs
        return score

    def negamax(self, player: str, depth: int, alpha: int, beta: int) -> int:
        """Valor de la posición para `player`, que es quien mueve."""
        moves = self.candidates()
        if not moves:
            return 0
        if depth == 0:
            return self.evaluate(player)
        rival = O if player == X else X
        best = -WIN_SCORE * 2
        for move in moves:
            self.cells[move] = player
            if self.wins_at(move, player):
                value = WIN_SCORE + depth  # ganar pronto vale más
            else:
                value = -self.negamax(rival, depth - 1, -beta, -alpha)
            self.cells[move] = EMPTY
            best = max(best, value)
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return best

    def best_move(self, player: str, depth: int) -> int:
        rival = O if player == X else X
        best_value, best_move = -WIN_SCORE * 2, None
        alpha = -WIN_SCORE * 2
        for move in self.candidates():
            self.cells[move] = player
            if self.wins_at(move, player):
                value = WIN_SCORE + depth
            else:
                value = -self.negamax(rival, depth - 1, -WIN_SCORE * 2, -alpha)
            self.cells[move] = EMPTY
            if value > best_value:
                best_value, best_move = value, move
            alpha = max(alpha, value)
        assert best_move is not None
        return best_move


def minimax(board: Board) -> int:
    """En 3x3 juega perfecto y nunca pierde. En tableros grandes busca unas
    pocas jugadas por delante y evalúa las líneas abiertas."""
    if all(c == EMPTY for c in board.cells):
        return len(board.cells) // 2  # abrir en el centro es óptimo y evita buscar
    depth = SEARCH_DEPTH.get(board.size, 3)
    return _Search(board).best_move(board.turn, depth)


RIVALS = {
    "pollito": pollito,
    "zorro": zorro,
    "minimax": minimax,
}
