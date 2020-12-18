import django_filters
from django_filters import FilterSet

from risk_analysis.models import DataSetModel, RiskDataSetPoints, SGKDebtListModel, TaxDebtList


class RiskAnalysisFilter(FilterSet):
    firm_full_name = django_filters.CharFilter(lookup_expr='icontains', label='Firm full name')

    class Meta:
        model = DataSetModel
        fields = ('related_customer',)


class RiskPointsFilter(FilterSet):
    class Meta:
        model = RiskDataSetPoints
        fields = ('customer_id',)
