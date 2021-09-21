class King(object):

    def __init__(self, color='white'):
        self.color = color

    def __str__(self):
        return "♔" if self.color == 'white' else "♚"
