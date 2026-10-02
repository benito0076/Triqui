"""Interfaz gráfica (tkinter): tablero clickeable, rivales de IA y marcador."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from .ai import RIVALS
from .board import O, X, Board

CELL = 120
PAD = 20
SIZE = CELL * 3 + PAD * 2
BG = "#1e1e2e"
GRID = "#585b70"
X_COLOR = "#f38ba8"
O_COLOR = "#89b4fa"
WIN_COLOR = "#a6e3a1"
AI_DELAY_MS = 450

TWO_PLAYERS = "2 jugadores"


class TriquiApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        root.title("Triqui Arcade")
        root.configure(bg=BG)
        root.resizable(False, False)

        self.board = Board()
        self.scores = {"Tú": 0, "IA": 0, "Empates": 0}
        self.pending_ai: str | None = None

        self.mode = tk.StringVar(value="zorro")
        self.symbol = tk.StringVar(value=X)
        self.status = tk.StringVar()
        self.score_text = tk.StringVar()

        self._build_controls()
        self.canvas = tk.Canvas(
            root, width=SIZE, height=SIZE, bg=BG, highlightthickness=0
        )
        self.canvas.pack(padx=10)
        self.canvas.bind("<Button-1>", self.on_click)
        tk.Label(root, textvariable=self.status, bg=BG, fg="white",
                 font=("Segoe UI", 14, "bold")).pack(pady=(6, 0))
        tk.Label(root, textvariable=self.score_text, bg=BG, fg=GRID,
                 font=("Segoe UI", 10)).pack(pady=(0, 10))

        self.new_game()

    # --- controles -------------------------------------------------------
    def _build_controls(self) -> None:
        bar = tk.Frame(self.root, bg=BG)
        bar.pack(pady=10)
        tk.Label(bar, text="Rival:", bg=BG, fg="white").pack(side="left")
        box = ttk.Combobox(
            bar, textvariable=self.mode, state="readonly", width=11,
            values=[*sorted(RIVALS), TWO_PLAYERS],
        )
        box.pack(side="left", padx=(4, 10))
        box.bind("<<ComboboxSelected>>", lambda _e: self.new_game())
        tk.Label(bar, text="Juego con:", bg=BG, fg="white").pack(side="left")
        for s in (X, O):
            tk.Radiobutton(
                bar, text=s, value=s, variable=self.symbol, command=self.new_game,
                bg=BG, fg="white", selectcolor=BG, activebackground=BG,
                activeforeground="white",
            ).pack(side="left")
        ttk.Button(bar, text="Nueva partida", command=self.new_game).pack(
            side="left", padx=(10, 0)
        )

    # --- flujo de la partida --------------------------------------------
    @property
    def vs_ai(self) -> bool:
        return self.mode.get() != TWO_PLAYERS

    def new_game(self) -> None:
        if self.pending_ai:
            self.root.after_cancel(self.pending_ai)
            self.pending_ai = None
        self.board = Board()
        self._refresh()
        self._maybe_ai_turn()

    def on_click(self, event: tk.Event) -> None:
        if self.board.is_over() or self.pending_ai or self._ai_to_move():
            return
        col, row = (event.x - PAD) // CELL, (event.y - PAD) // CELL
        if not (0 <= col < 3 and 0 <= row < 3):
            return
        move = row * 3 + col
        if move in self.board.legal_moves():
            self._play(move)

    def _ai_to_move(self) -> bool:
        return self.vs_ai and self.board.turn != self.symbol.get()

    def _maybe_ai_turn(self) -> None:
        if not self.board.is_over() and self._ai_to_move():
            self.pending_ai = self.root.after(AI_DELAY_MS, self._ai_move)

    def _ai_move(self) -> None:
        self.pending_ai = None
        self._play(RIVALS[self.mode.get()](self.board))

    def _play(self, move: int) -> None:
        self.board.play(move)
        if self.board.is_over():
            self._record_result()
        self._refresh()
        self._maybe_ai_turn()

    def _record_result(self) -> None:
        winner = self.board.winner()
        if winner is None:
            self.scores["Empates"] += 1
        elif self.vs_ai:
            self.scores["Tú" if winner == self.symbol.get() else "IA"] += 1

    # --- dibujo ----------------------------------------------------------
    def _refresh(self) -> None:
        self._draw()
        winner = self.board.winner()
        if winner:
            who = "" if not self.vs_ai else (
                " (tú)" if winner == self.symbol.get() else " (IA)")
            self.status.set(f"¡Gana {winner}{who}!")
        elif self.board.is_draw():
            self.status.set("Empate")
        else:
            self.status.set(f"Turno de {self.board.turn}")
        s = self.scores
        self.score_text.set(
            f"Tú {s['Tú']}  ·  IA {s['IA']}  ·  Empates {s['Empates']}"
            if self.vs_ai else f"Empates {s['Empates']}"
        )

    def _center(self, index: int) -> tuple[int, int]:
        r, c = divmod(index, 3)
        return PAD + c * CELL + CELL // 2, PAD + r * CELL + CELL // 2

    def _draw(self) -> None:
        cv = self.canvas
        cv.delete("all")
        for i in (1, 2):
            p = PAD + i * CELL
            cv.create_line(p, PAD + 8, p, SIZE - PAD - 8, fill=GRID, width=4, capstyle="round")
            cv.create_line(PAD + 8, p, SIZE - PAD - 8, p, fill=GRID, width=4, capstyle="round")
        for i, mark in enumerate(self.board.cells):
            cx, cy = self._center(i)
            d = CELL * 0.28
            if mark == X:
                for sx in (1, -1):
                    cv.create_line(cx - d, cy - sx * d, cx + d, cy + sx * d,
                                   fill=X_COLOR, width=10, capstyle="round")
            elif mark == O:
                cv.create_oval(cx - d, cy - d, cx + d, cy + d, outline=O_COLOR, width=10)
        line = self.board.winning_line()
        if line:
            (x1, y1), (x2, y2) = self._center(line[0]), self._center(line[2])
            cv.create_line(x1, y1, x2, y2, fill=WIN_COLOR, width=8, capstyle="round")


def main() -> None:
    root = tk.Tk()
    TriquiApp(root)
    root.mainloop()
