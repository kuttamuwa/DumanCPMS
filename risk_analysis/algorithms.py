import numpy as np
import pandas as pd

from appconfig.errors import DomainPointsValueError
from appconfig.models import Domains, Subtypes, RiskDataConfigModel
from risk_analysis.models import DataSetManager, DataSetModel, RiskDataSetPoints
import bisect


class ControlRiskDataSet:
    def __init__(self, riskds_pk=None):
        self.domains = Domains.objects.all()
        self.subtypes = Subtypes.objects.all()
        self.risk_dataset = None

        self.risk_configs = RiskDataConfigModel.objects.all()

        # setter
        self.set_risk_dataset(riskds_pk)

    def set_risk_dataset(self, riskds_pk):
        if riskds_pk is None:
            raise NotImplementedError('Tüm verilere analiz yapmak henüz eklenmemiştir !')

            # rd = DataSetModel.objects.all()

        else:
            rd = DataSetModel.objects.get(pk=riskds_pk)

        print(f"Risk dataset : {rd.customer}")
        self.risk_dataset = rd

    def get_intervals_by_name(self, name, convert_df=False):
        d = self.domains.get(name=name)
        s = self.subtypes.filter(domain=d)

        if convert_df:
            df = pd.DataFrame(s.values('max_interval', 'min_interval', 'pts'))
            return df

        return s

    @property
    def get_risk_dataset(self):
        return self.risk_dataset

    def domain_controls(self, silent=True):
        try:
            self.domains.model.get_total_points(alert=True)
        except DomainPointsValueError as err:
            if silent:
                raise err
            else:
                return False

    def get_domains(self):
        return self.domains

    def get_subtypes(self):
        return self.subtypes

    def get_domain_and_subtypes(self):
        return self.get_domains(), self.get_subtypes()

    def get_subtype_via_domain(self):
        self.get_domain_and_subtypes()

    def control_columns(self):
        pass

    def control_data(self):
        pass


