from bootstrap_modal_forms.forms import BSModalModelForm, BSModalForm
from django import forms

from .errors import SubtypePoints, DomainPoints
from .models import Domains, Subtypes


def subtypes_point_sum_exceeds_100(value, domain):
    if sum([Subtypes.objects.get(domain=domain).pts].append(value)) > 100:
        raise SubtypePoints(domain)


def domains_point_sum_exceeds_100(value):
    if sum([d.point for d in Domains.objects.all()] + [value]) > 100:
        raise DomainPoints


class DomainFilterForm(BSModalForm):
    domain_name = forms.ModelChoiceField(queryset=Domains.objects.all(), label='Domain Name',
                                         required=False)

    class Meta:
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
    subpoint = forms.FloatField(min_value=0.0, max_value=100.0, help_text='Point between intervals')
    min_interval = forms.FloatField(max_value=100, min_value=0.0, help_text='Minimum interval')

    max_interval = forms.FloatField(max_value=100, min_value=0.0, help_text='Maximum interval')

    def save(self, commit=True):
        # subtypes_point_sum_exceeds_100(self.subpoint, self.domain)
        super(SubtypeModalForm, self).save()

    class Meta:
        model = Subtypes
        fields = ['domain', 'subpoint', 'min_interval', 'max_interval']


class SubtypeFilterForm(BSModalForm):
    sub_domain = forms.ModelChoiceField(queryset=Domains.objects.all(), label='Domain', required=False)

    class Meta:
        fields = ['name']
