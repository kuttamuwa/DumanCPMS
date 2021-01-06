from django.shortcuts import render
from django.views import View
from rest_framework import generics

from dashboard.api import account, accountserializer
from risk_analysis.models import DataSetModel
from risk_analysis.serializer import RiskAnalysisDatasetSerializer


class DashBoardView(View):
    template = 'dboards/customer_dash.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template)

    def post(self, request, *args, **kwargs):
        return render(request, self.template)


class AccountAPIListView(generics.ListCreateAPIView):
    queryset = account.objects.all().order_by('-created_date')
    serializer_class = accountserializer


class AccountDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = account.objects.all().order_by('-created_date')
    serializer_class = accountserializer


class RiskAnalysisAPIListView(generics.ListCreateAPIView):
    queryset = DataSetModel.objects.all().order_by('-created_date')
    serializer_class = RiskAnalysisDatasetSerializer


class RiskAnalysisAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DataSetModel.objects.all().order_by('-created_date')
    serializer_class = RiskAnalysisDatasetSerializer