class AnalyzingRiskDataSet(ControlRiskDataSet):
    """
    It also converts bulk data into categorized data
    # todo: 100'den buyukse veya 0'dan kucukse uyari ver.
    """

    def __init__(self, riskds_pk=None, analyze_right_now=True):
        super().__init__(riskds_pk)
        self.analyzed_data = None
        self.analyze_decision = True  # default value
        self.risk_pts = None

        self.controls()

        if analyze_right_now:
            self.analyze_all()

    def set_risk_points_object(self):
        if self.risk_dataset is not None:
            customer = self.risk_dataset.customer
            self.risk_pts = RiskDataSetPoints(customer=customer)

    def controls(self):
        self.domain_controls()
        # bla bla
        # if settings.DEBUG:
        #     ImportAllDomains.import_all_domains()
        #     ImportAllSubtypes.import_subtypes()

    def get_analyzed_data(self):
        return self.analyzed_data

    @staticmethod
    def get_points_from_value(value, dataframe):
        pts = None

        if value is not None:
            for index, row in dataframe.iterrows():
                if row["min_interval"] < value < row["max_interval"]:
                    pts = row['pnt']
        return pts

    def analyze_decision_based_on_latest12months_payback(self):
        """
        Son 12 Ay İade %si: İade aylık satışın % 10 unu aşmazsa hesaplama yapılmayacak
        HINT: Puanlaması başka fonksiyonda
        """
        rd = self.get_risk_dataset

        if pd.isna(rd.last_twelve_months_payback_perc):
            print("Son 12 aylık ortalama iade yuzdesi verisi bulunamamıştır. \n"
                  "Analiz kararı (default) Evet olarak verilmiştir.")
            self.analyze_decision = True  # no data but we will analyze

        else:
            if rd.avg_order_amount_last_twelve_months is np.nan:
                print("Analiz karari son 12 aylık ortalama sipariş tutarı verisi olmadığı için verilemedi. \n")
                print("Bu yüzden analiz kararı (default) Evet olarak devam edilecek.")

            else:
                if rd.avg_order_amount_last_twelve_months * 0.1 <= rd.last_twelve_months_payback_perc:
                    self.analyze_decision = False
                    print("Analiz yapilmayacak.")

            return self.analyze_decision

    def detect_son_12ay_satis_ort_sapma(self):
        """
        %0-20 azalış	3
        %20-50 azalış	5
        %50-75 azalış	10
        """

        pnt_df = self.get_intervals_by_name('Son 12 Ay Satış Ortalamasından Sapma', convert_df=True)
        rd = self.get_risk_dataset
        aberration = rd.last_3_months_aberration
        pts = self.get_points_from_value(aberration, pnt_df)

        self.risk_pts
        return pts

    def analyze_kar(self):
        """
        %0-5	15
        %5-10	10
        %10-15	7
        %15-20	5
        %20 ve üzeri	3

        """
        pnt_df = self.get_intervals_by_name('Kar', convert_df=True)
        rd = self.get_risk_dataset
        profit = rd.profit
        pts = self.get_points_from_value(profit, pnt_df)

        return pts

    def analyze_son_12_ay_iade_yuzdesi(self):
        """
        %0-20 	3
        %20-50 	5
        %50-75 	10
        %75 üzeri 	15

        """
        pnt_df = self.get_intervals_by_name('Son 12 ay iade yüzdesi', convert_df=True)
        rd = self.get_risk_dataset
        last_twelve_months_payback_perc = rd.last_twelve_months_payback_perc
        pts = self.get_points_from_value(last_twelve_months_payback_perc, pnt_df)

        return pts

    def analyze_ort_gecikme_gun_sayisi(self):
        """
        10 gün	5
        20 gün	10
        30 gün ve üzeri	15

        """
        pnt_df = self.get_intervals_by_name('Ortalama Gecikme Gün Sayısı', convert_df=True)
        rd = self.get_risk_dataset
        avg_delay_time = rd.avg_delay_time
        pts = self.get_points_from_value(avg_delay_time, pnt_df)

        return pts

    def analyze_ort_gecikme_gun_bakiyesi(self):
        """
        0-50000	5
        50000-100000	8
        100000 ve üzeri	10

        """
        pnt_df = self.get_intervals_by_name('Ortalama Gecikme Gün Bakiyesi')
        rd = self.get_risk_dataset
        avg_delay_balance = rd.avg_delay_balance
        pts = self.get_points_from_value(avg_delay_balance, pnt_df)

        return pts

    def analyze_devir_gunu(self):
        """
        0-15	5
        15-30	10
        30 ve üzeri	15

        """
        pnt_df = self.get_intervals_by_name('Devir Günü')
        rd = self.get_risk_dataset

        period_day = rd.period_day  # todo bu kısım getter'a verilmeli
        if period_day is None:
            period_day = DataSetManager.calc_period_day(rd.period_velocity)

        pts = self.get_points_from_value(period_day, pnt_df)

        return pts

    def detect_teminat_limit_riskini_karsilama_seviyesi(self):
        """
        %0-20 	15
        %20-50 	10
        %50-75 	5
        %75 üzeri 	3

        """
        pnt_df = self.get_intervals_by_name('Teminat Limit Riskini Karşılama Seviyesi')
        rd = self.get_risk_dataset
        teminat_limit_risk_kars_seviyesi = (rd.warrant_amount / rd.limit) * 100
        pts = self.get_points_from_value(teminat_limit_risk_kars_seviyesi, pnt_df)

        return pts

    def bulk_to_dataframe(self):
        return self.analyzed_data

        return toplam

    def analyze_all(self):
        # todo: logging
        self.analyze_decision_based_on_latest12months_payback()  # true -> analiz yapilir, false -> yapilmaz. default -> true.

        # eger yukaridaki False dondururse hesaplama yapilmaz?<
        if self.analyze_decision:
            self.set_risk_points_object()  # risk point was created

            self.detect_son_12ay_satis_ort_sapma()
            self.analyze_kar()
            self.analyze_son_12_ay_iade_yuzdesi()
            self.analyze_ort_gecikme_gun_sayisi()
            self.analyze_ort_gecikme_gun_bakiyesi()
            self.analyze_devir_gunu()
            self.detect_teminat_limit_riskini_karsilama_seviyesi()

            return self.analyzed_data

        else:
            # todo: logging
            return False
