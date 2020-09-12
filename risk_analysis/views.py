from abc import ABC

from django.shortcuts import render
from collections import Counter
from risk_analysis.models import DataSetModel


class BaseWarnings(ABC):
    template_name = 'risk_analysis/added_dataset_warning_base.html'
    messages = []

    def alert_popup(self, request):
        return render(request, template_name=self.template_name,
                      context={'messages': self.messages})


class DataSetWarnings(DataSetModel, BaseWarnings):
    """
        Including warnings and importing some files, pulling some data etc.
    """

    def alert(self, request):
        self.alert_popup(request)

    def limit_exceed_warning(self, request):
        if self.balance > self.limit:
            self.messages.append('Bakiye Limitten yüksek !')

    def maturity_exceed_warning(self):
        # todo: davut abi bekleniyor -> whatsapp
        pass

    def payback_anomali_warning(self):
        """
        iade % si geçmiş aylara kıyasla artarsa veya genel müşteri ortalamasına kıyasla yüksekse
        """
        artis_gecmis_aylara_gore = None

        customer_data = DataSetModel.objects.all().filter(customer_id=self.customer_id)

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
        customer_data = DataSetModel.objects.all().filter(customer_id=self.customer_id)

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
