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

    def moves(self, rank, file, mask_black=None, mask_white=None, *args, **kwargs):
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
        # Initialise result
        result = np.zeros((self.n_files, self.n_ranks), dtype=bool)

        # Set black side -> white side diagonal as possible moves
        result = np.logical_or(result, np.diag(self.capture_mask(
            index = min(rank, file),
            black = np.diag(mask_black, file-rank),
            white = np.diag(mask_white, file-rank),
        ), file-rank))

        # Set white side -> black side diagonal as possible moves
        result = np.logical_or(result, np.flip(np.diag(self.capture_mask(
            index = min(rank, self.n_files - file - 1),
            black = np.diag(np.flip(mask_black, axis=1), self.n_ranks-1 - rank - file),
            white = np.diag(np.flip(mask_white, axis=1), self.n_ranks-1 - rank - file),
        ), self.n_ranks-1 - rank - file), axis=1))

        # Remove own rank and file as moves
        result[rank, file] = False

        # Return result
        return result
