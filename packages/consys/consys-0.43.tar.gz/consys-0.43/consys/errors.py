"""
Errors
"""


class BaseError(Exception):
    """Base error"""

    code = 0

    def __init__(self, field):
        self.txt = field
        super().__init__()


class ErrorSpecified(BaseError):
    """Not all parameters"""

    code = 4


class ErrorBusy(BaseError):
    """Busy"""

    code = 5


class ErrorInvalid(BaseError):
    """Invalid
    Does not pass the criteria
    """

    code = 6


class ErrorWrong(BaseError):
    """Wrong
    Passes the criteria, but is incorrect
    """

    code = 7


class ErrorUpload(BaseError):
    """Uploading to the server"""

    code = 8


class ErrorAccess(BaseError):
    """No rights"""

    code = 9


class ErrorEmpty(BaseError):
    """Nothing to display"""

    code = 10


class ErrorEnough(BaseError):
    """Not enough"""

    code = 11


class ErrorBlock(BaseError):
    """Blocked"""

    code = 12


class ErrorType(BaseError):
    """Incorrect data type"""

    code = 13


class ErrorCount(BaseError):
    """Quantity limit"""

    code = 14


class ErrorRepeat(BaseError):  # TODO: Already / Duplicate
    """Duplicate"""

    code = 15


class ErrorTime(BaseError):
    """Time expired"""

    code = 16


class ErrorUnsaved(BaseError):
    """The object has not been saved yet"""

    code = 17
