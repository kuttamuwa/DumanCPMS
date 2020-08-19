from crispy_forms.tests.forms import forms
from django.contrib.auth.models import User

from checkaccount.models import CheckAccount


class CheckAccountCreateForm(forms.ModelForm):
    class Meta:
        model = CheckAccount
        fields = '__all__'
        # fields = ['firm_type', 'firm_full_name', 'taxpayer_number', 'birthplace', 'tax_department',
        #           'firm_address', 'firm_key_contact_personnel', 'sector', 'city', 'district',
        #           'phone_number', 'fax', 'web_url', 'email_addr', 'representative_person']
        # labels = {
        #     'taxpayer_number': 'Mükellef numarası',
        # }
        # help_texts = {'taxpayer_number': 'Sahis firmasi ise TCKNO, Tuzel Kisilik ise Vergi No'}
        # error_messages = {'taxpayer_number': 'Tax payer field cannot be more than 15 characters'}


class LoginUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')

