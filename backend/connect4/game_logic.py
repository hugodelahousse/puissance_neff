from enum import IntEnum
from typing import Tuple, List, Optional


class BoardState(IntEnum):
    EMPTY = 0
    YELLOW = 1
    RED = 2


class BoardPlayer(IntEnum):
    YELLOW = BoardState.YELLOW
    RED = BoardState.RED


class Board:
    WIDTH = 7
    HEIGHT = 6
    WIN_COUNT = 4

    def __init__(self):
        self.board: List[BoardState] = [
            BoardState.EMPTY for _ in range(Board.HEIGHT * Board.WIDTH)
        ]

    @staticmethod
    def line_column_to_index(row: int, column: int):
        return row * Board.HEIGHT + column

    def get_position(self, row: int, column: int):
        return self.board[self.line_column_to_index(row, column)]

    def set_position(self, row: int, column: int, color: BoardState):
        self.board[self.line_column_to_index(row, column)] = color

    def column_full(self, column: int):
        return self.get_position(Board.HEIGHT - 1, column) != BoardState.EMPTY

    @classmethod
    def valid_column(cls, column: int):
        return 0 <= column < cls.WIDTH

    @classmethod
    def valid_row(cls, row: int):
        return 0 <= row < cls.HEIGHT

    def play(
        self, column: int, color: BoardPlayer
    ) -> Tuple[Optional[Tuple[int, int]], bool]:
        """
        :return: A tuple with the position played, and whether or not the move was a win
        """
        for row in range(Board.HEIGHT):
            if self.get_position(row, column) == BoardState.EMPTY:
                self.set_position(row, column, BoardState[color.value])
                return (row, column), self.check_win(row, column)

        return None, False

    def check_win_rec(
        self,
        row: int,
        column: int,
        delta_row: int,
        delta_column: int,
        color: BoardState,
    ) -> int:
        column += delta_column
        delta_row += delta_row
        if (
            not self.valid_column(column)
            or not self.valid_row(row)
            or self.get_position(row, column) != color
        ):
            return 0

        return 1 + self.check_win_rec(row, column, delta_row, delta_column, color)

    def check_win(self, row: int, column: int) -> bool:
        color = self.get_position(row, column)
        if color == BoardState.EMPTY:
            return False

        deltas = [(1, 0), (0, 1), (1, 1), (1, -1)]

        for delta_row, delta_column in deltas:
            if (
                1
                + self.check_win_rec(row, column, delta_row, delta_column, color)
                + self.check_win_rec(row, column, -delta_row, -delta_column, color)
            ):
                return True

        return False

    def to_list(self) -> List[List[BoardState]]:
        return [
            [self.get_position(row, column) for column in range(self.WIDTH)]
            for row in range(self.HEIGHT)
        ]
