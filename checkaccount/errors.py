class RiskAnalysisBaseException(Exception):
    raise_state = False
    message = None
    errors = None

    def __init__(self, message=None, errors=None):
        self.message = message
        self.errors = errors

        if self.raise_state:
            raise super(RiskAnalysisBaseException, self).__init__(self.message)
        else:
            pass


class NoLangSpecified(RiskAnalysisBaseException):
    pass


class SysException(RiskAnalysisBaseException):
    pass


class LegalEntityMustHaveBirthPlace(RiskAnalysisBaseException):
    message = "Legal Entity must have birth place. Please select it"


class SoleTraderMustHaveTaxPayerNumber(RiskAnalysisBaseException):
    message = "Sole trader must have tax payer number or TCKNO"
