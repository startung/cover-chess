from time import sleep
import chess.pgn

with open("pgn/Kasparov.pgn") as pgn:
    # while line := pgn.readline():
    #     print(line)
    while game := chess.pgn.read_game(pgn):
        event = game.headers["Event"]
        if event == "AGS Computer Challenge":
            print(f"{event}, {game.headers['White']} vs {game.headers['Black']}")
            # board = game.board()
            # for move in game.mainline_moves():
            #     board.push(move)
            #     print(board.unicode(empty_square="·", invert_color=True), end="\n\n")
            #     sleep(1)

    offset = pgn.tell()
    ags_offsets = []
    while headers := chess.pgn.read_headers(pgn):
        if headers["Event"] == "AGS Computer Challenge":
            ags_offsets.append(pgn.tell())
        offset = pgn.tell()

    for offset in ags_offsets:
        pgn.seek(offset)
        game = chess.pgn.read_game(pgn)
        print(f"{game.headers['White']} vs {game.headers['Black']}")
