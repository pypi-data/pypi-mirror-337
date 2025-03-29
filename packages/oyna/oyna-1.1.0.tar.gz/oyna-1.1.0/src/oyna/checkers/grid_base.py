import platform
import sys
from enum import Enum
from typing import Literal, Optional


class Emoji(Enum):
    EMPTY = "🔹"
    PLAYER = "🔴"
    COMPUTER = "⚫️"


def getch() -> str:
    if platform.system() == "Windows":
        import msvcrt

        return str(msvcrt.getch().decode("utf-8")).lower()  # type: ignore
    else:
        import termios
        import tty

        fd = sys.stdin.fileno()
        oldsettings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, oldsettings)
        return ch


class Board:
    def __init__(self, size: int = 8) -> None:
        self.size = size
        self.cells: list[list[Emoji]] = self._cells()
        self.location = self.size // 2, self.size // 2
        self.selected_piece: Optional[tuple[int, int]] = None
        self.initialize()

    def initialize(self) -> None:
        for i in range(3):
            for j in range(self.size):
                if (i + j) % 2 == 1:
                    self.cells[i][j] = Emoji.COMPUTER
                if (self.size - i - 1 + j) % 2 == 1:
                    self.cells[self.size - i - 1][j] = Emoji.PLAYER

    def _cells(self) -> list[list[Emoji]]:
        return [[Emoji.EMPTY for _ in range(self.size)] for _ in range(self.size)]

    def get_valid_moves_for_piece(
        self, row: int, col: int, player: Literal[Emoji.PLAYER, Emoji.COMPUTER]
    ) -> list[tuple[int, int]]:
        """Get valid moves for a specific piece, disallowing backward moves."""
        valid_moves = []
        opponent = Emoji.COMPUTER if player == Emoji.PLAYER else Emoji.PLAYER
        directions = (
            [(-1, -1), (-1, 1)] if player == Emoji.PLAYER else [(1, -1), (1, 1)]
        )

        for dr, dc in directions:
            r, c = row + dr, col + dc
            if (
                0 <= r < self.size
                and 0 <= c < self.size
                and self.cells[r][c] == Emoji.EMPTY
            ):
                valid_moves.append((r, c))
            elif (
                0 <= r < self.size
                and 0 <= c < self.size
                and self.cells[r][c] == opponent
            ):
                r += dr
                c += dc
                if (
                    0 <= r < self.size
                    and 0 <= c < self.size
                    and self.cells[r][c] == Emoji.EMPTY
                ):
                    valid_moves.append((r, c))

        return valid_moves

    def print_board(self, highlight_moves: list[tuple[int, int]] | None = None) -> None:
        board_str = ""
        highlight_moves = highlight_moves or []
        for i in range(self.size):
            for j in range(self.size):
                if self.location == (i, j):
                    board_str += f"\033[48;2;50;100;200m{self.cells[i][j].value}\033[0m"
                elif (i, j) in highlight_moves:
                    board_str += (
                        f"\033[48;2;100;200;100m{self.cells[i][j].value}\033[0m"
                    )
                else:
                    board_str += self.cells[i][j].value
            board_str += "\n"
        print(f"\033[H\033[J{board_str}")

    def make_move(
        self,
        start: tuple[int, int],
        end: tuple[int, int],
        player: Literal[Emoji.PLAYER, Emoji.COMPUTER],
    ) -> None:
        self.cells[start[0]][start[1]] = Emoji.EMPTY
        self.cells[end[0]][end[1]] = player
        dr, dc = end[0] - start[0], end[1] - start[1]
        if abs(dr) == 2 and abs(dc) == 2:
            self.cells[start[0] + dr // 2][start[1] + dc // 2] = Emoji.EMPTY

    def computer_move(self) -> None:
        best_move = None
        for r in range(self.size):
            for c in range(self.size):
                if self.cells[r][c] == Emoji.COMPUTER:
                    valid_moves = self.get_valid_moves_for_piece(r, c, Emoji.COMPUTER)
                    for move in valid_moves:
                        dr, dc = move[0] - r, move[1] - c
                        if abs(dr) == 2 and abs(dc) == 2:
                            best_move = ((r, c), move)
                            break
                    if best_move:
                        break
        if not best_move:
            for r in range(self.size):
                for c in range(self.size):
                    if self.cells[r][c] == Emoji.COMPUTER:
                        valid_moves = self.get_valid_moves_for_piece(
                            r, c, Emoji.COMPUTER
                        )
                        if valid_moves:
                            best_move = ((r, c), valid_moves[0])
                            break
                if best_move:
                    break
        if best_move:
            self.make_move(best_move[0], best_move[1], Emoji.COMPUTER)

    def action(self, char: str) -> None:
        move = (0, 0)
        match char:
            case "a":
                move = (0, -1)
            case "d":
                move = (0, 1)
            case "w":
                move = (-1, 0)
            case "s":
                move = (1, 0)
            case " ":
                exit()
            case "e":
                if self.selected_piece:
                    valid_moves = self.get_valid_moves_for_piece(
                        self.selected_piece[0], self.selected_piece[1], Emoji.PLAYER
                    )
                    if self.location in valid_moves:
                        self.make_move(self.selected_piece, self.location, Emoji.PLAYER)
                        self.selected_piece = None
                        self.computer_move()
                    else:
                        self.selected_piece = None
                elif self.cells[self.location[0]][self.location[1]] == Emoji.PLAYER:
                    self.selected_piece = self.location
                return
        new_location = self.location[0] + move[0], self.location[1] + move[1]
        if 0 <= new_location[0] < self.size and 0 <= new_location[1] < self.size:
            self.location = new_location


def run() -> None:
    board = Board()
    while True:
        board.print_board(
            (
                board.get_valid_moves_for_piece(
                    board.selected_piece[0], board.selected_piece[1], Emoji.PLAYER
                )
                if board.selected_piece
                else None
            )
        )
        board.action(getch())


if __name__ == "__main__":
    run()
