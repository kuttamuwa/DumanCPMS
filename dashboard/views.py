from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from rest_framework import viewsets

from checkaccount.serializers import CheckAccountSerializer
from externalapp.models import ExternalBlackList, SystemBlackList, KonkordatoList, SGKDebtListModel, TaxDebtList
from risk_analysis.models import DataSetModel
from risk_analysis.views import DataSetWarnings

try:
    from checkaccount.models import CheckAccount

    account = CheckAccount

except ImportError:
    from risk_analysis.basemodels import DummyUser

    account = DummyUser


class DashBoardView(View):
    template = 'dboards/customer_dash.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template)

    def post(self, request, *args, **kwargs):
        return render(request, self.template)


class AccountInitialProcesses:
    """
    Including warnings and importing some files, pulling some data etc.
    """
    account_warning_template = 'checkaccount/added_dataset_warning_base.html'

    def find_recent_accounts(self):
        customers = DataSetWarnings.recent_accounts()
        return customers

    @FutureWarning
    def find_konkordato_list(self, request, customer_id):
        related_konkordato_lists = KonkordatoList.objects.all().filter(customer_id=customer_id)
        return self.alert_popup(request, 'Konkordato List', related_konkordato_lists)

    def limitexceeds(self, request):
        return DataSetModel.objects.get_limit_exceeds()


class LimitView(ListView):
    pass


class MaturityView(ListView):
    pass


class PeriodVelocityView(ListView):
    pass


class BlackListView(ListView):

    def alert_popup(self, request, message_type, *messages):
        context = {'messages': messages, 'message_type': message_type}
        return self.render_base(request, context=context)

    def render_base(self, request, **kwargs):
        return render(request, self.template_name, kwargs)

    def find_related_black_list(self, request, customer_id):
        related_black_list_record = ExternalBlackList.objects.all().filter(customer_id=customer_id)
        return self.alert_popup(request, 'Black list', related_black_list_record)

    def find_related_black_list_in_system(self, request, customer_id):
        related_sys_black_list_record = SystemBlackList.objects.all().filter(customer_id=customer_id)
        return self.alert_popup(request, 'System Black List', related_sys_black_list_record)

    def find_tax_debt_list(self, request, customer_id):
        tax_debts = TaxDebtList.objects.all().filter(customer_id=customer_id)
        return self.alert_popup(request, "Tax Debt List", tax_debts)

    def find_sgk_debt_list(self, request, customer_id):
        sgk_debts = SGKDebtListModel.objects.all().filter(customer_id=customer_id)
        return self.alert_popup(request, 'SGK Debt List', sgk_debts)


class CheckAccountAPI(viewsets.ModelViewSet):
    queryset = account.objects.all().order_by('-created_date')
    serializer_class = CheckAccountSerializer


def recent_customers(request, count=5):
    return CheckAccount.objects.all()[:count]
