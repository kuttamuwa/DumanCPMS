import django_filters
from django_filters import FilterSet

from checkaccount.models import CheckAccount
from risk_analysis.models import DataSetModel, RiskDataSetPoints, SGKDebtListModel, TaxDebtList, DomainPts


class RiskAnalysisFilter(FilterSet):
    firm_full_name = django_filters.CharFilter(lookup_expr='icontains', label='Firm full name')

    # taxpayer_number = django_filters.NumberFilter(lookup_expr='icontains', label='Tax payer number')

    class Meta:
        model = DataSetModel
        fields = ('related_customer',)

    #     # fields = {
    #     #     'firm_type': ['exact'],
    #     #     'firm_key_contact_personnel'
    #     # }
    #     fields = (
    #         'firm_type', 'firm_full_name', 'taxpayer_number', 'firm_key_contact_personnel', 'representative_person',
    #         'customer_id')


class DomainPointsFilter(FilterSet):
    domain = django_filters.ChoiceFilter(choices=DataSetModel.get_domain_list())
    # pts = django_filters.(max_value=100.0)

    class Meta:
        model = DomainPts
        fields = ()


class RiskPointsFilter(FilterSet):
    # customer_id = django_filters.CharFilter(lookup_expr='icontains', label='Customer')

    class Meta:
        model = RiskDataSetPoints
        fields = ('customer_id',)


class SGKDataFilter(FilterSet):
    class Meta:
        model = SGKDebtListModel
        fields = ('taxpayer_number', 'firm_title')


class TaxDataFilter(FilterSet):
    class Meta:
        model = TaxDebtList
        fields = ('tax_department', 'taxpayer_number', 'dept_title', 'real_operating_income',
                  'dept_amount')
