from gui import GUI

import sys
sys.path.insert(0, '..')
from board import Board

if __name__ == "__main__":
    # Create new GUI
    gui = GUI(
        board = Board.from_fen("rnbqkbnr/pppppppp/8/6Q1/8/4n1p1/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    )

    # Run GUI
    gui.run()
