"""Interfaz de consola para jugar contra la IA o contra otra persona."""

from __future__ import annotations

import argparse

from .ai import RIVALS
from .board import MODES, X, Board


def ask_move(board: Board) -> int:
    legal = board.legal_moves()
    last = board.size ** 2
    while True:
        raw = input(f"Turno de {board.turn}. Casilla (1-{last}): ").strip()
        if raw.isdigit() and int(raw) - 1 in legal:
            return int(raw) - 1
        print("Jugada inválida, intenta de nuevo.")


def play_game(rival: str | None, mode: str = "clasico") -> None:
    board = Board.from_mode(mode)
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
    parser.add_argument(
        "--modo", choices=sorted(MODES), default="clasico",
        help="clasico (3x3), gran5 (5x5, 4 en línea) o gran7 (7x7, 5 en línea); solo consola",
    )
    parser.add_argument(
        "--consola", action="store_true",
        help="jugar en la consola en lugar de la ventana gráfica",
    )
    args = parser.parse_args()
    if not args.consola:
        from .gui import main as gui_main
        gui_main()
        return
    play_game(None if args.dos_jugadores else args.rival, args.modo)
