from django.shortcuts import render

from externalapp.models import ExternalBlackList, SystemBlackList, KonkordatoList
from risk_analysis.models import TaxDebtList, SGKDebtListModel
from risk_analysis.views import DataSetWarnings


class AccountInitialProcesses:
    """
    Including warnings and importing some files, pulling some data etc.
    """
    account_warning_template = 'checkaccount/added_dataset_warning_base.html'

    def render_base(self, request, **kwargs):
        return render(request, self.account_warning_template, kwargs)

    def alert_popup(self, request, message_type, *messages):
        context = {'messages': messages, 'message_type': message_type}
        return self.render_base(request, context=context)

    def find_recent_accounts(self):
        customers = DataSetWarnings.recent_accounts()
        return customers

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

    @FutureWarning
    def find_konkordato_list(self, request, customer_id):
        related_konkordato_lists = KonkordatoList.objects.all().filter(customer_id=customer_id)
        return self.alert_popup(request, 'Konkordato List', related_konkordato_lists)

