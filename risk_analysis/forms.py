from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm
from django.forms import inlineformset_factory

from checkaccount.models import CheckAccount
from risk_analysis.models import DataSetModel, SGKDebtListModel, TaxDebtList
from risk_analysis.analyze_models import RiskDSAnalyze
from crispy_forms.tests.forms import forms
from django import forms as djforms


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


class TAXImportDataForm(forms.ModelForm):
    taxDataFile = forms.FileField(
        label='Select your data excel file',
        help_text='Does your data have all columns that we need? \n'
                  'Please consult on this page: ',
    )

    class Meta:
        model = TaxDebtList
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
    customer = forms.ModelChoiceField(queryset=CheckAccount.objects.all())
    analyze_now = forms.BooleanField(required=False, label='Analyze now', initial=True)

    def save(self, commit=True):
        super(RiskAnalysisImportDataForm, self).save()

    class Meta:
        model = DataSetModel
        fields = ['riskDataFile', 'customer']


class RiskDSAnalyzeForm(BSModalForm):
    risk_ds_analyze = forms.ModelChoiceField(queryset=RiskDSAnalyze.objects.all(),
                                             help_text='Analyzed of risk dataset objects')

    class Meta:
        fields = ['risk_ds_analyze']