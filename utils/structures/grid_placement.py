
from dataclasses import dataclass


@dataclass
class GridPlacement():
    def __init__(self, col=0, row=0, span={"col": 1, "row": 1}, sticky='') -> None:
        self.col    : int               = col
        self.row    : int               = row
        self.span   : dict[str, int]    = span
        self.sticky :str                = sticky
