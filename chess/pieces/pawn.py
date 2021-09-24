from .base import Piece, Color
import numpy as np

class Pawn(Piece):

    def __init__(self, color, *args, **kwargs):
        """Initialise bishop, sets color of piece."""
        # Initialise bishop with correct symbol
        super().__init__(
            color,
            symbol = "♙",
            *args,
            **kwargs,
        )

    ########################################################################
    #                                Moves                                 #
    ########################################################################

    def moves(self, rank, file, *args, **kwargs):
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
        # Initialise result
        result = np.zeros((self.n_files, self.n_ranks), dtype=bool)

        # Set moves for white
        if self.color == Color.WHITE:
            result[rank-1, file-1:file+2] = True
            if rank >= self.n_ranks-2:
                result[rank-2:rank, file] = True

        # Set moves for black
        else:
            result[rank+1, file-1:file+2] = True
            if rank <= 1:
                result[rank+1:rank+3, file] = True

        # Return result
        return result
