import django_filters
from django_filters import FilterSet

from checkaccount.models import CheckAccount


class CheckAccountFilter(FilterSet):
    firm_full_name = django_filters.CharFilter(lookup_expr='icontains', label='Firm full name')
    taxpayer_number = django_filters.NumberFilter(lookup_expr='icontains', label='Tax payer number')

    class Meta:
        model = CheckAccount
        fields = ('firm_full_name', 'taxpayer_number')

    #     # fields = {
    #     #     'firm_type': ['exact'],
    #     #     'firm_key_contact_personnel'
    #     # }
    #     fields = (
    #         'firm_type', 'firm_full_name', 'taxpayer_number', 'firm_key_contact_personnel', 'representative_person',
    #         'customer_id')
