import os
from abc import ABC
from collections import Counter

import pandas as pd
from bootstrap_modal_forms.generic import BSModalFormView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View, generic
from django.views.generic.edit import FormView
from django_filters.views import FilterView

from DumanCPMS.settings import MEDIA_ROOT
from checkaccount.models import CheckAccount
from risk_analysis.algorithms import AnalyzingRiskDataSet
from risk_analysis.forms import RiskAnalysisCreateForm, RiskAnalysisImportDataForm, SGKImportDataForm, \
    TAXImportDataForm, RiskAnalysisRetrieveForm
from risk_analysis.models import DataSetModel, SGKDebtListModel, TaxDebtList


def risk_main_page(request):
    return render(request, 'risk_analysis/risk_main_page.html')


def generic_thanks(request):
    return render(request, 'risk_analysis/generic_thanks.html')


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

    def post(self, request, *args, **kwargs):
        data = request.FILES['riskDataFile']

        if not str(data.name).endswith('.xlsx'):
            return render(request, template_name='risk_analysis/error_pages/general_error.html',
                          context={'error': "Uploaded file must be xlsx file !"})

        p = default_storage.save(data.name, ContentFile(data.read()))

        # saving process
        p = os.path.join(MEDIA_ROOT, p)

        df = pd.read_excel(p, sheet_name="MPYS Sn")

        # Analyzing process
        for index, row in df.iterrows():
            limit = self.__nan_to_none(row.get('limit'))
            warrant_state = self.__nan_to_none(row.get('warrant_state'))  # todo: string converting
            warrant_amount = self.__nan_to_none(row.get('warrant_amount'))
            customer_name = self.__nan_to_none(row.get('customer_name'))

            # if warrant_state is None or warrant_state is False or warrant_state == 'Yok':
            #     if warrant_amount is None:
            #         warrant_amount = None

            maturity = self.__nan_to_none(row.get('maturity'))
            payment_frequency = self.__nan_to_none(row.get('payment_frequency'))
            maturity_exceed_avg = self.__nan_to_none(row.get('maturity_exceed_avg'))
            avg_order_amount_last_twelve_months = self.__nan_to_none(row.get('avg_order_amount_last_twelve_months'))
            avg_order_amount_last_three_months = self.__nan_to_none(row.get('avg_order_amount_last_three_months'))
            last_3_months_aberration = self.__nan_to_none(row.get('last_3_months_aberration'))
            last_month_payback_perc = self.__nan_to_none(row.get('last_month_payback_perc'))
            last_twelve_months_payback_perc = self.__nan_to_none(row.get('last_twelve_months_payback_perc'))
            avg_last_three_months_payback_perc = self.__nan_to_none(row.get('avg_last_three_months_payback_perc'))
            last_three_months_payback_comparison = self.__nan_to_none(row.get('last_three_months_payback_comparison'))
            avg_delay_time = self.__nan_to_none(row.get('avg_delay_time'))
            avg_delay_balance = self.__nan_to_none(row.get('avg_delay_balance'))
            period_day = self.__nan_to_none(row.get('period_day'))
            period_velocity = self.__nan_to_none(row.get('period_velocity'))

            # bakiye - teminat tutarı: balance - warrant amount
            risk_excluded_warrant_balance = self.__nan_to_none(row.get('risk_excluded_warrant_balance'))

            balance = self.__nan_to_none(row.get('balance'))
            profit = self.__nan_to_none(row.get('profit'))  # d. a. ş. y.

            profit_percent = self.__nan_to_none(row.get('profit_percent'))  # kar yuzdesi davut a. v. v, ş.y.

            # çek dahili toplam risk davut abinin veride var, şemada yok.
            total_risk_including_cheque = self.__nan_to_none(row.get('total_risk_including_cheque'))

            # bu veri şemamızda yok, davut abinin gönderdiği örnek veride var.
            last_12_months_total_endorsement = self.__nan_to_none(row.get('last_12_months_total_endorsement'))
            # period_percent = row.get('period_percent')

            try:
                related_check_account = CheckAccount.objects.get(firm_full_name=customer_name)

            except CheckAccount.DoesNotExist:
                related_check_account = CheckAccount(firm_full_name=customer_name).save()

            risk_model_object = DataSetModel(
                related_customer=related_check_account,
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
                payment_frequency=payment_frequency,
                maturity_exceed_avg=maturity_exceed_avg,
                avg_delay_balance=avg_delay_balance,
                last_month_payback_perc=last_month_payback_perc,
                profit=profit,
                profit_percent=profit_percent
            )
            risk_model_object.save()
            try:
                # saving data
                # analyzedata.save_risk_dataset_data()
                # analyzedata.save_risk_points_data()
                return self.get_success_url_primitive(request, customer=related_check_account)

            except Exception as err:
                return self.get_error_url(request, err)


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
            riskds = DataSetModel.objects.filter(
                related_customer=CheckAccount.objects.get(customer_id=related_customer_id))
            return render(request, self.template_name, context={'filter': self.form_class,
                                                                'riskdatasets': riskds})

    def form_valid(self, form):
        if 'clear' in self.request.POST:
            self.filter = ''
        else:
            self.filter = '?related_customer=' + form.cleaned_data['related_customer']

        response = super().form_valid(form)
        return response

    def get_success_url(self):
        return reverse_lazy('index') + self.filter


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


