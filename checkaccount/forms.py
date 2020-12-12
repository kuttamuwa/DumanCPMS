from crispy_forms.tests.forms import forms
from django.contrib.auth.models import User
from django.forms import FileField

from checkaccount.fields import DumanModelFileField, DumanFormFileField
from checkaccount.models import CheckAccount, AccountDocuments


class CheckAccountCreateForm(forms.ModelForm):
    class Meta:
        model = CheckAccount
        exclude = ('Created by',)

    def __init__(self, *args, **kwargs):
        # self.base_fields['Created by'].disabled = True
        super(CheckAccountCreateForm, self).__init__(*args, **kwargs)


class LoginUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')


class UploadAccountDocumentForm(forms.ModelForm):
    # activity_certificate_pdf = FileField(label='Activity Certificate', required=False, allow_empty_file=True)
    # tax_return_pdf = FileField(label='TAX Return', required=False, allow_empty_file=True)
    # authorized_signatures_list_pdf = FileField(label='Authorized Signatures List', required=False,
    #                                            allow_empty_file=True)

    class Meta:
        model = AccountDocuments
        exclude = ('customer', 'Created by')

