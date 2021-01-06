from bootstrap_modal_forms.forms import BSModalForm
from crispy_forms.tests.forms import forms

# from checkaccount.models import CheckAccount
from risk_analysis.models import DataSetModel
from risk_analysis.usermodel import UserAdaptor


class RiskAnalysisCreateForm(forms.ModelForm):
    class Meta:
        model = DataSetModel
        exclude = (
            'created_by', 'created_date', 'customer', 'analyzed_pts'
        )

    def __init__(self, *args, **kwargs):
        super(RiskAnalysisCreateForm, self).__init__(*args, **kwargs)


class RiskAnalysisImportDataForm(forms.ModelForm):
    riskDataFile = forms.FileField(
        label='Select your data excel file',
        help_text='Does your data have all columns that we need? \n'
                  'Please consult on this page: ',

    )

    class Meta:
        model = DataSetModel
        fields = ()


class RiskAnalysisRetrieveForm(BSModalForm):
    related_customer = forms.ModelChoiceField(queryset=UserAdaptor.objects.all(),
                                              required=False)

    class Meta:
        fields = ['customer']

