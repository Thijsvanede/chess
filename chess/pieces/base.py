from enum import Enum
import numpy as np

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


    def moves(self, rank, file, mask_black=None, mask_white=None):
        """Return the possible moves for a piece on a given rank and file.

            Parameters
            ----------
            rank : int
                Rank of piece.

            file : int
                File of piece.

            mask_black : np.array of shape=(n_ranks, n_files), optional
                Optional mask indicating location of black pieces on board.

            mask_white : np.array of shape=(n_ranks, n_files), optional
                Optional mask indicating location of white pieces on board.

            Returns
            -------
            moves : np.array of shape=(n_ranks, n_files)
                Mask of available moves on board.
            """
        raise NotImplementedError("Moves should be implemented by subclasses.")

    ########################################################################
    #                       Auxiliary move functions                       #
    ########################################################################

    def capture_mask(self, index, black, white):
        # Perform check
        assert black.shape == white.shape, "Black and white should be of same shape."

        # Initialise result
        result = np.zeros(black.shape, dtype=bool)

        # Initialise same and different color masks
        same      = white if self.color == Color.WHITE else black
        different = black if self.color == Color.WHITE else white

        # Fill result
        for i in range(index+1, black.shape[0]):
            if same[i]:
                break
            elif different[i]:
                result[i] = True
                break
            else:
                result[i] = True

        for i in range(index-1, -1, -1):
            if same[i]:
                break
            elif different[i]:
                result[i] = True
                break
            else:
                result[i] = True

        # Return result
        return result

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
