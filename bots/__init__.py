import chess
from abc import ABC, abstractmethod

INF = 1e10

class ChessBotClass(ABC):
    @abstractmethod
    def __call__(self, board_fen: str) -> tuple[chess.Move, float]:
        pass

    def __str__(self) -> str:
        pass

class MiniMaxBot(ChessBotClass):
    def __init__(self, max_depth: int) -> None:
        self._max_depth = max_depth

    def __str__(self) -> str:
        return f"MiniMax({self._max_depth})"

    def evaluate_board(self, board, turn):
        return 0

    def minimax(self, depth: int,
                board: chess.Board,
                alpha: float, beta: float,
                maximizing: bool) -> float:

        if depth == 0 or board.is_game_over():
            return self.evaluatqe_board(board, board.turn) * -1**(not maximizing)
        if maximizing:
            value = -INF
            for move in board.legal_moves:
                board.push(move) #also switches turn
                value = max(value, self.minimax(depth - 1,
                                                board, alpha,
                                                beta, not maximizing))
                board.pop()
                if value > beta:
                    break
                alpha = max(alpha, value)
        else:
            value = INF
            for move in board.legal_moves:
                board.push(move)
                value = min(value, self.minimax(depth - 1,
                                           board, alpha,
                                           beta, not maximizing))
                board.pop()
                if value < alpha:
                    break
                beta = min(beta, value)
        return value

    def __call__(self, board_fen: str) -> tuple[chess.Move, float]:
        board = chess.Board(board_fen)

        best_move = None
        best_eval = -INF
        for move in board.legal_moves:
            board.push(move)
            value = self.minimax(self._max_depth, board, -INF, INF, True)
            if value > best_eval:
                best_eval = value
                best_move = move
            board.pop()
        return best_move, best_eval