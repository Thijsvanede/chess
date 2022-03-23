import numpy as np
import pieces
from typing import Optional, Tuple

class Board(object):

    def __init__(
            self,
            n_ranks : int = 8,
            n_files : int = 8,
        ):
        """Create a chess board for the given number of files and ranks.

            Parameters
            ----------
            n_ranks : int
                Number of ranks on chess board.

            n_files : int
                Number of files on chess board.
            """
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

    def square2internal(self, square: str) -> Optional[Tuple[int, int]]:
        """Returns internal representation for square.

            Parameters
            ----------
            square : str
                String representation of square as {file}{rank}. E.g, e1 is the
                initial square of the white king.

            Returns
            -------
            rank : int
                Rank of square.

            file : int
                File of square.
            """
        if square == '-':
            return None
        else:
            return self.n_ranks - int(square[1]), ord(square[0].lower()) - ord('a')

    def internal2square(self, rank: int, file: int) -> str:
        """Returns string representation of square.

            Parameters
            -------
            rank : int
                Rank of square.

            file : int
                File of square.

            Parameters
            ----------
            square : str
                String representation of square as {file}{rank}. E.g, e1 is the
                initial square of the white king.
            """
        return chr(file + ord('a')) + str(self.n_ranks - rank)

    ########################################################################
    #                              Get moves                               #
    ########################################################################

    def move(
            self,
            src_rank : int,
            src_file : int,
            dst_rank : int,
            dst_file : int,
        ) -> bool:
        """Perform a move by moving the piece from src square to dst square.

            Parameters
            ----------
            src_rank : int
                Rank of source square to move from.

            src_file : int
                File of source square to move from.

            dst_rank : int
                Rank of destination square to move to.

            dst_file : int
                File of destination square to move to.

            Returns
            -------
            success : bool
                True if move was successful.
            """
        # Check if move is allowed
        if self.get_moves(src_rank, src_file)[dst_rank, dst_file]:

            print(f"{self.internal2square(src_rank, src_file)} ({src_rank}, {src_file}) -> {self.internal2square(dst_rank, dst_file)} ({dst_rank}, {dst_file})")

            # Handle special cases
            self.handle_en_passant(src_rank, src_file, dst_rank, dst_file)
            self.handle_castling  (src_rank, src_file, dst_rank, dst_file)
            self.handle_promotion (src_rank, src_file, dst_rank, dst_file)

            # Perform move
            self.move_piece(src_rank, src_file, dst_rank, dst_file)

            # Update internals after a move was made
            self.move_update()

            # Return successful move
            return True

        # Return unsuccessful move
        return False


    def move_piece(
            self,
            src_rank : int,
            src_file : int,
            dst_rank : int,
            dst_file : int,
        ) -> None:
        """Move a piece from a source square to a destination square.

            Note
            ----
            Method does not perform any checks of whether the move is possible.
            Use self.move() to perform all necessary checks.

            Parameters
            ----------
            src_rank : int
                Rank of source square to move from.

            src_file : int
                File of source square to move from.

            dst_rank : int
                Rank of destination square to move to.

            dst_file : int
                File of destination square to move to."""
        # Copy piece from source square to destination square
        self.board[dst_rank, dst_file] = self.board[src_rank, src_file]
        # Remove piece from source square
        self.board[src_rank, src_file] = None


    def get_moves(
            self,
            rank : int,
            file : int,
        ) -> np.ndarray:
        """Get the possible moves for a given square.

            Parameters
            ----------
            rank : int
                Rank of square for which to get moves.

            file : int
                File of square for which to get moves.

            Returns
            -------
            moves : np.array of shape=(self.n_ranks, self.n_files)
                Boolean array representing the available moves of a piece.
            """
        # Case of no piece or incorrect colour:
        if (
                self.board[rank, file] is None or
                self.board[rank, file].color.value != self.color
            ):
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

    ########################################################################
    #                         En passant functions                         #
    ########################################################################

    def handle_en_passant(
            self,
            src_rank : int,
            src_file : int,
            dst_rank : int,
            dst_file : int,
        ) -> None:
        """Handle moves influencing the en passant rule.

            This involves the following actions:
            1. If a pawn takes en passant, remove the captured pawn from the board.
            2. If a pawn moves two squares, set the new en passant square.
            3. If no pawn was moved two squares, clear the en passant square.

            Parameters
            ----------
            src_rank : int
                Rank of source square to move from.

            src_file : int
                File of source square to move from.

            dst_rank : int
                Rank of destination square to move to.

            dst_file : int
                File of destination square to move to.
            """
        # Check if move that was made is en passant
        if self.is_en_passant(src_rank, src_file, dst_rank, dst_file):
            # Remove the captured en passant pawn
            self.board[src_rank, dst_file] = None

        # Check if new en passant move is possible
        if self.is_double_pawn_move(src_rank, src_file, dst_rank, dst_file):
            # Set new en passant square
            self.en_passant = self.internal2square(
                rank = (src_rank + dst_rank) // 2,
                file = src_file,
            )

        # Otherwise, disable en passant moves
        else:
            # Disable en passant move
            self.en_passant = '-'

    def is_en_passant(
            self,
            src_rank : int,
            src_file : int,
            dst_rank : int,
            dst_file : int,
        ) -> bool:
        """Check whether a move is taking en passant.

            Parameters
            ----------
            src_rank : int
                Rank of source square to move from.

            src_file : int
                File of source square to move from.

            dst_rank : int
                Rank of destination square to move to.

            dst_file : int
                File of destination square to move to.

            Returns
            -------
            is_en_passant : bool
                True if move is taking en passant.
            """
        return (
            # Check whether the capturing piece is a pawn
            isinstance(self.board[src_rank, src_file], pieces.Pawn) and
            # Check if the destination square is equal to the en_passant square
            self.square2internal(self.en_passant) == (dst_rank, dst_file)
        )


    def is_double_pawn_move(
            self,
            src_rank : int,
            src_file : int,
            dst_rank : int,
            dst_file : int,
        ) -> bool:
        """Check whether a move is a pawn moving forward two squares.

            Parameters
            ----------
            src_rank : int
                Rank of source square to move from.

            src_file : int
                File of source square to move from.

            dst_rank : int
                Rank of destination square to move to.

            dst_file : int
                File of destination square to move to.

            Returns
            -------
            is_double_pawn_move : bool
                True if move is a double pawn move.
            """
        return (
            # Check whether the moving piece is a pawn
            isinstance(self.board[src_rank, src_file], pieces.Pawn) and
            # Check whether the pawn moved two pieces
            abs(src_rank - dst_rank) == 2
        )

    ########################################################################
    #                          Castling functions                          #
    ########################################################################

    def handle_castling(
            self,
            src_rank : int,
            src_file : int,
            dst_rank : int,
            dst_file : int,
        ) -> None:
        """Handle moves influencing the castling rule.

            This involves the following actions:
            1. If a king castled, move the corresponding rook.
            2. If a king moved, remove all castling rights for that colour.
            3. If a rook moved, remove the castling rights for that rook colour.

            Parameters
            ----------
            src_rank : int
                Rank of source square to move from.

            src_file : int
                File of source square to move from.

            dst_rank : int
                Rank of destination square to move to.

            dst_file : int
                File of destination square to move to.
            """
        # Check if castled
        if self.is_castle_move(src_rank, src_file, dst_rank, dst_file):
            # Move the corresponding rook
            if src_file > dst_file:
                self.move_piece(src_rank, 0, dst_rank, dst_file+1)
            else:
                self.move_piece(src_rank, self.n_files-1, dst_rank, dst_file-1)

        # Check if the king moved
        if isinstance(self.board[src_rank, src_file], pieces.King):
            # Remove castling rights of king colour
            if self.board[src_rank, src_file].color == pieces.Color.WHITE:
                self.castling = ''.join(x for x in self.castling if x.islower())
            else:
                self.castling = ''.join(x for x in self.castling if x.isupper())

        # Check if the rook moved
        elif isinstance(self.board[src_rank, src_file], pieces.Rook):
            # Remove castling rights of the rook color and side
            if self.board[src_rank, src_file].color == pieces.Color.WHITE:
                # White queen side
                if src_file == 0:
                    self.castling = ''.join(x for x in self.castling if x!='Q')
                # White king side
                else:
                    self.castling = ''.join(x for x in self.castling if x!='K')
            else:
                # Black queen side
                if src_file == 0:
                    self.castling = ''.join(x for x in self.castling if x!='q')
                # Black king side
                else:
                    self.castling = ''.join(x for x in self.castling if x!='k')


    def is_castle_move(
            self,
            src_rank : int,
            src_file : int,
            dst_rank : int,
            dst_file : int,
        ) -> bool:
        """Check if a move would be a castling move.

            Parameters
            ----------
            src_rank : int
                Rank of source square to move from.

            src_file : int
                File of source square to move from.

            dst_rank : int
                Rank of destination square to move to.

            dst_file : int
                File of destination square to move to.

            Returns
            -------
            is_castle_move : boolean
                True if move will castle the king
            """
        return (
            # Check whether moving piece is a king
            isinstance(self.board[src_rank, src_file], pieces.King) and
            # Check whether king moves two squares horizontally
            abs(src_file - dst_file) == 2
        )


    ########################################################################
    #                         Promotion functions                          #
    ########################################################################

    def handle_promotion(
            self,
            src_rank : int,
            src_file : int,
            dst_rank : int,
            dst_file : int,
        ) -> None:
        """Handle moves involving promotion of a piece.

            This involves the following actions:
            1. If a pawn reaches the last rank, prompt the user for a piece to
               promote to.
            2. If the piece is chosen, replace the pawn by said piece.

            Parameters
            ----------
            src_rank : int
                Rank of source square to move from.

            src_file : int
                File of source square to move from.

            dst_rank : int
                Rank of destination square to move to.

            dst_file : int
                File of destination square to move to.
            """
        # Check if the move promotes a pawn
        if self.is_promotion(src_rank, src_file, dst_rank, dst_file):
            # Get possible promotion pieces
            possibilities = set('nbrq')
            # Initialise promotion piece
            piece = None

            # Query user until we receive a correct promotion piece
            while piece not in possibilities:
                # Query the user for a piece
                piece = self.query_promotion()

            # Get color of pawn
            color = self.board[src_rank, src_file].color

            # Create new piece
            if piece == 'q':
                piece = pieces.Queen(color)
            elif piece == 'r':
                piece = pieces.Rook(color)
            elif piece == 'b':
                piece = pieces.Bishop(color)
            elif piece == 'n':
                piece = pieces.Knight(color)
            else:
                raise ValueError(
                    f"Unknown piece {piece}, should be one of {possibilities}"
                )

            # Transform pawn to piece
            self.board[src_rank, src_file] = piece


    def is_promotion(
            self,
            src_rank : int,
            src_file : int,
            dst_rank : int,
            dst_file : int,
        ) -> bool:
        """Check if a move is a promotion of a pawn.

            Parameters
            ----------
            src_rank : int
                Rank of source square to move from.

            src_file : int
                File of source square to move from.

            dst_rank : int
                Rank of destination square to move to.

            dst_file : int
                File of destination square to move to.

            Returns
            -------
            is_promotion : boolean
                True if move promotes a pawn.
            """
        return (
            # Check whether moving piece is a pawn
            isinstance(self.board[src_rank, src_file], pieces.Pawn) and
            # Check whether the pawn moved to the last rank
            (dst_rank == 0 or dst_rank == self.n_ranks-1)
        )


    def query_promotion(self) -> str:
        """Query the user for which piece to promote to.

            Returns
            -------
            piece : str ('n'|'b'|'r'|'q')
                String representation of piece, can be 'n', 'b', 'r', 'q'.
            """
        # Get possible promotion pieces
        possibilities = set('nbrq')
        # Initialise promotion piece
        piece = None

        # Query user until we receive a correct promotion piece
        while piece not in possibilities:
            # Query the user for a piece
            piece = input('Please select a piece to promote to (n/b/r/q): ')
            # Get piece as lowercase
            piece = piece.lower()
            
            # Give feedback if required
            if piece not in possibilities:
                print("That is not an available choice!")

        # Return piece
        return piece

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
