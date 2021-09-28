import numpy as np
import pieces

class Board(object):

    def __init__(self, n_ranks=8, n_files=8):
        """"""
        self.n_files    = n_files
        self.n_ranks    = n_ranks
        self.board      = np.zeros((n_ranks, n_files), dtype=object)
        self.color      = pieces.Color.WHITE.value
        self.castling   = 'KQkq'
        self.en_passant = '-'
        self.halfmove   = 1
        self.fullmove   = 0

    ########################################################################
    #                              Get square                              #
    ########################################################################

    def square2internal(self, square):
        """Returns internal representation for square."""
        if square == '-':
            return None
        else:
            return self.n_ranks - int(square[1]), ord(square[0].lower()) - ord('a')

    def internal2square(self, rank, file):
        """Returns string representation of square."""
        return chr(file + ord('a')) + str(self.n_ranks - rank)

    ########################################################################
    #                              Get moves                               #
    ########################################################################

    def move(self, src_rank, src_file, dst_rank, dst_file):
        """"""
        # Check if move is allowed
        if self.moves(src_rank, src_file)[dst_rank, dst_file]:

            # Handle en passant rule
            if self.move_en_passant(src_rank, src_file, dst_rank, dst_file):
                # Capture pawn from en passant
                self.board[src_rank, dst_file] = None

            # Handle castling rule
            if self.move_castling(src_rank, src_file, dst_rank, dst_file):
                # Move the relevant rook
                if src_file > dst_file:
                    self.board[src_rank, dst_file+1] = self.board[src_rank, 0]
                    self.board[src_rank, 0         ] = None
                else:
                    self.board[src_rank, dst_file-1    ] = self.board[src_rank, self.n_files-1]
                    self.board[src_rank, self.n_files-1] = None

            # Perform move
            self.board[dst_rank, dst_file] = self.board[src_rank, src_file]
            self.board[src_rank, src_file] = None

            # Update internals after a move was made
            self.move_update()

            # Return successful move
            return True

        # Return unsuccessful move
        return False

    def moves(self, rank, file):
        """"""
        if self.board[rank, file] is None or self.board[rank, file].color.value != self.color:
            # Return no moves
            return np.zeros((self.n_ranks, self.n_files), dtype=bool)
        else:
            # Return moves for piece
            return self.board[rank, file].moves(
                rank       = rank,
                file       = file,
                castling   = self.castling,
                en_passant = self.square2internal(self.en_passant),
                mask_black = self.piece_mask(color=pieces.Color.BLACK),
                mask_white = self.piece_mask(color=pieces.Color.WHITE),
            )

    ########################################################################
    #                       Auxiliary move functions                       #
    ########################################################################

    def move_update(self):
        """Update all internal variables after a successful move."""
        # Flip active color
        if self.color == pieces.Color.WHITE.value:
            self.color = pieces.Color.BLACK.value
        else:
            self.color = pieces.Color.WHITE.value
            self.fullmove += 1

        # Increment clocks
        self.halfmove += 1


    def move_en_passant(self, src_rank, src_file, dst_rank, dst_file):
        """Check if the move activated a possible en passant move.
            Returns whether pawn was captured en passant."""
        # Check if pawn was captured en passant
        result = all([
            self.square2internal(self.en_passant) == (dst_rank, dst_file),
            isinstance(self.board[src_rank, src_file], pieces.Pawn),
        ])

        # Check if new en passant is possible
        if all([
                isinstance(self.board[src_rank, src_file], pieces.Pawn),
                abs(src_rank - dst_rank) == 2,
                src_file == dst_file,
            ]):

            # Update the en passant square
            self.en_passant = self.internal2square(
                (src_rank + dst_rank) // 2,
                src_file,
            )

        # Otherwise disable en passant moves
        else:
            self.en_passant = '-'

        # Return whether en passant capture was performed
        return result


    def move_castling(self, src_rank, src_file, dst_rank, dst_file):
        """Check if the move influences castling rights.
            Returns whether the king castled."""
        # Check if castled
        castled = all([
            isinstance(self.board[src_rank, src_file], pieces.King),
            abs(src_file - dst_file) == 2,
        ])

        # Remove castling rights of specific color, if necessary
        if castled:
            if self.board[src_rank, src_file] == pieces.Color.WHITE:
                self.castling = ''.join(x for x in self.castling if x.islower())
            else:
                self.castling = ''.join(x for x in self.castling if x.isupper())

        # TODO - implement castling move

        # Return result
        return castled


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
                    piece_color = pieces.Color.BLACK
                else:
                    piece_color = pieces.Color.WHITE

                # Set specific piece
                if piece.lower() == 'p':
                    setup[-1].append(pieces.Pawn(piece_color))
                elif piece.lower() == 'n':
                    setup[-1].append(pieces.Knight(piece_color))
                elif piece.lower() == 'b':
                    setup[-1].append(pieces.Bishop(piece_color))
                elif piece.lower() == 'r':
                    setup[-1].append(pieces.Rook(piece_color))
                elif piece.lower() == 'q':
                    setup[-1].append(pieces.Queen(piece_color))
                elif piece.lower() == 'k':
                    setup[-1].append(pieces.King(piece_color))
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
        board.en_passant = en_passant
        board.halfmove   = int(halfmove)
        board.fullmove   = int(fullmove)

        # Return result
        return board



################################################################################
#                                String method                                 #
################################################################################

    def __str__(self):
        """"""
        return self.string()

    def string(self, moves=None):
        # Setup board top
        result  = "╔" + "═══╤"*(self.n_files-1) + "═══╗\n"

        # Setup board rows
        for index_rank, row in enumerate(self.board):
            result += "║"

            for index_file, square in enumerate(row):
                if square:
                    square = str(square)
                else:
                    square = ''

                if moves is not None and moves[index_rank, index_file]:
                    if square:
                        square = '[' + square + ']'
                    else:
                        square = '.'

                result += "{:^3}".format(square)

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

    board_2 = Board.from_fen("rnbqkbnr/pppppppp/8/6Q1/8/4n1p1/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    board = Board.from_fen("rnbqk2r/p4pp1/2p2n2/1pPpp1B1/1b1P2Pp/P1N2N1P/1P2PP2/R2QKB1R b KQkq g3 0 9")

    print(board.string(
        moves = board.moves(4, 7)
    ))
    exit()

    from utils import print_boards_grid

    from time import time
    start = time()
    boards = list()
    for i in range(1000):
        for rank in range(8):
            for file in range(8):
                if board.board[rank, file] is not None:
                    moves = board.moves(rank, file)
                    # boards.append(board.string(
                    #     moves = board.moves(rank, file)
                    # ))

    # print_boards_grid(boards, width=3)

    print(time() - start)
