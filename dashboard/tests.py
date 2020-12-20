from django.test import TestCase
from risk_analysis.models import DataSetModel
from risk_analysis.views import DataSetWarnings


class DashboardTests(TestCase):
    risk_dataset = DataSetModel
    warning_dataset = DataSetWarnings(risk_dataset)

    def __init__(self):
        self.risk_dataset = DataSetModel.objects.first()
        super(DashboardTests, self).__init__(self)

    def test_recent_accounts(self, latest=5):
        accounts = self.warning_dataset.recent_accounts()[:latest]
        print(accounts)

    @staticmethod
    def test_recent_checkaccounts(latest=5):
        from checkaccount.models import CheckAccount
        customers = CheckAccount.objects.all()[:latest]
        return customers

    @staticmethod
    def test_limit_exceeds():
        DataSetWarnings().limit_exceed_warning()

    @staticmethod
    def test_maturity_exceeds():
        pass

    @staticmethod
    def test_period_velocity():
        pass

    @staticmethod
    def test_check_endeks_verisi():
        pass

    @staticmethod
    def test_arkasi_yazili_cekler():
        pass

    @staticmethod
    def test_kredi_limiti_daralanlar():
        pass

    @staticmethod
    def test_kredi_limiti_kapatilanlar():
        pass

    @staticmethod
    def test_vergi_borcu():
        pass

    @staticmethod
    def test_sgk_borcu():
        pass

    @staticmethod
    def test_kara_liste():
        pass

    @staticmethod
    def test_findeks_kredi_notu():
        pass

    @staticmethod
    def test_karekodlu_cek_skoru():
        pass
