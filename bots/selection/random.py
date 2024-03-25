import chess
import random

from bots import ChessBotClass


class RandomSelection(ChessBotClass):
    def __str__(self) -> str:
        return "Random"

    def __call__(self, board_fen) -> tuple[chess.Move, float]:
        board = chess.Board(board_fen)
        moves = list(board.legal_moves)
        idx = int(random.random() * len(moves))
        move = moves[idx]
        return move, 0
