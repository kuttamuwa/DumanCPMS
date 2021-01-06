from rest_framework import serializers
from .models import CheckAccount


class CheckAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckAccount
        fields = '__all__'


