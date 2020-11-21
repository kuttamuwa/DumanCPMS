from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from bootstrap_modal_forms.forms import BSModalModelForm, BSModalForm
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
from .models import Domains


class DomainFilterForm(BSModalForm):
    name = forms.CharField(max_length=100)

    class Meta:
        fields = ['name']


class DomainModalForm(BSModalModelForm):
    name = forms.CharField(max_length=100)
    point = forms.FloatField(max_value=100.0, min_value=0.0)  # todo: validators

    class Meta:
        fields = '__all__'
        model = Domains
