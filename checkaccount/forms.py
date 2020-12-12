from crispy_forms.tests.forms import forms
from django.contrib.auth.models import User

from checkaccount.fields import DumanFormFileField
from checkaccount.models import CheckAccount, AccountDocuments


class CheckAccountCreateForm(forms.ModelForm):
    class Meta:
        model = CheckAccount
        fields = '__all__'


class LoginUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')


class UploadAccountDocumentForm(forms.ModelForm):
    activity_certificate_pdf = DumanFormFileField(label='Activity Certificate', required=False, allow_empty_file=True)
    tax_return_pdf = DumanFormFileField(label='TAX Return', required=False, allow_empty_file=True)
    authorized_signatures_list_pdf = DumanFormFileField(label='Authorized Signatures List', required=False,
                                                        allow_empty_file=True)

    class Meta:
        model = AccountDocuments
        exclude = ('customer',)