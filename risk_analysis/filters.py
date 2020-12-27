from django_filters import FilterSet

from risk_analysis.models import DataSetModel, RiskDataSetPoints


class RiskAnalysisFilter(FilterSet):
    class Meta:
        model = DataSetModel
        fields = ('customer',)


class RiskPointsFilter(FilterSet):
    class Meta:
        model = RiskDataSetPoints
        fields = ('risk_dataset', 'variable', )
