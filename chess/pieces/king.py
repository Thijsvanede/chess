from .base import Color, Piece
import numpy as np

class King(Piece):

    def __init__(self, color, *args, **kwargs):
        """Initialise bishop, sets color of piece."""
        # Initialise bishop with correct symbol
        super().__init__(
            color,
            symbol = "♔",
            *args,
            **kwargs,
        )

    ########################################################################
    #                                Moves                                 #
    ########################################################################

    def moves(self, rank, file, castling=set(), *args, **kwargs):
        """Return the possible moves for a piece on a given rank and file.

            Parameters
            ----------
            rank : int
                Rank of piece.

            file : int
                File of piece.

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

        print(rank == self.n_ranks-1 and file == 4)

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

        # Remove own rank and file as moves
        result[rank, file] = False

        # Return result
        return result
