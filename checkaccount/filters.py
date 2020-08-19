from django_filters import FilterSet

from checkaccount.models import CheckAccount


class CheckAccountFilter(FilterSet):
    class Meta:
        model = CheckAccount
        fields = {
            'firm_type': ['exact']
        }
        # fields = (
        #     'firm_type', 'firm_full_name', 'taxpayer_number', 'firm_key_contact_personnel', 'representative_person',
        #     'customer_id')
