from risk_analysis.models import DataSetModel


class DataSetModelDTO:
    @classmethod
    def from_row(cls, row):
        DataSetModel(
            *row
        )