from crispy_forms.tests.forms import forms
from django.contrib.auth.models import User

from checkaccount.models import CheckAccount


class CheckAccountCreateForm(forms.ModelForm):
    class Meta:
        model = CheckAccount
        fields = '__all__'


class LoginUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()
