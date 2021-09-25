import numpy as np
import pieces

class Board(object):

    def __init__(self, n_ranks=8, n_files=8):
        """"""
        self.n_files   = n_files
        self.n_ranks   = n_ranks
        self.board     = np.zeros((n_ranks, n_files), dtype=object)
        self.color     = 'w'
        self.castling = 'KQkq'

    ########################################################################
    #                              Get moves                               #
    ########################################################################

    def moves(self, rank, file):
        """"""
        if self.board[rank, file] is None:
            # Return no moves
            return np.zeros((self.n_ranks, self.n_files), dtype=bool)
        else:
            # Return moves for piece
            return self.board[rank, file].moves(
                rank = rank,
                file = file,
                castling = self.castling,
            )

    ########################################################################
    #                             Piece masks                              #
    ########################################################################

    def piece_mask(self, color=None):
        """Returns mask of board where pieces are of given color.

            Parameters
            ----------
            color : Color, optional
                Color for which to return mask. If None is given, return mask
                for both BLACK and WHITE.

            Returns
            -------
            mask : np.array of shape=(n_ranks, n_files)
                Boolean mask that is True if a cell contains a piece of given
                color.
            """
        # Get mask for specific colors
        if color is not None:
            return np.vectorize(
                lambda x: x is not None and
                x.color == color
            )(self.board)

        # Get mask for both BLACK and WHITE
        else:
            return np.logical_or(
                self.piece_mask(pieces.Color.WHITE),
                self.piece_mask(pieces.Color.BLACK),
            )

    ########################################################################
    #                             I/O methods                              #
    ########################################################################

    @classmethod
    def from_fen(cls, fen):
        """"""
        # Parse FEN
        position, color, castling, en_passant, halfmove, fullmove = fen.split()

        # Parse position
        setup = list()
        # Loop over all ranks in FEN
        for rank in position.split('/'):
            # Start new rank
            setup.append(list())

            # Loop over each individual piece
            for piece in rank:
                # Get color from piece
                if piece.islower():
                    color = pieces.Color.BLACK
                else:
                    color = pieces.Color.WHITE

                # Set specific piece
                if piece.lower() == 'p':
                    setup[-1].append(pieces.Pawn(color))
                elif piece.lower() == 'n':
                    setup[-1].append(pieces.Knight(color))
                elif piece.lower() == 'b':
                    setup[-1].append(pieces.Bishop(color))
                elif piece.lower() == 'r':
                    setup[-1].append(pieces.Rook(color))
                elif piece.lower() == 'q':
                    setup[-1].append(pieces.Queen(color))
                elif piece.lower() == 'k':
                    setup[-1].append(pieces.King(color))
                else:
                    for _ in range(int(piece)):
                        setup[-1].append(None)

        # Setup board as numpy array
        setup = np.asarray(setup, dtype=object)

        # Ensure we have 2 dimensions
        assert setup.ndim == 2, "FEN notation differed per rank."

        # Create board
        board = cls(
            n_files = setup.shape[0],
            n_ranks = setup.shape[1],
        )

        # Setup board
        board.board      = setup
        board.color      = color
        board.castling   = castling
        board.en_passant = None if en_passant == '-' else en_passant
        board.halfmove   = int(halfmove)
        board.fullmove   = int(fullmove)

        # Return result
        return board



################################################################################
#                                String method                                 #
################################################################################

    def __str__(self):
        """"""
        # Setup board top
        result  = "╔" + "═══╤"*(self.n_files-1) + "═══╗\n"

        # Setup board rows
        for index_rank, row in enumerate(self.board):
            result += "║"

            for index_file, square in enumerate(row):
                result += "{:^3}".format(str(square) if square else ' ')

                if index_file == self.n_files-1 and index_rank != self.n_ranks-1:
                    result += "║\n╟" + "───┼"*(self.n_files-1) + "───╢\n"
                elif index_file == self.n_files-1 and index_rank == self.n_ranks-1:
                    # Setup board bottom
                    result += "║\n╚" + "═══╧"*(self.n_files-1) + "═══╝"
                else:
                    result += '│'

        # Return result
        return result

if __name__ == "__main__":

    board = Board.from_fen("rnbqkbnr/pppppppp/8/7Q/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    print(board)

    print(board.moves(7, 1))
