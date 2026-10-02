"""Interfaz de consola para jugar contra la IA o contra otra persona."""

from __future__ import annotations

import argparse

from .ai import RIVALS
from .board import X, Board


def ask_move(board: Board) -> int:
    legal = board.legal_moves()
    while True:
        raw = input(f"Turno de {board.turn}. Casilla (1-9): ").strip()
        if raw.isdigit() and int(raw) - 1 in legal:
            return int(raw) - 1
        print("Jugada inválida, intenta de nuevo.")


def play_game(rival: str | None) -> None:
    board = Board()
    human = X  # contra la IA, la persona siempre es X
    while not board.is_over():
        print("\n" + str(board) + "\n")
        if rival and board.turn != human:
            move = RIVALS[rival](board)
            print(f"{rival.capitalize()} juega en {move + 1}")
        else:
            move = ask_move(board)
        board.play(move)
    print("\n" + str(board) + "\n")
    winner = board.winner()
    print(f"¡Gana {winner}!" if winner else "Empate.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Triqui Arcade")
    parser.add_argument(
        "--rival", choices=sorted(RIVALS), default="zorro",
        help="rival de IA (por defecto: zorro)",
    )
    parser.add_argument(
        "--dos-jugadores", action="store_true",
        help="juegan dos personas en el mismo equipo",
    )
    args = parser.parse_args()
    play_game(None if args.dos_jugadores else args.rival)
