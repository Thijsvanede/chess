import os
import io
import pygame

class GUI(object):

    def __init__(self,
            board,
            title  = "Chess",
            fps    = 30,
            width  = 640,
            height = 640,
            style  = {
                "square": {
                    "light": [255, 228, 196],
                    "dark" : [205, 133,  63],
                }
            }
        ):

        # Initialise variables
        self.title  = title
        self.height = height
        self.width  = width
        self.fps    = fps

        # Setup color schemes
        self.square_light = style.get('square',{}).get('light', [255, 228, 196])
        self.square_dark  = style.get('square',{}).get('dark' , [205, 133,  63])
        self.colors = [self.square_light, self.square_dark]

        # Setup chess board variables
        self.board = board

        self.square_width  = self.width  / self.board.n_ranks
        self.square_height = self.height / self.board.n_files

        self.overlay      = None
        self.last_clicked = (None, None)

        # Set running to false
        self.running = True

    ########################################################################
    #                              Run method                              #
    ########################################################################

    def run(self):
        """Run board, invokes setup() and loop() methods."""
        # First setup board
        self.setup()
        # Loop forever
        self.loop()

    ########################################################################
    #                             Setup method                             #
    ########################################################################

    def setup(self):
        """Setup the game."""
        # Initialise pygame
        pygame.init()

        # Setup display
        self.display = pygame.display.set_mode((self.width, self.height))

        # Set Title
        pygame.display.set_caption(self.title)

        # Set FPS
        self.clock = pygame.time.Clock()

        # Load images
        self.images = self.load_images(
            os.path.join(os.path.dirname(__file__), 'img')
        )

    def load_images(self, directory):
        """Load all images from a directory"""
        # Initialise result
        result = dict()

        # Loop over all files in directory
        for file in os.listdir(directory):
            # Get path to file
            path = os.path.join(directory, file)

            # Parse PNG extension
            if file.lower().endswith('.png'):
                with open(path) as infile:
                    # Load image
                    image = pygame.image.load(infile).convert_alpha()
                    # Scale image
                    image = pygame.transform.scale(
                        image,
                        (round(self.square_width), round(self.square_height))
                    )
                    # Store image
                    result[file] = image

        # Return result
        return result

    ########################################################################
    #                             Loop method                              #
    ########################################################################

    def loop(self):
        while self.running:
            # Draw board
            self.draw_board()
            # Draw pieces
            self.draw_pieces()
            # Draw overlay
            self.draw_overlay()

            # Update display
            pygame.display.update()
            self.clock.tick(self.fps)

            # Handle any events
            self.handle_events()

    ########################################################################
    #                      Auxiliary drawing methods                       #
    ########################################################################

    def draw_board(self):
        """Draw squares on chess board."""
        # Loop over all ranks
        for rank in range(self.board.n_ranks):
            # Loop over all files
            for file in range(self.board.n_files):
                # Draw square
                pygame.draw.rect(
                    surface = self.display,
                    color   = self.colors[(rank + file) % 2],
                    rect    = (
                        file * self.square_width,
                        rank * self.square_height,
                        self.square_width,
                        self.square_height,
                    )
                )

    def draw_pieces(self):
        """Draw pieces on board."""
        # Loop over all ranks
        for rank in range(self.board.n_ranks):
            # Loop over all files
            for file in range(self.board.n_files):
                # Get piece
                piece = self.board.board[rank, file]

                # Check if there is a piece on the board
                if piece:
                    # If so, get corresponding image
                    image = self.images[f"{str(piece)}.png"]
                    # Display image
                    self.display.blit(
                        image, (
                        file * self.square_width,
                        rank * self.square_height,
                    ))

    def draw_overlay(self):
        """"""
        # Check if overlay should be drawn
        if self.overlay is not None:

            # Loop over all ranks
            for rank in range(self.board.n_ranks):
                # Loop over all files
                for file in range(self.board.n_files):
                    # Check if we should draw overlay
                    if self.overlay[rank, file]:
                        pygame.draw.circle(
                            surface = self.display,
                            color   = (150, 150, 150),
                            center  = (
                                (file + 0.5) * self.square_width,
                                (rank + 0.5) * self.square_height,
                            ),
                            radius  = self.square_width // 8,
                        )


    ########################################################################
    #                          Auxiliary methods                           #
    ########################################################################

    def handle_events(self):
        """Handle pygame events."""
        # Loop over all events
        for event in pygame.event.get():
            # Exit event
            if event.type == pygame.QUIT:
                # Set running to False
                self.running = False

            # Mouse press event
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Get coordinates of mouse press
                x, y = pygame.mouse.get_pos()

                # Get file and rank using coordinates
                file = int(x // self.square_width)
                rank = int(y // self.square_height)

                # Check if current click is same as last
                if (rank, file) == self.last_clicked:
                    self.last_clicked = (None, None)
                    self.overlay      = None
                    return

                # Check if move is allowed
                elif self.last_clicked != (None, None):
                    # Get possible moves of last clicked
                    moves = self.board.get_moves(*self.last_clicked)

                    # If move is allowed
                    if moves[rank, file]:
                        # Perform move
                        self.board.move(
                            src_rank = self.last_clicked[0],
                            src_file = self.last_clicked[1],
                            dst_rank = rank,
                            dst_file = file,
                        )

                        # Clear moves
                        self.last_clicked = (None, None)
                        self.overlay      = None
                        return


                # Get piece from file and rank
                piece = self.board.board[rank, file]

                if piece is None:
                    self.last_clicked = (None, None)
                    self.overlay      = None
                else:
                    self.last_clicked = (rank, file)
                    self.overlay = self.board.get_moves(rank, file)
