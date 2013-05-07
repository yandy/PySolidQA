from errors import SolidError
from parser import Parser
from translate import Translate

class PySolidQA(object):
    """
    The "controller" of PySolidQA
    this is the interface of this package/lib
    """
    def __init__(self, arg):
        super(PySolidQA, self).__init__()
        self.arg = arg

