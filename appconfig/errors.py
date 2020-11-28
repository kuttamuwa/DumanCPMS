class CheckAccountBaseException(Exception):
    raise_state = False
    message = None
    errors = None

    def __init__(self, message, errors):
        self.message = message
        self.errors = errors

        if self.raise_state:
            raise super(CheckAccountBaseException, self).__init__(self.message)
        else:
            pass


class CannotExceeds100(CheckAccountBaseException):
    message = "Cannot exceeds 100"


class SubtypePoints(CheckAccountBaseException):
    message = f"Summary of subtype points cannot be exceed 100"


class DomainPoints(CheckAccountBaseException):
    message = "Summary of domain points cannot be exceed 100"
