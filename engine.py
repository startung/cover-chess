import chess
import curses
import sys

from itertools import count
from bots.random import RandomBot
from bots.numberPiece import NumberPieceBot
from bots.valuePiece import ValuePieceBot
import time

VISUALIZE = "-v" in sys.argv
DEFAULT_PIECE_VALUES = {chess.PAWN : 1, chess.ROOK : 5, chess.KNIGHT : 3, chess.BISHOP : 3, chess.KING : 100, chess.QUEEN : 9}
MIN_MOVE_TIME = 0.5


def board_draw(board):
    piece_map = {
        'P': '♟',
        'R': '♜',
        'N': '♞',
        'B': '♝',
        'Q': '♛',
        'K': '♚',
        'p': '♙',
        'r': '♖',
        'n': '♘',
        'b': '♗',
        'q': '♕',
        'k': '♔',
        '.': ' '
    }
    board_str = str(board)
    for letter, piece in piece_map.items():
        board_str = board_str.replace(letter, piece)
    return board_str

def board_setup(board):
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    stdscr.clear()
    stdscr.refresh()
    stdscr.addstr(1, 0, board_draw(str(board)))
    stdscr.refresh()
    return stdscr

def board_move(stdscr, board, i):
    curr_board = board_draw(str(board).replace(' ', '').replace('\n', ''))
    stdscr.addstr(0, 0, "Move " + str(i))
    for y in range(0, 8):
        for x in range(0, 8):
            if (x+y) % 2 == 0:
                stdscr.addch(y+1,3*x, ' ', curses.A_REVERSE)
                stdscr.addch(y+1,3*x+1, curr_board[y*8 + x], curses.A_REVERSE)
                stdscr.addch(y+1,3*x+2, ' ', curses.A_REVERSE)
            else:
                stdscr.addch(y+1,3*x, ' ')
                stdscr.addch(y+1,3*x+1, curr_board[y*8 + x])
                stdscr.addch(y+1,3*x+2, ' ')
    stdscr.addstr(9, 0, "White score: " + str(score_board(board, chess.WHITE)))
    stdscr.addstr(10, 0, "Black score: " + str(score_board(board, chess.BLACK)))
    stdscr.refresh()
    time.sleep(MIN_MOVE_TIME) # slow down the bots so that we can see them

def board_close(stdscr):
    stdscr.keypad(False)
    curses.echo()
    curses.nocbreak()
    curses.endwin()

def score_board(board, color):
    return sum([DEFAULT_PIECE_VALUES[piece.piece_type] for piece in board.piece_map().values() if piece.color == color])

class Judge():
    def __init__(self, player_1, player_2, time_limit=300):
        self.player_1 = player_1
        self.player_2 = player_2
        self.time_limit = time_limit

    def run_game(self, initial_board_fen:str = None):
        board = chess.Board()

        if VISUALIZE:
            stdscr = board_setup(board)

        player_times = [0, 0]

        for i in count(0, 1):
            if board.is_checkmate():
                if VISUALIZE:
                    board_close(stdscr)
                    print(board_draw(str(board)))
                print("GAME OVER")
                print("Winner is bot", i%2 + 1, sep="_")
                break
            if i > 100:
                if VISUALIZE:
                    board_close(stdscr)
                    print(board_draw(str(board)))
                print("GAME OVER")
                print("Exceeded move limits, it's a tie")
                break

            board_fen = board.fen()

            start = time.time()
            if i % 2 == 0:
                move = self.player_1(board_fen)
            else:
                move = self.player_2(board_fen)
            end = time.time()

            player_times[i%2] += end - start

            if player_times[i%2] > self.time_limit:
                board_close(stdscr)
                print("GAME OVER")
                print("Time limit exceeded, winner is bot", i%2+1, sep="_")

            if not board.is_legal(move):
                raise ValueError("Illegal board move. The bot it hallucinating...")

            board.push(move)
            if VISUALIZE:
                board_move(stdscr, board, i)
            else:
                print(f"\rMove {i+1}: White({self.player_1}): {score_board(board, chess.WHITE)} Black({self.player_2}): {score_board(board, chess.BLACK)}", end="")

        print("Times used:", player_times)

class JudgeNoteBook():
    from IPython.display import clear_output
    def __init__(self, player_1, player_2, time_limit=300):
        self.player_1 = player_1
        self.player_2 = player_2
        self.time_limit = time_limit

    def run_game(self, initial_board_fen:str = None):
        board = chess.Board()

        player_times = [0, 0]

        for i in count(0, 1):
            if board.is_checkmate():
                print("GAME OVER")
                print("Winner is bot", i%2 + 1, sep="_")
                break
            if i > 100:
                print("GAME OVER")
                print("Exceeded move limits, it's a tie")
                break

            board_fen = board.fen()

            start = time.time()
            if i % 2 == 0:
                move = self.player_1(board_fen)
            else:
                move = self.player_2(board_fen)
            end = time.time()

            player_times[i%2] += end - start

            if player_times[i%2] > self.time_limit:
                print("GAME OVER")
                print("Time limit exceeded, winner is bot", i%2+1, sep="_")

            if not board.is_legal(move):
                raise ValueError("Illegal board move. The bot it hallucinating...")

            board.push(move)

            clear_output(wait=True)
            display(board)

            # slow down the bots so that we can see them
            time.sleep(.25)
        print("Times used:", player_times)

if __name__ == "__main__":
    # initialize the bots
    bot_1 = ValuePieceBot(3)
    bot_2 = NumberPieceBot(3)

    # run tournament
    judge = Judge(bot_1, bot_2)
    judge.run_game()