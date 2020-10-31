from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm
from django.forms import inlineformset_factory

from checkaccount.models import CheckAccount
from risk_analysis.models import DataSetModel, SGKDebtListModel, TaxDebtList, Subtypes, Domains
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
    # todo: şu help_text'in oraya sütunlara bakabileceği bir yer vermek lazım

    customer = forms.ModelChoiceField(queryset=CheckAccount.objects.all())

    class Meta:
        model = DataSetModel
        fields = ()


# DomainCreateFormInlineSet = inlineformset_factory(Domains, DomainPts, form=DomainCreateForm, extra=1,
#                                                   can_delete=True, fk_name='domain_name')

class DomainCreateForm(djforms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DomainCreateForm, self).__init__(*args, **kwargs)
        # add a "form-control" class to each form input
        # for enabling bootstrap

        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })

    class Meta:
        model = Domains
        fields = '__all__'

    def is_valid(self):
        # do something
        super(DomainCreateForm, self).is_valid()


class DomainsModalForm(BSModalModelForm):
    class Meta:
        model = Domains
        fields = '__all__'


class DomainsFilterModalForm(BSModalForm):
    class Meta:
        fields = '__all__'


class SubtypeCreateForm(forms.ModelForm):
    class Meta:
        model = Subtypes
        fields = '__all__'

    def is_valid(self):
        # do something
        super(SubtypeCreateForm, self).is_valid()
