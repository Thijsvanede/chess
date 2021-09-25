from .base import Piece, PieceRepresentation
import numpy as np

class Knight(Piece):

    def __init__(self, color, *args, **kwargs):
        """Initialise bishop, sets color of piece."""
        # Initialise bishop with correct symbol
        super().__init__(
            color,
            symbol = PieceRepresentation.KNIGHT,
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

        # Set squares surrounding knight to True
        result[
            max(0, rank-2) : rank+3,
            max(0, file-2) : file+3,
        ] = True

        # Remove "queen" moves
        # Set complete file and rank as possible moves
        result[rank, :] = False
        result[:, file] = False

        # Set diagonals as possible moves
        diagonal_lr = ~np.eye(self.n_files, self.n_ranks, file-rank, dtype=bool)
        diagonal_rl = np.flip(~np.eye(
            self.n_files,
            self.n_ranks,
            self.n_ranks-1 - rank - file,
            dtype=bool
        ), axis=1)
        result = np.logical_and(result, diagonal_lr)
        result = np.logical_and(result, diagonal_rl)

        # Return result
        return result
