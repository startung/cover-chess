import chess

piece_values = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0,
}


def evaluate_board(fen: str, color: chess.Color) -> float:
    board = chess.Board(fen)
    return sum(
        [
            piece_values[piece.piece_type]
            for piece in board.piece_map().values()
            if piece.color == color
        ]
    ) - sum(
        [
            piece_values[piece.piece_type]
            for piece in board.piece_map().values()
            if piece.color != color
        ]
    )
