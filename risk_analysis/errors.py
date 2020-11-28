class DoesNotExistValueError(ValueError):
    raise ValueError


class MaturitySpeedError(DoesNotExistValueError):
    raise ValueError("Vade hızı boş verilmiş. Hızın bulunması için gerekli diğer veriler olan son "
                     "12 aylık ortalama sipariş tutarı ve bakiye bilgileri de eksik. \n"
                     "Algoritmanın sağlıklı çalışabilmesi için ilgili verileri lütfen doldurun !")


class BalanceError(DoesNotExistValueError):
    raise ValueError("Bakiye verisi doldurulmalı ! \n"
                     "Ozellikle devir gunu verilmediyse !")
