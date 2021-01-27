from rest_framework import serializers
from .models import CheckAccount, AccountDocuments, PartnershipDocuments, SysPersonnel, Sectors, Cities, Districts


class CheckAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckAccount
        fields = '__all__'


class AccountDocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountDocuments
        fields = '__all__'


class PartnershipDocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartnershipDocuments
        fields = '__all__'


class SysPersonnelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SysPersonnel
        fields = '__all__'


class SectorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sectors
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Cities
        fields = '__all__'


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = Districts
        fields = '__all__'
