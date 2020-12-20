class AppConfigBaseException(BaseException):
    raise_state = False
    message = None
    errors = None

    @classmethod
    def turn_raise_setting(cls):
        cls.raise_state = True

    @classmethod
    def set_msg(cls, value):
        if value is not None:
            cls.message = value

    @classmethod
    def set_err(cls, value):
        if value is not None:
            cls.errors = value

    def raise_once(self):
        raise super(BaseException, self).__init__(self.message, self.errors)

    def __init__(self, message=None, errors=None):
        self.set_msg(message)
        self.set_err(errors)

        if self.raise_state:
            raise super(AppConfigBaseException, self).__init__(self.message)
        else:
            pass


class CannotExceeds100(AppConfigBaseException):
    message = "Cannot exceeds 100"


class SubtypePoints(AppConfigBaseException):
    message = f"Summary of subtype points cannot be exceed 100"


class DomainPointsValueError(AppConfigBaseException):
    message = "Summary of domain points must be 100"
