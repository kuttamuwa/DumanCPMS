from bootstrap_modal_forms.forms import BSModalModelForm, BSModalForm
from django import forms

from .models import Domains, Subtypes


def subtypes_point_sum_exceeds_100(value, domain):
    if sum([Subtypes.objects.get(domain=domain).pts].append(value)) > 100:
        raise ValueError(f"Summary of subtype points cannot be exceed 100 for {domain} domain")


def domains_point_sum_exceeds_100(value):
    if sum([d.point for d in Domains.objects.all()] + [value]) > 100:
        raise ValueError("Summary of domain points cannot be exceed 100")


class DomainFilterForm(BSModalForm):
    name = forms.CharField(max_length=100)

    class Meta:
        model = Domains
        fields = ['name']


class DomainModalForm(BSModalModelForm):
    name = forms.CharField(max_length=100)
    point = forms.FloatField(max_value=100.0, min_value=0.0,
                             validators=[domains_point_sum_exceeds_100])  # todo: validators

    class Meta:
        exclude = ['created_by']
        model = Domains


class SubtypeModalForm(BSModalModelForm):
    domain = forms.ModelChoiceField(queryset=Domains.objects.all(),
                                    help_text='Subtype is sub choicable value '
                                              'under domains')
    pts = forms.FloatField(min_value=0.0, max_value=100.0, help_text='Point between intervals')
    min_interval = forms.FloatField(help_text='Minimum interval')

    max_interval = forms.FloatField(help_text='Maximum interval')

    class Meta:
        model = Subtypes
        fields = ['domain', 'pts', 'min_interval', 'max_interval']


class SubtypeFilterForm(BSModalForm):
    domain = forms.ModelChoiceField(queryset=Domains.objects.all(),
                                    help_text='Subtype is sub choicable value '
                                              'under domains')

    class Meta:
        fields = ['domain']
