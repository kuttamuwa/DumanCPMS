from rest_framework import viewsets

from checkaccount.models import CheckAccount, AccountDocuments, PartnershipDocuments, SysPersonnel, Sectors, Cities, \
    Districts
from checkaccount.serializers import CheckAccountSerializer, AccountDocumentsSerializer, PartnershipDocumentsSerializer
from checkaccount.serializers import SysPersonnelSerializer, SectorsSerializer, CitySerializer, DistrictSerializer


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


class CitiesAPI(viewsets.ModelViewSet):
    queryset = Cities.objects.all().order_by('name')
    serializer_class = CitySerializer


class DistrictAPI(viewsets.ModelViewSet):
    queryset = Districts.objects.all()
    serializer_class = DistrictSerializer

    def get_queryset(self):
        city_pk = self.request.query_params.get('city_pk')
        city = Cities.objects.filter(pk=city_pk)

        return city
