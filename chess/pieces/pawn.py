from .base import Piece, Color, PieceRepresentation
import numpy as np

class Pawn(Piece):

    def __init__(self, color, *args, **kwargs):
        """Initialise bishop, sets color of piece."""
        # Initialise bishop with correct symbol
        super().__init__(
            color,
            symbol = PieceRepresentation.PAWN,
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

        # Get mask of other pieces
        other_pieces = np.zeros((self.n_files, self.n_ranks), dtype=bool)
        if mask_black is not None:
            other_pieces = np.logical_or(other_pieces, mask_black)
        if mask_white is not None:
            other_pieces = np.logical_or(other_pieces, mask_white)

        # Set moves for white
        if self.color == Color.WHITE:
            # Check if blocked
            if not other_pieces[rank-1, file]:
                # Add regular move
                result[rank-1, file] = True

                # Add double move
                if rank >= self.n_ranks-2 and not other_pieces[rank-2, file]:
                    result[rank-2, file] = True

            # Add capture moves
            if mask_black is not None:
                if file > 0 and mask_black[rank-1, file-1]:
                    result[rank-1, file-1] = True
                if file < self.n_files-1 and mask_black[rank-1, file+1]:
                    result[rank-1, file+1] = True

        # Set moves for black
        else:
            # Check if blocked
            if not other_pieces[rank+1, file]:
                # Add regular move
                result[rank+1, file] = True

                # Add double move
                if rank <= 1 and not other_pieces[rank+2, file]:
                    result[rank+2, file] = True

            # Add capture moves
            if mask_white is not None:
                if file > 0 and mask_white[rank+1, file-1]:
                    result[rank+1, file-1] = True
                if file < self.n_files-1 and mask_white[rank+1, file+1]:
                    result[rank+1, file+1] = True

        # Return result
        return result
