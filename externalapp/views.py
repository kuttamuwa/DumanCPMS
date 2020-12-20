import os

from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import FormView
import pandas as pd
from django_filters.views import FilterView

from DumanCPMS.settings import MEDIA_ROOT
from externalapp.forms import *
from risk_analysis.usermodel import UserAdaptor


def not_in_admin_group(user):
    if user.is_superuser:
        return True


@method_decorator(login_required(login_url='/login'), name='dispatch')
@method_decorator(user_passes_test(not_in_admin_group, login_url='/login'), name='dispatch')
class UploadExternalBlackListView(FormView):
    form_class = ExternalBlackListImportDataForm
    template_name = 'externalapp/import_form.html'

    @staticmethod
    def __nan_to_none(value):
        if pd.isna(value):
            value = None

        return value

    def get_success_url_primitive(self, request, customer):
        return render(request, template_name=self.succeeded_template,
                      context={'customer': customer})

    def get_success_url(self):
        # file uploading completed
        # referring document page
        return reverse_lazy('docs', kwargs=self.kwargs)

    def get_error_url(self, request, message):
        return render(request, template_name=self.error_template,
                      context={'error': message})

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context={'forms': self.form_class})

    @staticmethod
    def handle_with_customer(customer):
        if customer not in ("", None):
            try:
                customer = UserAdaptor.objects.get(firm_full_name=customer)

            except UserAdaptor.DoesNotExist:
                customer = UserAdaptor.objects.create(firm_full_name=customer)

        else:
            customer = UserAdaptor.dummy_creator.create_dummy()

        return customer

    def post(self, request, *args, **kwargs):
        data = request.FILES['riskDataFile']

        if not str(data.name).endswith('.xlsx'):
            return render(request, template_name='risk_analysis/error_pages/general_error.html',
                          context={'error': "Uploaded file must be xlsx file !"})

        p = default_storage.save(data.name, ContentFile(data.read()))

        # saving process
        p = os.path.join(MEDIA_ROOT, p)

        df = pd.read_excel(p)

        # Analyzing process
        for index, row in df.iterrows():
            print(row)

            kw = {}
            return redirect('get-riskds', **kw)


@method_decorator(login_required(login_url='/login'), name='dispatch')
@method_decorator(user_passes_test(not_in_admin_group, login_url='/login'), name='dispatch')
class UploadSystemBlackListView(FormView):
    form_class = SystemBlackListImportDataForm
    template_name = 'externalapp/import_form.html'

    @staticmethod
    def __nan_to_none(value):
        if pd.isna(value):
            value = None

        return value

    def get_success_url_primitive(self, request, customer):
        return render(request, template_name=self.succeeded_template,
                      context={'customer': customer})

    def get_success_url(self):
        # file uploading completed
        # referring document page
        return reverse_lazy('docs', kwargs=self.kwargs)

    def get_error_url(self, request, message):
        return render(request, template_name=self.error_template,
                      context={'error': message})

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context={'forms': self.form_class})

    @staticmethod
    def handle_with_customer(customer):
        if customer not in ("", None):
            try:
                customer = UserAdaptor.objects.get(firm_full_name=customer)

            except UserAdaptor.DoesNotExist:
                customer = UserAdaptor.objects.create(firm_full_name=customer)

        else:
            customer = UserAdaptor.dummy_creator.create_dummy()

        return customer

    def post(self, request, *args, **kwargs):
        data = request.FILES['riskDataFile']

        if not str(data.name).endswith('.xlsx'):
            return render(request, template_name='risk_analysis/error_pages/general_error.html',
                          context={'error': "Uploaded file must be xlsx file !"})

        p = default_storage.save(data.name, ContentFile(data.read()))

        # saving process
        p = os.path.join(MEDIA_ROOT, p)

        df = pd.read_excel(p)

        # Analyzing process
        for index, row in df.iterrows():
            print(row)

            kw = {}
            return redirect('get-riskds', **kw)


@method_decorator(login_required(login_url='/login'), name='dispatch')
@method_decorator(user_passes_test(not_in_admin_group, login_url='/login'), name='dispatch')
class UploadKonkordatoView(FormView):
    form_class = KonkordatoListImportDataForm
    template_name = 'externalapp/import_form.html'

    @staticmethod
    def __nan_to_none(value):
        if pd.isna(value):
            value = None

        return value

    def get_success_url_primitive(self, request, customer):
        return render(request, template_name=self.succeeded_template,
                      context={'customer': customer})

    def get_success_url(self):
        # file uploading completed
        # referring document page
        return reverse_lazy('docs', kwargs=self.kwargs)

    def get_error_url(self, request, message):
        return render(request, template_name=self.error_template,
                      context={'error': message})

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context={'forms': self.form_class})

    @staticmethod
    def handle_with_customer(customer):
        if customer not in ("", None):
            try:
                customer = UserAdaptor.objects.get(firm_full_name=customer)

            except UserAdaptor.DoesNotExist:
                customer = UserAdaptor.objects.create(firm_full_name=customer)

        else:
            customer = UserAdaptor.dummy_creator.create_dummy()

        return customer

    def post(self, request, *args, **kwargs):
        data = request.FILES['riskDataFile']

        if not str(data.name).endswith('.xlsx'):
            return render(request, template_name='risk_analysis/error_pages/general_error.html',
                          context={'error': "Uploaded file must be xlsx file !"})

        p = default_storage.save(data.name, ContentFile(data.read()))

        # saving process
        p = os.path.join(MEDIA_ROOT, p)

        df = pd.read_excel(p)

        # Analyzing process
        for index, row in df.iterrows():
            pass

            kw = {}
            return redirect('get-riskds', **kw)