# SGK
@method_decorator(login_required(login_url='/login'), name='dispatch')
@method_decorator(user_passes_test(not_in_riskanalysis_group, login_url='/login'), name='dispatch')
class UploadSGKData(FormView):
    form_class = SGKImportDataForm
    template_name = 'risk_analysis/create_page/import_sgk_dataset_form.html'
    error_template = 'risk_analysis/error_pages/general_error.html'
    succeeded_template = 'risk_analysis/succeeded_page_sgk.html'

    @staticmethod
    def __nan_to_none(value):
        if pd.isna(value):
            value = None

        return value

    def get_success_url_primitive(self, request):
        return render(request, template_name=self.succeeded_template)

    def get_success_url(self):
        # file uploading completed
        # referring document page
        return reverse_lazy('docs', kwargs=self.kwargs)

    def get_error_url(self, request, message):
        return render(request, template_name=self.error_template,
                      context={'error': message})

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context={'forms': SGKImportDataForm})

    def post(self, request, *args, **kwargs):
        data = request.FILES['sgkDataFile']
        p = default_storage.save(data.name, ContentFile(data.read()))

        # saving process
        p = os.path.join(MEDIA_ROOT, p)
        df = pd.read_excel(p, skiprows=1)

        error_rows = []
        try:
            for index, row in df.iterrows():
                taxpayer_number = self.__nan_to_none(row.get('Vergi No/ TC Kimlik No'))
                firm_title = self.__nan_to_none(row.get('İŞVERENİN UNVANI/ADI SOYADI'))
                debt_amount = self.__nan_to_none(row.get('Prim Aslı Borç Tutarı'))

                sgk_model_object = SGKDebtListModel(
                    taxpayer_number=taxpayer_number,
                    firm_title=firm_title,
                    debt_amount=debt_amount
                )
                sgk_model_object.save()
        except Exception as err:
            error_rows.append({'row': row, 'error description': err})

        return render(request, template_name=self.succeeded_template,
                      context={'errors': error_rows})


@method_decorator(login_required(login_url='/login'), name='dispatch')
@method_decorator(user_passes_test(not_in_riskanalysis_group, login_url='/login'), name='dispatch')
class RetrieveSGKFormView(FilterView):
    pass


