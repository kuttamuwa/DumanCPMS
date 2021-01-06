from rest_framework import serializers
from .models import DataSetModel


class RiskAnalysisDatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSetModel
        fields = '__all__'