@method_decorator(login_required(login_url='/login'), name='dispatch')
@method_decorator(user_passes_test(not_in_admin_group, login_url='/login'), name='dispatch')
class UploadTAXDebtView(FormView):
    form_class = TaxDebtListImportDataForm
    template_name = 'externalapp/import_form.html'

    @staticmethod
    def __nan_to_none(value):
        if pd.isna(value):
            value = None

        return value

    def get_success_url_primitive(self, request, customer):
        return render(request, template_name=self.succeeded_template,
                      context={'customer': customer})

    def get_success_url(self):
        # file uploading completed
        # referring document page
        return reverse_lazy('docs', kwargs=self.kwargs)

    def get_error_url(self, request, message):
        return render(request, template_name=self.error_template,
                      context={'error': message})

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context={'forms': self.form_class})

    @staticmethod
    def handle_with_customer(customer):
        if customer not in ("", None):
            try:
                customer = UserAdaptor.objects.get(firm_full_name=customer)

            except UserAdaptor.DoesNotExist:
                customer = UserAdaptor.objects.create(firm_full_name=customer)

        else:
            customer = UserAdaptor.dummy_creator.create_dummy()

        return customer

    def post(self, request, *args, **kwargs):
        data = request.FILES['riskDataFile']

        if not str(data.name).endswith('.xlsx'):
            return render(request, template_name='risk_analysis/error_pages/general_error.html',
                          context={'error': "Uploaded file must be xlsx file !"})

        p = default_storage.save(data.name, ContentFile(data.read()))

        # saving process
        p = os.path.join(MEDIA_ROOT, p)

        df = pd.read_excel(p)

        # Analyzing process
        for index, row in df.iterrows():
            pass

            kw = {}
            return redirect('get-riskds', **kw)


@method_decorator(login_required(login_url='/login'), name='dispatch')
@method_decorator(user_passes_test(not_in_admin_group, login_url='/login'), name='dispatch')
class UploadSGKDebtView(FormView):
    form_class = SGKDebtListImportDataForm
    template_name = 'externalapp/import_form.html'

    @staticmethod
    def __nan_to_none(value):
        if pd.isna(value):
            value = None

        return value

    def get_success_url_primitive(self, request, customer):
        return render(request, template_name=self.succeeded_template,
                      context={'customer': customer})

    def get_success_url(self):
        # file uploading completed
        # referring document page
        return reverse_lazy('docs', kwargs=self.kwargs)

    def get_error_url(self, request, message):
        return render(request, template_name=self.error_template,
                      context={'error': message})

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context={'forms': self.form_class})

    @staticmethod
    def handle_with_customer(customer):
        if customer not in ("", None):
            try:
                customer = UserAdaptor.objects.get(firm_full_name=customer)

            except UserAdaptor.DoesNotExist:
                customer = UserAdaptor.objects.create(firm_full_name=customer)

        else:
            customer = UserAdaptor.dummy_creator.create_dummy()

        return customer

    def post(self, request, *args, **kwargs):
        data = request.FILES['riskDataFile']

        if not str(data.name).endswith('.xlsx'):
            return render(request, template_name='risk_analysis/error_pages/general_error.html',
                          context={'error': "Uploaded file must be xlsx file !"})

        p = default_storage.save(data.name, ContentFile(data.read()))

        # saving process
        p = os.path.join(MEDIA_ROOT, p)

        df = pd.read_excel(p)

        # Analyzing process
        for index, row in df.iterrows():
            pass

            kw = {}
            return redirect('get-riskds', **kw)


# Retrieving
@method_decorator(login_required(login_url='/login'), name='dispatch')
@method_decorator(user_passes_test(not_in_admin_group, login_url='/login'), name='dispatch')
class RetrieveSGKFormView(FilterView):
    pass


@method_decorator(login_required(login_url='/login'), name='dispatch')
@method_decorator(user_passes_test(not_in_admin_group, login_url='/login'), name='dispatch')
class RetrieveTaxFormView(FilterView):
    pass
