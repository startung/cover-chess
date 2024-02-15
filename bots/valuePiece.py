import chess

from bots import MiniMaxBot

class ValuePieceBot(MiniMaxBot):
    def __init__(self,
            max_depth: int
        ) -> None:
        super().__init__(max_depth)
        self.piece_values = {chess.PAWN : 1, chess.ROOK : 5, chess.KNIGHT : 3, chess.BISHOP : 3, chess.KING : 100, chess.QUEEN : 9}

    def __str__(self) -> str:
        return f"Value Piece({self._max_depth})"

    def evaluate_board(self, board: chess.Board, color: chess.Color) -> float:
        return sum([self.piece_values[piece.piece_type] for piece in board.piece_map().values() if piece.color == color])