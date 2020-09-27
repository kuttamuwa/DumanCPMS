from crispy_forms.tests.forms import forms
from django.contrib.auth.models import User

from checkaccount.models import CheckAccount, AccountDocuments, SGKDebtList


class CheckAccountCreateForm(forms.ModelForm):
    class Meta:
        model = CheckAccount
        fields = '__all__'


class LoginUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')


class UploadSGKDatasetForm(forms.ModelForm):
    class Meta:
        model = SGKDebtList
        fields = '__all__'


class UploadAccountDocumentForm(forms.ModelForm):
    class Meta:
        model = AccountDocuments
        fields = ('activity_certificate_pdf', 'tax_return_pdf', 'authorized_signatures_list_pdf',
                  'description')
