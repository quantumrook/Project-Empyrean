
from dataclasses import dataclass
from dataclasses import dataclass

@dataclass
class GridPlacement():

    col:        int
    row:        int
    span:       dict[str, int]
    sticky:     str

    def __init__(self, col=0, row=0, span={"col": 1, "row": 1}, sticky='') -> None:
        self.col = col
        self.row = row
        self.span = span
        self.sticky = sticky