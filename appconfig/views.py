from bootstrap_modal_forms.generic import BSModalFormView, BSModalCreateView, BSModalUpdateView, BSModalReadView, \
    BSModalDeleteView
from django.db.models import ProtectedError
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import generic

from appconfig.forms import DomainFilterForm, DomainModalForm, SubtypeFilterForm, SubtypeModalForm, \
    RiskConfigFilterForm, RiskConfigModalForm
from appconfig.models import Domains, Subtypes, RiskDataConfigModel


# All Indexes
class Index(generic.ListView):
    template_name = 'appconfig/index.html'
    model = [Domains, Subtypes, RiskDataConfigModel]

    def get_queryset(self):
        qs = super().get_queryset()
        return qs

    def get(self, request, *args, **kwargs):
        context = {'domains': Domains.objects.all(),
                   'subtypes': Subtypes.objects.all(),
                   'riskconfigs': RiskDataConfigModel.objects.all()}
        get_req = request.GET

        if get_req:
            domain_name = get_req.get('domain_name')
            sub_domain = get_req.get('sub_domain')
            source_field = get_req.get('source_field')

            if domain_name is not None:
                context['domains'] = Domains.objects.filter(pk=domain_name)

            if sub_domain is not None:
                context['subtypes'] = Subtypes.objects.filter(domain_id=sub_domain)

            if source_field is not None:
                context['riskconfigs'] = RiskDataConfigModel.objects.filter(source_field=source_field)

        return render(request, 'appconfig/index.html', context=context)


class SubtypeIndex(generic.ListView):
    model = Subtypes
    context_object_name = 'subtypes'
    template_name = 'appconfig/subtypedirs/subtype_index.html'

    def get_queryset(self):
        qs = super().get_queryset()
        if 'type' in self.request.GET:
            qs = qs.filter(domain_name=str(self.request.GET['domain_name']))
        return qs


class DomainIndex(generic.ListView):
    model = Domains
    context_object_name = 'domains'
    template_name = 'appconfig/domaindirs/domain_index.html'

    def get_queryset(self):
        qs = super().get_queryset()
        if 'domain_name' in self.request.GET:
            qs = qs.filter(domain_name=str(self.request.GET['domain_name']))
        return qs


class RiskDataIndex(generic.ListView):
    model = RiskDataConfigModel
    context_object_name = 'riskconfigs'
    template_name = 'appconfig/riskdata/riskdataset_index.html'

    def get_queryset(self):
        qs = super().get_queryset()

        return qs


# Domains
class DomainFilterView(BSModalFormView):
    template_name = 'appconfig/domaindirs/filter_domain.html'
    form_class = DomainFilterForm

    def form_valid(self, form):
        if 'clear' in self.request.POST:
            self.filter = ''
        else:
            self.filter = '?domain_name=' + str(form.cleaned_data['domain_name'].pk)

        response = super().form_valid(form)
        return response

    def get_success_url(self):
        return reverse_lazy('app-index') + self.filter


class DomainCreateView(BSModalCreateView):
    template_name = 'appconfig/domaindirs/create_domain.html'
    form_class = DomainModalForm
    success_message = 'Success: Domain was created.'
    success_url = reverse_lazy('app-index')

    def form_valid(self, form):
        return super(DomainCreateView, self).form_valid(form)


class DomainUpdateView(BSModalUpdateView):
    model = Domains
    template_name = 'appconfig/domaindirs/update_domain.html'
    form_class = DomainModalForm
    success_message = 'Success: Domain was updated.'
    success_url = reverse_lazy('app-index')

    def form_valid(self, form):
        return super(DomainUpdateView, self).form_valid(form)


class DomainReadView(BSModalReadView):
    model = Domains
    template_name = 'appconfig/domaindirs/read_domain.html'


class DomainDeleteView(BSModalDeleteView):
    model = Domains
    template_name = 'appconfig/domaindirs/delete_domain.html'
    success_message = 'Success: Domain was deleted.'
    success_url = reverse_lazy('app-index')

    def post(self, request, *args, **kwargs):
        return super(DomainDeleteView, self).post(request, *args, **kwargs)


