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
        fields = ('customer',)


class SGKDataFilter(FilterSet):
    class Meta:
        model = SGKDebtListModel
        fields = ('taxpayer_number', 'firm_title')


class TaxDataFilter(FilterSet):
    class Meta:
        model = TaxDebtList
        fields = ('tax_department', 'taxpayer_number', 'dept_title', 'real_operating_income',
                  'dept_amount')
