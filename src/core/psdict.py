"""PostScript Dictionary Object"""


class PSDict:
    """PostScript Dictionary Object"""

    def __init__(self):
        self.dict = {}
        self.parent = None  # For static scoping

    def __setitem__(self, key, value):
        self.dict[key] = value

    def __getitem__(self, key):
        return self.dict[key]

    def set_parent(self, parent):
        self.parent = parent

    def __contains__(self, key):
        return key in self.dict

    def __repr__(self):
        return f"PSDict({self.dict})"

    def __str__(self):
        return f"PSDict({self.dict})"
