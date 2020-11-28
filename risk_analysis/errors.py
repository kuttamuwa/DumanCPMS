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


class DoesNotExistValueError(RiskAnalysisBaseException):
    pass


class ValidationError(RiskAnalysisBaseException):
    message = "Vade hızı boş verilmiş. Hızın bulunması için gerekli diğer veriler olan son "
    "12 aylık ortalama sipariş tutarı ve bakiye bilgileri de eksik. \n"
    "Algoritmanın sağlıklı çalışabilmesi için ilgili verileri lütfen doldurun !"


class BalanceError(DoesNotExistValueError):
    message = "Bakiye verisi doldurulmalı ! \n"
    "Ozellikle devir gunu verilmediyse !"


class MaturitySpeedError(RiskAnalysisBaseException):
    message = "Vade hızı verisi doldurulmamış"
