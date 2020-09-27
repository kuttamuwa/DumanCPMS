from checkaccount.models import CheckAccount
from risk_analysis.models import DataSetModel, SGKDebtListModel
from crispy_forms.tests.forms import forms


class SGKImportDataForm(forms.ModelForm):
    sgkDataFile = forms.FileField(
        label='Select your data excel file',
        help_text='Does your data have all columns that we need? \n'
                  'Please consult on this page: ',

    )
    # todo: şu help_text'in oraya sütunlara bakabileceği bir yer vermek lazım

    class Meta:
        model = SGKDebtListModel
        fields = ()


class RiskAnalysisCreateForm(forms.ModelForm):
    class Meta:
        model = DataSetModel
        fields = '__all__'


class RiskAnalysisImportDataForm(forms.ModelForm):
    riskDataFile = forms.FileField(
        label='Select your data excel file',
        help_text='Does your data have all columns that we need? \n'
                  'Please consult on this page: ',

    )
    # todo: şu help_text'in oraya sütunlara bakabileceği bir yer vermek lazım

    customer = forms.ModelChoiceField(queryset=CheckAccount.objects.all())

    class Meta:
        model = DataSetModel
        fields = ()

