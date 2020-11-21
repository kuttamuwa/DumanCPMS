from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from bootstrap_modal_forms.forms import BSModalModelForm, BSModalForm
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
from .models import Domains, Subtypes


class DomainFilterForm(BSModalForm):
    name = forms.CharField(max_length=100)

    class Meta:
        fields = ['name']


class DomainModalForm(BSModalModelForm):
    name = forms.CharField(max_length=100)
    point = forms.FloatField(max_value=100.0, min_value=0.0)  # todo: validators

    class Meta:
        exclude = ['created_by']
        model = Domains


class SubtypeModalForm(BSModalModelForm):
    domain_name = forms.ChoiceField(choices=Domains.objects.all(), help_text='Subtype is sub choicable value'
                                                                             ' under domains')
    subpoint = forms.FloatField(min_value=0.0, max_value=100.0, help_text='Point between intervals')
    min_interval = forms.FloatField(max_value=100, min_value=0.0, help_text='Minimum interval')

    max_interval = forms.FloatField(max_value=100, min_value=0.0, help_text='Maximum interval')

    class Meta:
        model = Subtypes
        fields = '__all__'


class SubtypeFilterForm(BSModalForm):
    name = forms.CharField(max_length=100)

    class Meta:
        fields = ['name']
