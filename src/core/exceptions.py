"""PostScript Interpreter Exceptions"""


class ParseFailed(Exception):
    """A exception indicating that parsing has failed."""

    def __init__(self, message):
        super().__init__(message)


class TypeMismatch(Exception):
    """A exception indicating that type mismatch has failed."""

    def __init__(self, message):
        super().__init__(message)
