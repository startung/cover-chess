import chess

from bots import MiniMaxBot

class NumberPieceBot(MiniMaxBot):
    def __str__(self) -> str:
        return f"Number Piece({self._max_depth})"

    def evaluate_board(self, board: chess.Board, color: chess.Color) -> float:
        return sum([piece.color == color for piece in board.piece_map().values()])