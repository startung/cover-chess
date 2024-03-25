import chess

def evaluate_board(fen: str, color: chess.Color) -> float:
    board = chess.Board(fen)
    return sum([piece.color == color for piece in board.piece_map().values()]) - sum([piece.color != color for piece in board.piece_map().values()])