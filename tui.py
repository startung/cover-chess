import chess


def draw(fen: str, rating: int) -> None:
    board = chess.Board(fen)
    print(board.unicode(empty_square="·", invert_color=True))
    print(f"Rating: {rating}")


if __name__ == "__main__":

    board = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    draw(board, 0)
