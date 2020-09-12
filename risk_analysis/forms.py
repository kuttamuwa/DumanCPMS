from checkaccount.models import CheckAccount
from risk_analysis.models import DataSetModel
from crispy_forms.tests.forms import forms


class RiskAnalysisImportDataForm(forms.ModelForm):
    riskDataFile = forms.FileField(
        label='Select your data excel file',
        help_text='Does your data have all columns that we need?',

    )
    customer = forms.ModelChoiceField(queryset=CheckAccount.objects.all())

    class Meta:
        model = DataSetModel
        fields = ()


class RiskAnalysisCreateForm(forms.ModelForm):
    class Meta:
        model = DataSetModel
        fields = '__all__'
