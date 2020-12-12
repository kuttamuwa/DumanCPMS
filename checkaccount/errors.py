class CheckAccountBaseException(Exception):
    raise_state = False
    message = None
    errors = None

    def __init__(self, message=None, errors=None):
        self.message = message
        self.errors = errors

        if self.raise_state:
            raise super(CheckAccountBaseException, self).__init__(self.message)
        else:
            pass


class NoLangSpecified(CheckAccountBaseException):
    pass


class SysException(CheckAccountBaseException):
    pass


class LegalEntityMustHaveBirthPlace(CheckAccountBaseException):
    message = "Legal Entity must have birth place. Please select it"


class SoleTraderMustHaveTaxPayerNumber(CheckAccountBaseException):
    message = "Sole trader must have tax payer number or TCKNO"
