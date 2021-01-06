from rest_framework import serializers
from .models import CheckAccount, AccountDocuments, PartnershipDocuments, SysPersonnel, Sectors


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
