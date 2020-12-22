import os
from abc import ABC
from collections import Counter

import pandas as pd
from bootstrap_modal_forms.generic import BSModalFormView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DetailView
from django.views.generic.edit import FormView, CreateView
from django_filters.views import FilterView

from DumanCPMS.settings import MEDIA_ROOT
from risk_analysis.algorithms import AnalyzingRiskDataSet
from risk_analysis.forms import RiskAnalysisCreateForm, RiskAnalysisImportDataForm, RiskAnalysisRetrieveForm
from risk_analysis.models import DataSetModel
from risk_analysis.tests import CreateRiskDatasetOne
from risk_analysis.usermodel import UserAdaptor


def risk_main_page(request):
    return render(request, 'risk_analysis/risk_main_page.html')


def generic_thanks(request):
    return render(request, 'risk_analysis/generic_thanks.html')


def not_in_riskanalysis_group(user):
    if user.is_superuser:
        return True

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
    error_template = 'risk_analysis/error_pages/general_error.html'
    succeeded_template = 'risk_analysis/succeeded_page.html'

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
        return render(request, self.template_name, context={'forms': RiskAnalysisImportDataForm})

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
            customer = self.handle_with_customer(self.__nan_to_none(row.get('Müşteri')))
            limit = self.__nan_to_none(row.get('limit'))
            warrant_state = self.__nan_to_none(row.get('teminat'))  # todo: string converting
            warrant_amount = self.__nan_to_none(row.get('Teminat Tutarı'))
            maturity = self.__nan_to_none(row.get('Vade'))

            maturity_exceed_avg = self.__nan_to_none(row.get('Ort. Gecikme Gün Bakiyesi (TL)'))
            avg_order_amount_last_twelve_months = self.__nan_to_none(row.get('Son 12 Ay Ortalama Sipariş Tutarı'))
            avg_order_amount_last_three_months = self.__nan_to_none(row.get('Son 3 Ay Ortalama Sipariş Tutarı'))
            last_3_months_aberration = self.__nan_to_none(
                row.get('Son 3 ay ile Son 11 aylık satış ortalamasından sapma')) # veride yok

            # veride yok
            last_month_payback_perc = self.__nan_to_none(row.get('Son ay iade yüzdesi'))

            last_twelve_months_payback_perc = self.__nan_to_none(row.get('Son 12 ay iade yüzdesi'))

            # veride yok
            avg_last_three_months_payback_perc = self.__nan_to_none(row.get('Son 3 ay ortalama iade yüzdesi'))

            # veride yok ayrıca saçma, hesaplanabilir
            last_three_months_payback_comparison = self.__nan_to_none(row.get('last_three_months_payback_comparison'))

            avg_delay_time = self.__nan_to_none(row.get('Ort. Gecikme Gün Sayısı'))
            avg_delay_balance = self.__nan_to_none(row.get('Ort. Gecikme Gün Bakiyesi (TL)'))
            period_day = self.__nan_to_none(row.get('Devir Günü'))

            # Devir hızı: Müşterinin Aylık Sipariş Hacmi / Müşterinin Aylık Ortalama Bakiye
            period_velocity = self.__nan_to_none(row.get('Devir Hızı'))

            # bakiye - teminat tutarı: balance - warrant amount
            risk_excluded_warrant_balance = self.__nan_to_none(row.get('Teminat Harici Bakiye-Risk'))

            balance = self.__nan_to_none(row.get('Bakiye'))
            profit = self.__nan_to_none(row.get('Kar'))  # d. a. ş. y.

            profit_percent = self.__nan_to_none(row.get('Kar yüzdesi'))  # kar yuzdesi davut a. v. v, ş.y.

            # çek dahili toplam risk davut abinin veride var, şemada yok.
            total_risk_including_cheque = self.__nan_to_none(row.get('Çek Dahil Toplam Risk'))

            # bu veri şemamızda yok, davut abinin gönderdiği örnek veride var.
            last_12_months_total_endorsement = self.__nan_to_none(row.get('Son 12 Ay Toplam Ciro'))
            # period_percent = row.get('period_percent')

            risk_model_object = DataSetModel(
                customer=customer,
                last_12_months_total_endorsement=last_12_months_total_endorsement,
                maturity=maturity,
                limit=limit,
                total_risk_including_cheque=total_risk_including_cheque,
                warrant_state=warrant_state,
                warrant_amount=warrant_amount,
                avg_order_amount_last_twelve_months=avg_order_amount_last_twelve_months,
                avg_order_amount_last_three_months=avg_order_amount_last_three_months,
                last_3_months_aberration=last_3_months_aberration,
                last_twelve_months_payback_perc=last_twelve_months_payback_perc,
                avg_last_three_months_payback_perc=avg_last_three_months_payback_perc,
                last_three_months_payback_comparison=last_three_months_payback_comparison,
                avg_delay_time=avg_delay_time,
                risk_excluded_warrant_balance=risk_excluded_warrant_balance,
                balance=balance,
                period_velocity=period_velocity,
                period_day=period_day,
                maturity_exceed_avg=maturity_exceed_avg,
                avg_delay_balance=avg_delay_balance,
                last_month_payback_perc=last_month_payback_perc,
                profit=profit,
                profit_percent=profit_percent
            )
            risk_model_object.save()

        return redirect('ra-index')


