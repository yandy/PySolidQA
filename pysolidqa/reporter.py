class Reporter(object):
    """
    The "View" of PySolidQA
    implemented the print/report system
    """
    def __init__(self, arg):
        super(Reporter, self).__init__()
        self.arg = arg
