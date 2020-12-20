from django import forms

from externalapp.models import ExternalBlackList, SystemBlackList, KonkordatoList, TaxDebtList, SGKDebtListModel


class ExternalBlackListImportDataForm(forms.ModelForm):
    dataFile = forms.FileField(
        label='Select your data excel file',
        help_text='Does your data have all columns that we need? \n'
                  'Please consult on this page: ',

    )

    class Meta:
        model = ExternalBlackList
        fields = ()
        
        
class SystemBlackListImportDataForm(forms.ModelForm):
    dataFile = forms.FileField(
        label='Select your data excel file',
        help_text='Does your data have all columns that we need? \n'
                  'Please consult on this page: ',

    )

    class Meta:
        model = SystemBlackList
        fields = ()
        

class KonkordatoListImportDataForm(forms.ModelForm):
    dataFile = forms.FileField(
        label='Select your data excel file',
        help_text='Does your data have all columns that we need? \n'
                  'Please consult on this page: ',

    )

    class Meta:
        model = KonkordatoList
        fields = ()


class TaxDebtListImportDataForm(forms.ModelForm):
    dataFile = forms.FileField(
        label='Select your data excel file',
        help_text='Does your data have all columns that we need? \n'
                  'Please consult on this page: ',

    )

    class Meta:
        model = TaxDebtList
        fields = ()


class SGKDebtListImportDataForm(forms.ModelForm):
    dataFile = forms.FileField(
        label='Select your data excel file',
        help_text='Does your data have all columns that we need? \n'
                  'Please consult on this page: ',

    )

    class Meta:
        model = SGKDebtListModel
        fields = ()