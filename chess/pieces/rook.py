from .base import Piece, PieceRepresentation
import numpy as np

class Rook(Piece):

    def __init__(self, color, *args, **kwargs):
        """Initialise bishop, sets color of piece."""
        # Initialise bishop with correct symbol
        super().__init__(
            color,
            symbol = PieceRepresentation.ROOK,
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

        # Set file as possible moves
        result[rank, :] = self.capture_mask(
            index = file,
            black = mask_black[rank, :],
            white = mask_white[rank, :],
        )

        # Set rank as possible moves
        result[:, file] = self.capture_mask(
            index = rank,
            black = mask_black[:, file],
            white = mask_white[:, file],
        )

        # Remove own rank and file as moves
        result[rank, file] = False

        # Return result
        return result
