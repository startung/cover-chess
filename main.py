import tui
import chess
from bots.evaluation.numberPiece import evaluate_board as numberPiece
from bots.evaluation.valuePiece import evaluate_board as valuePiece
from bots.selection.random import RandomSelection


def main():
    board = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    rating = valuePiece(board, chess.WHITE)
    tui.draw(board, rating)

    selection = RandomSelection()
    move, _ = selection(board)
    print(move)


if __name__ == "__main__":
    main()
