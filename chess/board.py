import numpy as np

class Board(object):

    def __init__(self, width=8, height=8):
        """"""
        self.width  = width
        self.height = height
        self.board  = np.zeros((width, height), dtype=object)

    ########################################################################
    #                             I/O methods                              #
    ########################################################################

    @classmethod
    def from_fen(cls, fen):
        """"""
        board = Board()



################################################################################
#                                String method                                 #
################################################################################

    def __str__(self):
        """"""
        # Setup board top
        result  = "╔" + "═══╤"*(self.width-1) + "═══╗\n"

        # Setup board rows
        for index_rank, row in enumerate(self.board):
            result += "║"

            for index_file, square in enumerate(row):
                result += "{:^3}".format(str(square) if square else ' ')

                if index_file == self.width-1 and index_rank != self.height-1:
                    result += "║\n╟" + "───┼"*(self.width-1) + "───╢\n"
                elif index_file == self.width-1 and index_rank == self.height-1:
                    # Setup board bottom
                    result += "║\n╚" + "═══╧"*(self.width-1) + "═══╝"
                else:
                    result += '│'

        # Return result
        return result

if __name__ == "__main__":
    board = Board()
    print(board)
