from bootstrap_modal_forms.generic import BSModalFormView, BSModalCreateView, BSModalUpdateView, BSModalReadView, \
    BSModalDeleteView
from django.db.models import ProtectedError
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import generic

from appconfig.forms import DomainFilterForm, DomainModalForm, SubtypeFilterForm, SubtypeModalForm
from appconfig.models import Domains, Subtypes


# indexes, main pages
def all_indexes(request):
    return render(request, 'appconfig/index.html',
                  context={'domains': Domains.objects.all(),
                           'subtypes': Subtypes.objects.all()})


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


# Domains
class DomainFilterView(BSModalFormView):
    template_name = 'appconfig/domaindirs/filter_domain.html'
    form_class = DomainFilterForm

    def form_valid(self, form):
        if 'clear' in self.request.POST:
            self.filter = ''
        else:
            self.filter = '?type=' + form.cleaned_data['type']

        response = super().form_valid(form)
        return response

    def get_success_url(self):
        return reverse_lazy('index') + self.filter


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


# Subtypes
class SubtypeFilterView(BSModalFormView):
    template_name = 'appconfig/subtypedirs/filter_subtype.html'
    form_class = SubtypeFilterForm

    def form_valid(self, form):
        if 'clear' in self.request.POST:
            self.filter = ''
        else:
            self.filter = '?type=' + form.cleaned_data['type']

        response = super().form_valid(form)
        return response

    def get_success_url(self):
        return reverse_lazy('app-index') + self.filter


class SubtypeCreateView(BSModalCreateView):
    template_name = 'appconfig/subtypedirs/create_subtype.html'
    form_class = SubtypeModalForm
    success_message = 'Success: Subtype was created.'
    success_url = reverse_lazy('app-index')

    # def get(self, request, *args, **kwargs):
    #     return super(SubtypeCreateView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        return super(SubtypeCreateView, self).form_valid(form)


class SubtypeUpdateView(BSModalUpdateView):
    model = Subtypes
    template_name = 'appconfig/subtypedirs/update_subtype.html'
    form_class = SubtypeModalForm
    success_message = 'Success: Subtype was updated.'
    success_url = reverse_lazy('app-index')

    def form_valid(self, form):
        return super(SubtypeUpdateView, self).form_valid(form)


class SubtypeReadView(BSModalReadView):
    model = Subtypes
    template_name = 'appconfig/subtypedirs/read_subtype.html'


class SubtypeDeleteView(BSModalDeleteView):
    model = Subtypes
    template_name = 'appconfig/subtypedirs/delete_subtype.html'
    success_message = 'Success: Subtype was deleted.'
    success_url = reverse_lazy('app-index')


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
