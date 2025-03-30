from .sorting import *
from . import sorting

__all__ = ["algoPrint", "algoWrite"]
__submodule__ = {"sorting": sorting}

from .print import algoPrint
from .write import algoWrite