@method_decorator(login_required(login_url='/login'), name='dispatch')
@method_decorator(user_passes_test(not_in_riskanalysis_group, login_url='/login'), name='dispatch')
class RiskAnalysisDetailView(DetailView):
    template_name = 'risk_analysis/get_risk_data.html'
    model = DataSetModel

    def get(self, request, *args, **kwargs):
        try:
            DataSetModel.objects.get(**kwargs)

        except DataSetModel.DoesNotExist:
            return redirect('risk_analysis-create-page')

        return super(RiskAnalysisDetailView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        return super(RiskAnalysisDetailView, self).get_queryset()


@method_decorator(login_required(login_url='/login'), name='dispatch')
@method_decorator(user_passes_test(not_in_riskanalysis_group, login_url='/login'), name='dispatch')
class RetrieveRiskAnalysisFormView(BSModalFormView):
    template_name = 'risk_analysis/risk_analysis_retrieve.html'
    form_class = RiskAnalysisRetrieveForm

    def get(self, request, *args, **kwargs):
        related_customer_id = request.GET.get('related_customer')
        if related_customer_id is None or related_customer_id == "":
            riskdatasets = DataSetModel.objects.all()
            return render(request, self.template_name, context={'filter': self.form_class,
                                                                'riskdatasets': riskdatasets})
        else:
            try:
                riskds = DataSetModel.objects.filter(
                    customer=UserAdaptor.objects.get(pk=related_customer_id))

                if len(riskds) == 0:
                    return redirect('risk_analysis-create-page')

                return render(request, self.template_name, context={'filter': self.form_class,
                                                                    'riskdatasets': riskds})

            except UserAdaptor.DoesNotExist:
                # messages.warning(request, errors.CADoesNotExists)
                return redirect('ra-index')

    def form_valid(self, form):
        if 'clear' in self.request.POST:
            self.filter = ''
        else:
            self.filter = '?related_customer=' + form.cleaned_data['customer']

        response = super().form_valid(form)
        return response

    def get_success_url(self):
        return reverse_lazy('index') + self.filter


@method_decorator(login_required(login_url='/login'), name='dispatch')
@method_decorator(user_passes_test(not_in_riskanalysis_group, login_url='/login'), name='dispatch')
class RiskAnalysisSearchView(FilterView):
    def get(self, request, *args, **kwargs):
        return super(RiskAnalysisSearchView, self).get(request, *args, **kwargs)


@method_decorator(login_required(login_url='/login'), name='dispatch')
@method_decorator(user_passes_test(not_in_riskanalysis_group, login_url='/login'), name='dispatch')
class CreateRiskAnalysisFormView(CreateView):
    form_class = RiskAnalysisCreateForm
    template_name = 'risk_analysis/create_page/create_form.html'
    model = DataSetModel

    def get_success_url(self):
        kw = self.kwargs
        return redirect('get-riskds', **kw)

    def get_form(self, form_class=None):
        form = super(CreateRiskAnalysisFormView, self).get_form(form_class)

        if self.request.method == 'POST':
            return form

        elif self.request.method == 'GET':
            form.instance.created_by = self.request.user
            rd = CreateRiskDatasetOne.create()
            form = RiskAnalysisCreateForm(instance=rd)

            return form


# Analyzing
def analyze_one(request, pk):
    rd = DataSetModel(pk=pk)
    analyze = AnalyzingRiskDataSet(rd)

    return render(request)


class AnalyzeOne(View):
    def get(self, request, pk, *args, **kwargs):
        super(AnalyzeOne, self).get(request, *args, **kwargs)

    def post(self, request, pk, *args, **kwargs):
        super(AnalyzeOne, self).post(request, *args, **kwargs)


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

    def recent_accounts(self):
        return self.dataset.values('customer')

    def maturity_exceed_warning(self):
        # todo: davut abi bekleniyor -> whatsapp
        pass

    def payback_anomali_warning(self):
        """
        iade % si geçmiş aylara kıyasla artarsa veya genel müşteri ortalamasına kıyasla yüksekse
        """
        artis_gecmis_aylara_gore = None

        customer_data = DataSetModel.objects.all().filter(customer_id=self.dataset.customer)

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
        customer_data = DataSetModel.objects.all().filter(customer_id=self.dataset.customer)

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
