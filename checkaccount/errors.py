class NoLangSpecified(ValueError):
    pass


class SysException(Exception):
    pass


class LegalEntityMustHaveBirthPlace(SysException):
    pass


class SoleTraderMustHaveTaxPayerNumber(SysException):
    pass
