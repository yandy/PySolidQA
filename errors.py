class SolidError(Exception):
    """docstring for SolidError"""
    def __init__(self, arg):
        self.arg = arg

    def __str__(self):
        self.arg

