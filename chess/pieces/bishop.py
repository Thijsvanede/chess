from .base import Piece, PieceRepresentation
import numpy as np

class Bishop(Piece):

    def __init__(self, color, *args, **kwargs):
        """Initialise bishop, sets color of piece."""
        # Initialise bishop with correct symbol
        super().__init__(
            color,
            symbol = PieceRepresentation.BISHOP,
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

        # Set diagonals as possible moves
        diagonal_lr = np.eye(self.n_files, self.n_ranks, file-rank, dtype=bool)
        diagonal_rl = np.flip(np.eye(
            self.n_files,
            self.n_ranks,
            self.n_ranks-1 - rank - file,
            dtype=bool
        ), axis=1)
        result = np.logical_or(result, diagonal_lr)
        result = np.logical_or(result, diagonal_rl)

        # Remove own rank and file as moves
        result[rank, file] = False

        # Return result
        return result