@method_decorator(login_required(login_url='/login'), name='dispatch')
@method_decorator(user_passes_test(not_in_riskanalysis_group, login_url='/login'), name='dispatch')
class UploadTaxData(FormView):
    form_class = TAXImportDataForm
    template_name = 'risk_analysis/create_page/import_tax_dataset_form.html'
    error_template = 'risk_analysis/error_pages/general_error.html'
    succeeded_template = 'risk_analysis/succeeded_page_tax.html'

    @staticmethod
    def __nan_to_none(value):
        if pd.isna(value):
            value = None

        return value

    def get_success_url_primitive(self, request):
        return render(request, template_name=self.succeeded_template)

    def get_success_url(self):
        # file uploading completed
        # referring document page
        return reverse_lazy('docs', kwargs=self.kwargs)

    def get_error_url(self, request, message):
        return render(request, template_name=self.error_template,
                      context={'error': message})

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context={'forms': TAXImportDataForm})

    def post(self, request, *args, **kwargs):
        data = request.FILES['taxDataFile']
        p = default_storage.save(data.name, ContentFile(data.read()))

        p = os.path.join(MEDIA_ROOT, p)
        df = pd.read_excel(p)

        error_rows = []

        for index, row in df.iterrows():
            tax_department = self.__nan_to_none(row.get('Vergi Dairesi'))
            taxpayer_number = self.__nan_to_none(row.get('Vergi Kimlik Numarası'))
            dept_title = self.__nan_to_none(row.get('Borçlunun Adı Soyadı/Unvanı'))
            real_operating_income = self.__nan_to_none(row.get('Esas Faaliyet Konusu'))
            dept_amount = self.__nan_to_none(row.get('Borç Miktarı'))

            # todo: buralar standartlastirilmali -> davut abi.
            dept_amount = float(dept_amount.replace('.', '').replace(',', '.'))

            tax_model_object = TaxDebtList(
                tax_department=tax_department,
                taxpayer_number=taxpayer_number,
                dept_title=dept_title,
                real_operating_income=real_operating_income,
                dept_amount=dept_amount
            )
            try:
                tax_model_object.save()
            except Exception as err:
                error_rows.append({'row': row, 'error description': err})

        return render(request, template_name=self.succeeded_template,
                      context={'errors': error_rows})


@method_decorator(login_required(login_url='/login'), name='dispatch')
@method_decorator(user_passes_test(not_in_riskanalysis_group, login_url='/login'), name='dispatch')
class RetrieveTaxFormView(FilterView):
    pass


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

        customer_data = DataSetModel.objects.all().filter(customer_id=self.dataset.related_customer)

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
        customer_data = DataSetModel.objects.all().filter(customer_id=self.dataset.related_customer)

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


class RiskAnalysisListView(generic.ListView):
    template_name = 'risk_analysis/risk_analysis_retrieve.html'

    def get(self, request, *args, **kwargs):
        customer_id = kwargs.get('customer_id')
        if customer_id is None:
            return render(request, 'risk_analysis/analysis/select_customer_page.html',
                          context={'riskdatasets': DataSetModel.objects.all()})

        else:
            customer_id = kwargs.get('customer_id')
            check_account = CheckAccount.objects.get(customer_id=customer_id)

            risk_data = DataSetModel.objects.get(related_customer=check_account)
            analyze_risk_ds = AnalyzingRiskDataSet(risk_data)
            analyze_risk_ds.analyze_all()

            return render(request, self.template_name)


class BasicDashboardData:
    def __init__(self, customer_id):
        self.customer_id = customer_id
        try:
            customer = CheckAccount.objects.get(customer_id=customer_id)

        except CheckAccount.DoesNotExist:
            # todo : logging
            print(f"{customer_id} idli musteri bulunamadı !")
            raise ValueError

        self.customer = customer

    def limit_exceeds(self):
        pass

    def maturity_exceeds(self):
        pass

    def income_period_velocity(self):
        pass

    def cheque_index_unwanted_range(self):
        """
        ne demek bu? Hangi aralık?
        # todo: ? Davut abi
        """
        pass

    def arkasi_yazili_cekler(self):
        """
        # todo boyle bir veri yok?
        """
        pass

    def narrowing_closing_credit_limit(self):
        """
        # todo boyle bir veri yok?
        """
        pass

    def tax_debts(self):
        """

        """
        pass

    def sgk_debts(self):
        """

        """
        pass

    def sector_black_list(self):
        """

        """
        pass

    def findeks_credit_pts(self):
        """

        """
        pass

    def qr_cheque_score_parallel_warning(self):
        """

        """
        pass

    def recent_added_check_accounts(self):
        return CheckAccount.objects[:-5]
