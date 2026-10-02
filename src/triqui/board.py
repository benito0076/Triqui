"""Lógica del tablero: estado, jugadas válidas y detección de ganador."""

from __future__ import annotations

X = "X"
O = "O"
EMPTY = " "

LINES = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # filas
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columnas
    (0, 4, 8), (2, 4, 6),             # diagonales
)


class Board:
    """Tablero 3x3. Las casillas se numeran de 0 a 8, por filas."""

    def __init__(self, cells: str | None = None) -> None:
        self.cells = list(cells) if cells else [EMPTY] * 9
        if len(self.cells) != 9:
            raise ValueError("El tablero debe tener 9 casillas")

    def copy(self) -> Board:
        return Board("".join(self.cells))

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

    def winning_line(self) -> tuple[int, int, int] | None:
        for a, b, c in LINES:
            if self.cells[a] != EMPTY and self.cells[a] == self.cells[b] == self.cells[c]:
                return (a, b, c)
        return None

    def winner(self) -> str | None:
        line = self.winning_line()
        return self.cells[line[0]] if line else None

    def is_draw(self) -> bool:
        return self.winner() is None and EMPTY not in self.cells

    def is_over(self) -> bool:
        return self.winner() is not None or EMPTY not in self.cells

    def __str__(self) -> str:
        rows = []
        for r in range(3):
            row = [
                c if c != EMPTY else str(r * 3 + i + 1)
                for i, c in enumerate(self.cells[r * 3:r * 3 + 3])
            ]
            rows.append(" " + " | ".join(row))
        return "\n---+---+---\n".join(rows)
