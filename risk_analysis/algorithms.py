from appconfig.models import Domains, Subtypes
from risk_analysis.models import DataSetModel, RiskDataSetPoints, DataSetManager
import numpy as np
import pandas as pd

"""
# todo : Puanlamaların yönetileceği bir admin paneli hazırlanacak.

"""


class ControlRiskDataSet:
    def __init__(self, risk_model_object):
        self.risk_model_object = risk_model_object
        self.domains = Domains.objects.all()
        self.subtypes = Subtypes.objects.all()

    def control_columns(self):
        pass

    def control_data(self):
        pass


class AnalyzingRiskDataSet(ControlRiskDataSet):
    """
    It also converts bulk data into categorized data
    # todo: 100'den buyukse veya 0'dan kucukse uyari ver.
    """

    def __init__(self, risk_model_object, analyze_right_now=True):
        super().__init__(risk_model_object)
        self.analyzed_data = None
        self.analyze_decision = True  # default value

        self.risk_point_object = RiskDataSetPoints(customer_id=self.risk_model_object.related_customer)  # almost empty

        if analyze_right_now:
            self.analyze_all()

    def get_analyzed_data(self):
        return self.analyzed_data

    def save_risk_dataset_data(self):
        self.risk_model_object.save()

    def save_risk_points_data(self):
        self.risk_point_object.save()

    def detect_son_12ay_iade_yuzdesi(self):
        """
        Son 12 Ay İade %si: İade aylık satışın % 10 unu aşmazsa hesaplama yapılmayacak
        HINT: Puanlaması başka fonksiyonda
        """
        last_twelve_months_payback_perc = self.risk_model_object.last_twelve_months_payback_perc
        if pd.isna(last_twelve_months_payback_perc):
            # todo: logging
            print("Son 12 aylık ortalama iade yuzdesi verisi bulunamamıştır. \n"
                  "Analiz kararı (default) Evet olarak verilmiştir.")
            self.analyze_decision = True  # no data but we will analyze

        else:
            avg_order_amount_last_twelve_months = self.risk_model_object.avg_order_amount_last_twelve_months
            if avg_order_amount_last_twelve_months is np.nan:
                # todo: logging
                print("Analiz karari son 12 aylık ortalama sipariş tutarı verisi olmadığı için verilemedi. \n")
                print("Bu yüzden analiz kararı (default) Evet olarak devam edilecek.")

            else:
                if avg_order_amount_last_twelve_months * 0.1 <= last_twelve_months_payback_perc:
                    self.analyze_decision = False
                    # todo: logging
                    print("Analiz yapilmayacak.")

            return self.analyze_decision

    def detect_son_12ay_satis_ort_sapma(self):
        """
        %0-20 azalış	3
        %20-50 azalış	5
        %50-75 azalış	10
        """
        pts_dict = {(0, -20): 3,
                    (-20, -50): 5,
                    (-50, -75): 10,
                    (-75, -100): 15}

        # todo: Veride son 12 aylik satis ortalamasindan sapma yazmiyor. Burayı nasıl bulacağız ? -> DAVUT ABIYE.
        # TODO: Biz son 3 aylık sapmayı kullanarak hesapladık, doğru mu?

        # last_3_months_aberration = self.risk_model_object.last_3_months_aberration

        avg_order_last_3_months = self.risk_model_object.avg_order_amount_last_three_months
        avg_order_last_12_months = self.risk_model_object.avg_order_amount_last_twelve_months

        last_3_months_aberration = ((
                                            avg_order_last_3_months - avg_order_last_12_months) / avg_order_last_12_months) * 100
        pts = None
        if not pd.isna(last_3_months_aberration):
            last_3_months_aberration = float(last_3_months_aberration)
            if last_3_months_aberration >= 0:
                pts = 0

            else:
                for t in pts_dict.items():
                    if t[0][0] < last_3_months_aberration < t[0][1]:
                        pts = t[1]

            if pts is not None:
                self.risk_point_object.son_12ay_ortalama_sapma_pts = pts
            else:
                # todo: logging
                print("Son 12 ay ortalama sapmaya gore risk puan hesaplamasi yapilamadi ?")
        else:
            # todo: logging
            print("Son 3 ayin yila oranla satış ortalamasından sapma verisi bulunamamıştır.")

    def analyze_kar(self):
        """
        %0-5	15
        %5-10	10
        %10-15	7
        %15-20	5
        %20 ve üzeri	3

        """
        pts_dict = {
            (0, 5): 15,
            (5, 10): 10,
            (10, 15): 7,
            (15, 20): 5,
            (20, 100): 3
        }
        kar = round(self.risk_model_object.profit_percent * 100)
        pts = None

        if not pd.isna(kar):
            for t in pts_dict.items():
                if t[0][0] < kar <= t[0][1]:
                    pts = t[1]

                if pts is not None:
                    self.risk_point_object.kar_pts = pts

                else:
                    print("Karın risk puanı hesaplanamamıştır ?")
                    # todo: logging

    def analyze_son_12_ay_iade(self):
        """
        %0-20 	3
        %20-50 	5
        %50-75 	10
        %75 üzeri 	15

        """
        pts_dict = {
            (0, 20): 3,
            (20, 50): 5,
            (50, 75): 10,
            (75, 100): 15
        }
        iade = self.risk_model_object.last_twelve_months_payback_perc
        pts = None

        if not pd.isna(iade):
            for t in pts_dict.items():
                if t[0][0] < iade <= t[0][1]:
                    pts = t[1]

                if pts is not None:
                    self.risk_point_object.iade_pts = pts

                else:
                    print("Iade puanlaması yapılamamıştır ?")
                    # todo: logging

    def analyze_ort_gecikme_gun_sayisi(self):
        """
        10 gün	5
        20 gün	10
        30 gün ve üzeri	15

        """
        pts_dict = {
            (0, 10): 5,
            (10, 20): 10,
            (20, 30): 15,
            (30, 999999): 15
        }
        pts = None

        avg_delay_time = self.risk_model_object.avg_delay_time
        if not pd.isna(avg_delay_time):
            for t in pts_dict.items():
                if t[0][0] < avg_delay_time <= t[0][1]:
                    pts = t[1]

            if pts is not None:
                self.risk_point_object.ort_gecikme_gun_bakiyesi_pts = pts

            else:
                print("Ortalama gecikme gun sayisina göre puanlama yapılamamıştır ?")
                # todo: logging

    def analyze_ort_gecikme_gun_bakiyesi(self):
        """
        0-50000	5
        50000-100000	8
        100000 ve üzeri	10

        """
        pts_dict = {
            (0, 50000): 5,
            (50000, 10000): 8,
            (100000, np.inf): 10
        }
        pts = None

        ort_gecikme_gun_bakiyesi = self.risk_model_object.avg_delay_balance
        if not pd.isna(ort_gecikme_gun_bakiyesi):
            for t in pts_dict.items():
                if t[0][0] < ort_gecikme_gun_bakiyesi <= t[0][1]:
                    pts = t[1]

            if pts is not None:
                self.risk_point_object.ort_gecikme_gun_bakiyesi_pts = pts

            else:
                print("Ortalama gecikme gun bakiyesi puani hesaplanamamıştır ?")
                # todo: logging

        else:
            print("Ortalama gecikme gun bakiyesi bulunamamıştır ?")

        pass

    def analyze_devir_gunu(self):
        """
        0-15	5
        15-30	10
        30 ve üzeri	15

        """
        pts_dict = {
            (0, 90): 5,
            (90, 150): 10,
            (150, np.inf): 15
        }
        pts = None

        devir_gunu = self.risk_model_object.period_day
        if pd.isna(devir_gunu):
            # veride yok, hesaplamak gerek
            devir_gunu = DataSetManager.calc_period_day(self.risk_model_object.period_velocity)

        for t in pts_dict.items():
            if t[0][0] < devir_gunu <= t[0][1]:
                pts = t[1]

        if pts is not None:
            self.risk_point_object.devir_gunu_pts = pts

    def detect_teminat_limit_riskini_karsilama_seviyesi(self):
        """
        %0-20 	15
        %20-50 	10
        %50-75 	5
        %75 üzeri 	3

        """
        pts_dict = {
            (0, 20): 15,
            (20, 50): 10,
            (50, 75): 5,
            (75, 100): 3
        }
        pts = None

        if self.risk_model_object.warrant_state is False:
            print("Teminat durumu olmadığı için limit risk karşılama seviyesi puanı yapılmamıştır.")

        else:
            teminat_limit_risk_kars_seviyesi = (self.risk_model_object.warrant_amount / self.risk_model_object.limit) * 100

            if teminat_limit_risk_kars_seviyesi is None:
                print("Teminat limit riskini karsilama seviyesi ")

            for t in pts_dict.items():
                if t[0][0] < teminat_limit_risk_kars_seviyesi <= t[0][1]:
                    pts = t[1]

                if pts is None:
                    print("Teminat limit riskini karşılama seviyesi için puanlama yapılamamıştır")

                self.risk_point_object.teminatin_limit_riskini_karsilamasi_pts = pts

    def bulk_to_dataframe(self):
        return self.analyzed_data

    def total_customer_point(self):
        toplam = self.risk_point_object.ort_gecikme_gun_bakiyesi_pts + self.risk_point_object.ort_gecikme_pts + \
                 self.risk_point_object.teminatin_limit_riskini_karsilamasi_pts + \
                 self.risk_point_object.son_12ay_ortalama_sapma_pts + self.risk_point_object.devir_gunu_pts + \
                 self.risk_point_object.iade_pts + self.risk_point_object.kar_pts

        return toplam

    def analyze_all(self):
        # todo: logging
        self.detect_son_12ay_iade_yuzdesi()  # true -> analiz yapilir, false -> yapilmaz. default -> true.

        # eger yukaridaki False dondururse hesaplama yapilmaz?<
        if self.analyze_decision:
            self.detect_son_12ay_satis_ort_sapma()
            self.analyze_kar()
            self.analyze_son_12_ay_iade()
            self.analyze_ort_gecikme_gun_sayisi()
            self.analyze_ort_gecikme_gun_bakiyesi()
            self.analyze_devir_gunu()
            self.detect_teminat_limit_riskini_karsilama_seviyesi()

            try:
                toplam_pts = self.total_customer_point()
            except Exception:
                pass

            return self.analyzed_data

        else:
            # todo: logging
            return False
