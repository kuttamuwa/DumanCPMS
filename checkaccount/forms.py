from bootstrap_modal_forms.forms import BSModalModelForm
from crispy_forms.tests.forms import forms

from checkaccount.models import CheckAccount, AccountDocuments


# Creating Check Account
class CheckAccountCreateForm(BSModalModelForm):
    class Meta:
        model = CheckAccount
        fields = '__all__'


# Uploading Files related to Check Account
class UploadAccountDocumentForm(forms.ModelForm):
    activity_certificate_pdf = forms.FilePathField(label='Activity Certificate', required=False, allow_empty_file=True)
    tax_return_pdf = forms.FilePathField(label='TAX Return', required=False, allow_empty_file=True)
    authorized_signatures_list_pdf = forms.FilePathField(label='Authorized Signatures List', required=False,
                                                         allow_empty_file=True)

    class Meta:
        model = AccountDocuments
        exclude = ('customer',)
