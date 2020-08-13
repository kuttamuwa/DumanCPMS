from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Column, Row, Fieldset, ButtonHolder
from crispy_forms.tests.forms import forms

from checkaccount.model_sys_specs import CariHesapSpecs
from checkaccount.models import CheckAccount


class CheckAccountForm(forms.ModelForm):
    class Meta:
        model = CheckAccount
        fields = '__all__'


class SearchCheckAccountForm(forms.Form):
    firm_full_name = forms.ModelChoiceField(label="Firm Full Name", queryset=CheckAccount.objects.all(),
                                            widget=forms.Select(attrs={'class': 'form-control input-sm'}))
    city = forms.ModelChoiceField(label='City', queryset=CheckAccount.objects.all(),
                                  widget=forms.Select(attrs={'class': 'form-control input-sm'}))
