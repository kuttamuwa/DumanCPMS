from abc import ABC

from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render
from collections import Counter

from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic.edit import CreateView, FormView
from django_filters.views import FilterView

from risk_analysis.forms import RiskAnalysisCreateForm, RiskAnalysisImportDataForm
from risk_analysis.models import DataSetModel

import pandas as pd


def risk_main_page(request):
    return render(request, 'risk_analysis/risk_main_page.html')


def not_in_riskanalysis_group(user):
    if user.is_authenticated and user.groups.filter(name='RiskAnalysisAdmin').exists():
        return True
    else:
        return False
    # todo : https://stackoverflow.com/questions/29682704/how-to-use-the-user-passes-test-decorator-in-class-based-views
    # todo: permissions ekleyelim
    # or user.user_permissions


def get_risk_by_customer_id(request, customer_id):
    """

        :param request:
        :param customer_id:
        :return:
    """
    try:
        dataset = DataSetModel.objects.get(customer_id=customer_id)

    except DataSetModel.DoesNotExist:
        return render(request, 'checkaccount/no_check_account_error.html')

    if request.method == 'GET':
        context = {'dataset': dataset}

        return render(request, context=context, template_name='risk_analysis/get_risk_data.html')


def creation_type_main_page(request):
    """
    Gives two option : Import with excel or type down one by one
    """
    return render(request, template_name='risk_analysis/create_page/create_page.html')


@method_decorator(login_required(login_url='/login'), name='dispatch')
@method_decorator(user_passes_test(not_in_riskanalysis_group, login_url='/login'), name='dispatch')
class UploadRiskAnalysisDataView(FormView):
    form_class = RiskAnalysisImportDataForm
    template_name = 'risk_analysis/create_page/import_form.html'

    def get_success_url(self):
        # file uploading completed
        # referring document page
        return reverse_lazy('docs', kwargs=self.kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context={'forms': RiskAnalysisImportDataForm})

    def post(self, request, *args, **kwargs):
        form = RiskAnalysisImportDataForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        pass

    # def get_context_data(self, **kwargs):
    #     customer_id = self.kwargs.get('customer_id')
    #     context = super().get_context_data(**kwargs)
    #
    #     if customer_id is not None:
    #         ds = DataSetModel.objects.get(customer_id=customer_id)
    #         context['ds'] = ds
    #
    #     return context
    #
    # def form_valid(self, form):
    #     form.instance.customer_id = DataSetModel.objects.get(customer_id=self.kwargs.get('customer_id'))
    #     self.object = form.save()
    #     return HttpResponseRedirect(self.get_success_url())


@method_decorator(login_required(login_url='/login'), name='dispatch')
@method_decorator(user_passes_test(not_in_riskanalysis_group, login_url='/login'), name='dispatch')
class RetrieveRiskAnalysisFormView(FilterView):
    pass


class CreateRiskAnalysisFormView(View):
    form_class = RiskAnalysisCreateForm
    initial = {'key': 'value'}
    template_name = 'risk_analysis/create_page/create_form.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            return HttpResponseRedirect('/success/')

        return render(request, self.template_name, {'form': form})


class BaseWarnings(ABC):
    template_name = 'risk_analysis/added_dataset_warning_base.html'
    messages = []

    def alert_popup(self, request):
        return render(request, template_name=self.template_name,
                      context={'messages': self.messages})


class DataSetWarnings(BaseWarnings):
    """
        Including warnings and importing some files, pulling some data etc.
    """

    def __init__(self, dataset_object):
        self.dataset = dataset_object

    def alert(self, request):
        self.alert_popup(request)

    def limit_exceed_warning(self, request):
        if self.dataset.balance > self.dataset.limit:
            self.messages.append('Bakiye Limitten yüksek !')

    def maturity_exceed_warning(self):
        # todo: davut abi bekleniyor -> whatsapp
        pass

    def payback_anomali_warning(self):
        """
        iade % si geçmiş aylara kıyasla artarsa veya genel müşteri ortalamasına kıyasla yüksekse
        """
        artis_gecmis_aylara_gore = None

        customer_data = DataSetModel.objects.all().filter(customer_id=self.dataset.customer_id)

        payback_this_month = customer_data[-1].last_month_payback_comparison
        payback_back_month = customer_data[-2].last_month_payback_comparison

        if payback_this_month > payback_back_month:
            self.messages.append("Bu ayın geçmiş aylara göre geri iadesi, geçen aydan daha fazladır !")

        all_customers_data = DataSetModel.objects.all()
        all_customers_last_month_payback_comps = [i[-2].last_month_payback_comparison
                                                  < i[-1].last_month_payback_comparison for i in all_customers_data]

        stats = Counter(all_customers_last_month_payback_comps)
        if stats.get(True) > stats.get(False):
            self.messages.append("Diğer müşterilerin de iadeleri bu ay iadeleri çok !")

        else:
            self.messages.append("Diğer müşterilerin bu ay iadeleri bu müşteri kadar çok değil !")

    def income_freq_warning(self):
        """
        Alacak devir hızı geçmiş aylara kıyasla artarsa veya genel müşteri ortalamasına kıyasla yüksekse
        """
        customer_data = DataSetModel.objects.all().filter(customer_id=self.dataset.customer_id)

        income_freq_this_month = customer_data[-1].period_velocity
        income_freq_back_month = customer_data[-2].period_velocity

        if income_freq_this_month > income_freq_back_month:
            self.messages.append("Bu ayın geçmiş aylara göre geri iadesi, geçen aydan daha fazladır !")

        all_customers_data = DataSetModel.objects.all()
        all_customers_last_month_payback_comps = [i[-2].last_month_payback_comparison
                                                  < i[-1].last_month_payback_comparison for i in all_customers_data]

        stats = Counter(all_customers_last_month_payback_comps)
        if stats.get(True) > stats.get(False):
            self.messages.append("Diğer müşterilerin de iadeleri bu ay devir hızları artmış !")

        else:
            self.messages.append("Diğer müşterilerin bu ay iadeleri bu devir hızları artmamış !")

    def customer_performance_credit_pts(self):
        """
        General algorithm
        todo: important.
        """
        pass
