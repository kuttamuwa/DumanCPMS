class RiskAnalysisBaseException(Exception):
    raise_state = False
    message = None
    errors = None

    @classmethod
    def switch_tr(cls):
        pass

    @classmethod
    def switch_en(cls):
        pass

    def __init__(self, message=None, errors=None):
        self.message = message
        self.errors = errors

        if self.raise_state:
            raise super(RiskAnalysisBaseException, self).__init__(self.message)
        else:
            pass


class DoesNotExistValueError(RiskAnalysisBaseException):
    @classmethod
    def switch_tr(cls):
        super().switch_tr()

    @classmethod
    def switch_en(cls):
        pass


class CADoesNotExists(DoesNotExistValueError):
    message = 'Check Account Does Not Exists'

    @classmethod
    def switch_tr(cls):
        super().switch_tr()

    @classmethod
    def switch_en(cls):
        pass


class ValidationError(RiskAnalysisBaseException):
    message = "Vade hızı boş verilmiş. Hızın bulunması için gerekli diğer veriler olan son "
    "12 aylık ortalama sipariş tutarı ve bakiye bilgileri de eksik. \n"
    "Algoritmanın sağlıklı çalışabilmesi için ilgili verileri lütfen doldurun !"

    @classmethod
    def switch_tr(cls):
        super().switch_tr()

    @classmethod
    def switch_en(cls):
        pass


class BalanceError(DoesNotExistValueError):
    message = "Bakiye verisi doldurulmalı ! \n"
    "Ozellikle devir gunu verilmediyse !"

    @classmethod
    def switch_tr(cls):
        super().switch_tr()

    @classmethod
    def switch_en(cls):
        pass


class MaturitySpeedError(RiskAnalysisBaseException):
    message = "Vade hızı verisi doldurulmamış"

    @classmethod
    def switch_tr(cls):
        super().switch_tr()

    @classmethod
    def switch_en(cls):
        pass


class CreationErrors(RiskAnalysisBaseException):
    @classmethod
    def switch_tr(cls):
        super().switch_tr()

    @classmethod
    def switch_en(cls):
        pass


class CustomerNumberError(CreationErrors):
    message = 'Customer field has to be number or string !'

    @classmethod
    def switch_en(cls):
        pass

    @classmethod
    def switch_tr(cls):
        pass
