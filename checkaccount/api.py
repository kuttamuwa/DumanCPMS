from rest_framework import viewsets

from checkaccount.models import CheckAccount, AccountDocuments, PartnershipDocuments, SysPersonnel, Sectors
from checkaccount.serializers import CheckAccountSerializer, AccountDocumentsSerializer, PartnershipDocumentsSerializer
from checkaccount.serializers import SysPersonnelSerializer, SectorsSerializer


class CheckAccountAPI(viewsets.ModelViewSet):
    queryset = CheckAccount.objects.all().order_by('-created_date')
    serializer_class = CheckAccountSerializer


class AccountDocumentsAPI(viewsets.ModelViewSet):
    queryset = AccountDocuments.objects.all().order_by('-created_date')
    serializer_class = AccountDocumentsSerializer


class PartnershipDocumentsAPI(viewsets.ModelViewSet):
    queryset = PartnershipDocuments.objects.all().order_by('-created_date')
    serializer_class = PartnershipDocumentsSerializer


class SysPersonnelAPI(viewsets.ModelViewSet):
    queryset = SysPersonnel.objects.all().order_by('-created_date')
    serializer_class = SysPersonnelSerializer


class SectorsAPI(viewsets.ModelViewSet):
    queryset = Sectors.objects.all().order_by('-created_date')
    serializer_class = SectorsSerializer


