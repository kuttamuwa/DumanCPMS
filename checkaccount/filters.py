from django_filters import FilterSet

from checkaccount.models import CheckAccount


class CheckAccountFilter(FilterSet):
    class Meta:
        model = CheckAccount
        fields = '__all__'
