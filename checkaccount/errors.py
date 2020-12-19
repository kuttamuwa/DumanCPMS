from abc import ABC

from DumanCPMS import settings


class DumanMessageInterface(ABC):
    lang = settings.LANGUAGE_CODE

    @classmethod
    def switch_tr(cls, value):
        settings.LANGUAGE_CODE = 'tr-tr'

    @classmethod
    def translate_message(cls):
        pass

    @classmethod
    def translate_errors(cls):
        pass


class CheckAccountBaseException(Exception, DumanMessageInterface):
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

    @classmethod
    def raise_state_on(cls):
        cls.raise_state = True

    @classmethod
    def raise_state_off(cls):
        cls.raise_state = False

    @classmethod
    def translate_message(cls):
        super().translate_message()

    @classmethod
    def translate_errors(cls):
        super().translate_errors()

    @classmethod
    def switch_tr(cls, value):
        cls.translate_message()
        cls.translate_errors()


class AccountDocumentBaseException(Exception, DumanMessageInterface):
    @classmethod
    def translate_message(cls):
        super().translate_message()

    @classmethod
    def translate_errors(cls):
        super().translate_errors()

    @classmethod
    def switch_tr(cls, value):
        super().switch_tr(value)


class NoLangSpecified(CheckAccountBaseException):
    message = 'No Language Setting Specified !'

    @classmethod
    def translate_message(cls):
        super().translate_message()

    @classmethod
    def translate_errors(cls):
        super().translate_errors()

    @classmethod
    def switch_tr(cls, value):
        cls.message = "Herhangi bir dil ayarı seçilmemiş !"


class SysException(CheckAccountBaseException):
    pass


class LegalEntityMustHaveBirthPlace(CheckAccountBaseException):
    message = "Legal Entity must have birth place. Please select it"

    @classmethod
    def translate_message(cls):
        cls.message = "Doğum yeri seçili olmalı ! "

    @classmethod
    def translate_errors(cls):
        super().translate_errors()


class SoleTraderMustHaveTaxPayerNumber(CheckAccountBaseException):
    @classmethod
    def translate_message(cls):
        super().translate_message()

    @classmethod
    def translate_errors(cls):
        super().translate_errors()

    message = "Sole trader must have tax payer number or TCKNO"


class CheckAccountBaseWarnings:
    message = None


class DoesNotExistsWarning(CheckAccountBaseWarnings):
    message = "Check Account Does Not Exists"


class CheckAccountBaseInfo:
    message = None

    @classmethod
    def change_lang(cls, value):
        pass


class CheckAccountCreated(CheckAccountBaseInfo):
    message = 'Account was created !'

    @classmethod
    def change_lang(cls, value):
        cls.message = 'Hesap oluşturuldu !'


# Account Document
class AccountDocumentsBaseWarnings:
    message = None

    @classmethod
    def change_lang(cls, value):
        pass


class ADDoesNotExists(AccountDocumentsBaseWarnings):
    message = 'Account Document Does Not Exists'

    @classmethod
    def change_lang(cls, value):
        if value == 'TR':
            cls.message = 'Döküman bulunamadı !'
