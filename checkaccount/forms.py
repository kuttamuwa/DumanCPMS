from bootstrap_modal_forms import forms as bsforms
from crispy_forms.tests.forms import forms
from dal import autocomplete
from django.contrib.auth.models import User

from checkaccount.models import CheckAccount, AccountDocuments, Districts, Cities, Sectors, SysPersonnel


class CheckAccountCreateForm(forms.ModelForm):
    class Meta:
        model = CheckAccount
        exclude = ('Created by',
                   # 'city', 'district'
                   )

    def __init__(self, *args, **kwargs):
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


# DEV
class CheckAccountCreateFormExplicit(bsforms.BSModalModelForm):
    firm_type = forms.ChoiceField(choices=(('t', 'TUZEL_KISILIK'), ('s', 'SAHIS_ISLETMESI')),
                                  help_text='Business type of the firm')
    firm_full_name = forms.CharField(max_length=70, help_text='Firm Fullname', required=False)
    taxpayer_number = forms.CharField(
        help_text='Sahis firmasi ise TCKNO, Tuzel Kisilik ise Vergi No', max_length=15, required=False)

    # validators cannot be used
    birthplace = forms.ModelChoiceField(queryset=Cities.objects.all(), empty_label='İl',
                                        required=False, help_text='Şahıs firmaları için doğum yeri')
    tax_department = forms.CharField(max_length=100, help_text='Tax Department', required=False)
    firm_address = forms.CharField(max_length=200, help_text='Firm address', required=False)

    firm_key_contact_personnel = forms.ModelChoiceField(queryset=SysPersonnel.objects.all(),
                                                        help_text='Firma İletişim Kişisi', required=False)
    sector = forms.ModelChoiceField(queryset=Sectors.objects.all(), help_text='Sektör seçiniz', required=False)

    city = forms.ModelChoiceField(queryset=Cities.objects.all(), required=False)  # if city | district goes?
    district = forms.ModelChoiceField(queryset=Districts.objects.all(), required=False)

    phone_number = forms.CharField(max_length=15, help_text='Telefon numarası', required=False)
    fax = forms.CharField(max_length=15, required=False)
    web_url = forms.URLField(help_text='Web adresi', required=False)
    email_addr = forms.EmailField(help_text='Email adresi', required=False)
    representative_person = forms.ModelChoiceField(queryset=SysPersonnel.objects.all(), help_text='Temsilci seçiniz',
                                                   required=False)

    class Meta:
        model = CheckAccount
        fields = '__all__'
