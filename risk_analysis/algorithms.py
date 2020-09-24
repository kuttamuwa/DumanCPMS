from risk_analysis.models import DataSetModel


class ControlRiskDataSet:
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def control_columns(self):
        riskdataset_columns = DataSetModel._meta.fields
        for c in riskdataset_columns:
            if c not in self.dataframe.columns:
                # todo: logging
                print("")

    def control_data(self):
        pass


class AnalyzingRiskDataSet:
    """
    It also converts bulk data into categorized data
    """
    def __init__(self, control_object, analyze_right_now=True):
        self.control_object = control_object
        self.get_analyzed_data = None

        if analyze_right_now:
            self.analyze_all()

    def detect_son_12ay_satis_ort_sapma(self):
        """
        %0-20 azalış	3
        %20-50 azalış	5
        %50-75 azalış	10

        """

        pass

    def analyze_kar(self):
        """
        %0-5	15
        %5-10	10
        %10-15	7
        %15-20	5
        %20 ve üzeri	3

        """
        pass

    def analyze_iade(self):
        """
        %0-20 	3
        %20-50 	5
        %50-75 	10
        %75 üzeri 	15

        """
        pass

    def analyze_ort_gecikme_gun_sayisi(self):
        """
        10 gün	5
        20 gün	10
        30 gün ve üzeri	15

        """
        pass

    def analyze_ort_gecikme_gun_bakiyesi(self):
        """
        0-50000	5
        50000-100000	8
        100000 ve üzeri	10

        """
        pass

    def analyze_devir_gunu(self):
        """
        0-15	5
        15-30	10
        30 ve üzeri	15

        """
        pass

    def detect_teminat_limit_riskini_karsilama_seviyesi(self):
        """
        %0-20 	15
        %20-50 	10
        %50-75 	5
        %75 üzeri 	3

        """
        pass

    def bulk_to_dataframe(self):
        return self.get_analyzed_data

    def analyze_all(self):
        # todo: logging
        self.detect_son_12ay_satis_ort_sapma()
        self.analyze_kar()
        self.analyze_iade()
        self.analyze_ort_gecikme_gun_sayisi()
        self.analyze_ort_gecikme_gun_bakiyesi()
        self.analyze_devir_gunu()
        self.detect_teminat_limit_riskini_karsilama_seviyesi()



