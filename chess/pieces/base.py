from enum import Enum

class Color(Enum):
    WHITE = 'w'
    BLACK = 'b'

class PieceRepresentation(Enum):
    # Regular piece representations
    BISHOP = 'B'
    KING   = 'K'
    KNIGHT = 'N'
    PAWN   = 'P'
    QUEEN  = 'Q'
    ROOK   = 'R'

    # Fancy printable characters
    UNICODE_BISHOP = '♗'
    UNICODE_KING   = '♔'
    UNICODE_KNIGHT = '♘'
    UNICODE_PAWN   = '♙'
    UNICODE_QUEEN  = '♕'
    UNICODE_ROOK   = '♖'

class Piece(object):

    def __init__(self, color, symbol, n_files=8, n_ranks=8):
        """Initialise chess piece, sets color of piece."""
        # Check if color is corredt
        assert color in Color, "Color should be Color.BLACK or Color.WHITE"

        # Set piece color
        self.color  = color
        self.symbol = symbol

        # Set files and ranks
        self.n_files = n_files
        self.n_ranks = n_ranks


    def moves(self, rank, file):
        """Return the possible moves for a piece on a given rank and file.

            Parameters
            ----------
            rank : int
                Rank of piece.

            file : int
                File of piece.

            Returns
            -------
            moves : np.array of shape=(n_ranks, n_files)
                Mask of available moves on board.
            """
        raise NotImplementedError("Moves should be implemented by subclasses.")

    ########################################################################
    #                            String method                             #
    ########################################################################

    def __str__(self):
        """Return string representation of piece"""
        # Return regular symbol
        if self.color == Color.BLACK:
            return self.symbol.value.lower()

            # return self.symbol

        # Cast to black version of symbol
        else:
            return self.symbol.value.upper()
            # bytes   = self.symbol.encode('utf-8')
            # number  = int.from_bytes(bytes, byteorder='big')
            # number += 6 # Cast to black version of piece
            # bytes   = number.to_bytes(3, byteorder='big')
            # return bytes.decode('utf-8')
