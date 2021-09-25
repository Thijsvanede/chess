def print_boards_line(boards, separator=' ', end='\n'):
    """Print multiple boards on a single line."""
    for line in zip(*[board.split('\n') for board in boards]):
        print(separator.join(line))

def print_boards_grid(boards, width, separator=' ', end='\n\n'):
    """Print multiple boards in a grid."""
    for chunk in range(0, len(boards), width):
        print_boards_line(
            boards    = boards[chunk:chunk+width],
            separator = separator,
            end       = end,
        )