# Subtypes
class SubtypeFilterView(BSModalFormView):
    template_name = 'appconfig/subtypedirs/filter_subtype.html'
    form_class = SubtypeFilterForm

    def form_valid(self, form):
        if 'clear' in self.request.POST:
            self.filter = ''
        else:
            self.filter = '?sub_domain=' + str(form.cleaned_data['sub_domain'].pk)

        response = super().form_valid(form)
        return response

    def get_success_url(self):
        return reverse_lazy('app-index') + self.filter


class RiskConfigFilterView(BSModalFormView):
    template_name = 'appconfig/riskdata/filter_rdfield.html'
    form_class = RiskConfigFilterForm

    def form_valid(self, form):
        response = super().form_valid(form)
        return response

    def get_success_url(self):
        return reverse_lazy('app-index')


class SubtypeCreateView(BSModalCreateView):
    template_name = 'appconfig/subtypedirs/create_subtype.html'
    form_class = SubtypeModalForm
    success_message = 'Success: Subtype was created.'
    success_url = reverse_lazy('app-index')

    def form_valid(self, form):
        return super(SubtypeCreateView, self).form_valid(form)


class RiskConfigCreateView(BSModalCreateView):
    template_name = 'appconfig/riskdata/create_rdfield.html'
    form_class = RiskConfigModalForm
    success_message = 'Success: Risk Data Config was created.'
    success_url = reverse_lazy('app-index')

    def form_valid(self, form):
        return super(RiskConfigCreateView, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        return super(RiskConfigCreateView, self).get(request, *args, **kwargs)


class SubtypeUpdateView(BSModalUpdateView):
    model = Subtypes
    template_name = 'appconfig/subtypedirs/update_subtype.html'
    form_class = SubtypeModalForm
    success_message = 'Success: Subtype was updated.'
    success_url = reverse_lazy('app-index')

    def form_valid(self, form):
        return super(SubtypeUpdateView, self).form_valid(form)


class RiskConfigUpdateView(BSModalUpdateView):
    model = RiskDataConfigModel
    template_name = 'appconfig/riskdata/update_rdfield.html'
    form_class = RiskConfigModalForm
    success_message = 'Success: Risk Config was updated.'
    success_url = reverse_lazy('app-index')

    def form_valid(self, form):
        return super(RiskConfigUpdateView, self).form_valid(form)


class SubtypeReadView(BSModalReadView):
    model = Subtypes
    template_name = 'appconfig/subtypedirs/read_subtype.html'


class RiskConfigReadView(BSModalReadView):
    model = RiskDataConfigModel
    template_name = 'appconfig/riskdata/read_rdfield.html'


class SubtypeDeleteView(BSModalDeleteView):
    model = Subtypes
    template_name = 'appconfig/subtypedirs/delete_subtype.html'
    success_message = 'Success: Subtype was deleted.'
    success_url = reverse_lazy('app-index')


class RiskConfigDeleteView(BSModalDeleteView):
    model = RiskDataConfigModel
    template_name = 'appconfig/riskdata/delete_rdfield.html'
    success_message = 'Success: Risk Config object was deleted.'
    success_url = reverse_lazy('app-index')


def domains_list(request):
    data = dict()
    if request.method == 'GET':
        domains = Domains.objects.all()
        data['table'] = render_to_string(
            'appconfig/domaindirs/_domains_table.html',
            {'domains': domains},
            request=request
        )
        return JsonResponse(data)


def subtypes_list(request):
    data = dict()
    if request.method == 'GET':
        subtypes = Subtypes.objects.all()
        data['table'] = render_to_string(
            'appconfig/subtypedirs/_subtypes_table.html',
            {'subtypes': subtypes},
            request=request
        )
        return JsonResponse(data)


def riskconfigs_list(request):
    data = dict()
    if request.method == 'GET':
        riskconfigs = RiskDataConfigModel.objects.all()
        data['table'] = render_to_string(
            'appconfig/riskdata/_rdfields_table.html',
            {'riskconfigs': riskconfigs},
            request=request
        )
        return JsonResponse(data)
