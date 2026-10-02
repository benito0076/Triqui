"""Lógica del tablero: estado, jugadas válidas y detección de ganador.

El tablero es de `size` x `size` casillas y gana quien alinee `win_length`
fichas seguidas. Las casillas se numeran desde 0, por filas.
"""

from __future__ import annotations

from functools import lru_cache
from math import isqrt

X = "X"
O = "O"
EMPTY = " "

# nombre -> (tamaño, fichas en línea para ganar)
MODES = {
    "clasico": (3, 3),
    "gran5": (5, 4),
    "gran7": (7, 5),
}


@lru_cache(maxsize=None)
def windows(size: int, win_length: int) -> tuple[tuple[int, ...], ...]:
    """Todas las líneas de `win_length` casillas consecutivas posibles."""
    found = []
    for r in range(size):
        for c in range(size):
            for dr, dc in ((0, 1), (1, 0), (1, 1), (1, -1)):
                end_r = r + dr * (win_length - 1)
                end_c = c + dc * (win_length - 1)
                if 0 <= end_r < size and 0 <= end_c < size:
                    found.append(tuple(
                        (r + dr * i) * size + c + dc * i for i in range(win_length)
                    ))
    return tuple(found)


class Board:
    def __init__(
        self, cells: str | None = None, size: int = 3, win_length: int = 3
    ) -> None:
        if cells is not None:
            size = isqrt(len(cells))
            if size * size != len(cells):
                raise ValueError("El número de casillas debe ser un cuadrado")
        if not 1 <= win_length <= size:
            raise ValueError("win_length debe estar entre 1 y el tamaño del tablero")
        self.size = size
        self.win_length = win_length
        self.cells = list(cells) if cells is not None else [EMPTY] * (size * size)

    @classmethod
    def from_mode(cls, mode: str) -> Board:
        size, win_length = MODES[mode]
        return cls(size=size, win_length=win_length)

    def copy(self) -> Board:
        return Board("".join(self.cells), win_length=self.win_length)

    @property
    def turn(self) -> str:
        """Jugador al que le toca: X empieza."""
        return X if self.cells.count(X) == self.cells.count(O) else O

    def legal_moves(self) -> list[int]:
        if self.winner():
            return []
        return [i for i, c in enumerate(self.cells) if c == EMPTY]

    def play(self, move: int) -> None:
        if move not in self.legal_moves():
            raise ValueError(f"Jugada inválida: {move}")
        self.cells[move] = self.turn

    def winning_line(self) -> tuple[int, ...] | None:
        for line in windows(self.size, self.win_length):
            first = self.cells[line[0]]
            if first != EMPTY and all(self.cells[i] == first for i in line):
                return line
        return None

    def winner(self) -> str | None:
        line = self.winning_line()
        return self.cells[line[0]] if line else None

    def is_draw(self) -> bool:
        return self.winner() is None and EMPTY not in self.cells

    def is_over(self) -> bool:
        return self.winner() is not None or EMPTY not in self.cells

    def __str__(self) -> str:
        n = self.size
        width = len(str(n * n))
        rows = []
        for r in range(n):
            row = [
                (c if c != EMPTY else str(r * n + i + 1)).rjust(width)
                for i, c in enumerate(self.cells[r * n:(r + 1) * n])
            ]
            rows.append(" " + " | ".join(row))
        sep = "\n" + "+".join("-" * (width + 2) for _ in range(n)) + "\n"
        return sep.join(rows)
