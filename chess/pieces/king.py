from .base import Color, Piece, PieceRepresentation
import numpy as np

class King(Piece):

    def __init__(self, color, *args, **kwargs):
        """Initialise bishop, sets color of piece."""
        # Initialise bishop with correct symbol
        super().__init__(
            color,
            symbol = PieceRepresentation.KING,
            *args,
            **kwargs,
        )

    ########################################################################
    #                                Moves                                 #
    ########################################################################

    def moves(self, rank, file, mask_black=None, mask_white=None, castling=set(), *args, **kwargs):
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

            castling : iterable, default=set()
                Add relevant castling moves. Can contain KQkq.

            Returns
            -------
            moves : np.array of shape=(n_ranks, n_files)
                Mask of available moves on board.
            """
        # Initialise result
        result = np.zeros((self.n_files, self.n_ranks), dtype=bool)

        # Set squares surrounding king to True
        result[
            max(0, rank-1) : rank+2,
            max(0, file-1) : file+2,
        ] = True

        # Add castling moves
        if 'K' in castling and self.color == Color.WHITE:
            assert rank == self.n_ranks-1 and file == 4, "Cannot castle, king has moved!"
            result[rank, file+2] = True
        if 'Q' in castling and self.color == Color.WHITE:
            assert rank == self.n_ranks-1 and file == 4, "Cannot castle, king has moved!"
            result[rank, file-2] = True
        if 'k' in castling and self.color == Color.BLACK:
            assert rank == 0 and file == 4, "Cannot castle, king has moved!"
            result[rank, file+2] = True
        if 'q' in castling and self.color == Color.BLACK:
            assert rank == 0 and file == 4, "Cannot castle, king has moved!"
            result[rank, file-2] = True

        # Ensure king does not capture own pieces
        if mask_white is not None and self.color == Color.WHITE:
            result = np.logical_and(result, ~mask_white)
        if mask_black is not None and self.color == Color.BLACK:
            result = np.logical_and(result, ~mask_black)

        # Remove own rank and file as moves
        result[rank, file] = False

        # Return result
        return result
