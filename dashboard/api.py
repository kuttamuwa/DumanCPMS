from rest_framework import viewsets

from checkaccount.serializers import CheckAccountSerializer
from risk_analysis.models import DataSetModel
from risk_analysis.serializer import RiskAnalysisDatasetSerializer

try:
    from checkaccount.models import CheckAccount

    account = CheckAccount
    accountserializer = CheckAccountSerializer

except ImportError:
    from risk_analysis.basemodels import DummyUser, DummySerializer

    account = DummyUser
    accountserializer = DummySerializer


class CheckAccountAPI(viewsets.ModelViewSet):
    queryset = account.objects.all().order_by('-created_date')
    serializer_class = accountserializer


class RiskAnalysisAPI(viewsets.ModelViewSet):
    queryset = DataSetModel.objects.all().order_by('-created_date')
    serializer_class = RiskAnalysisDatasetSerializer

