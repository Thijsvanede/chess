from gui import GUI

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from board import Board

if __name__ == "__main__":
    # Create new GUI
    gui = GUI(
        board = Board.from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    )

    # Run GUI
    gui.run()
