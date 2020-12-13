from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView, LogoutView
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
# Create your views here.
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from django.views.generic.base import View
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from django_filters.views import FilterView
from dal import autocomplete
from checkaccount import tests
from checkaccount.forms import CheckAccountCreateForm, UploadAccountDocumentForm
from checkaccount.models import CheckAccount, AccountDocuments, SystemBlackList, KonkordatoList, ExternalBlackList
from risk_analysis.models import SGKDebtListModel, TaxDebtList


def main_page(request):
    return render(request, 'base.html')


checkaccount_shown_fields = ('customer_id',)


# Site views
def checkaccount_mainpage(request):
    return render(request, 'checkaccount/checkaccount_main.html')


def not_in_checkaccount_group(user):
    if user.is_superuser:
        return True

    if user.is_authenticated and user.groups.filter(name='CheckAccountAdmin').exists():
        return True
    else:
        return False
    # todo : https://stackoverflow.com/questions/29682704/how-to-use-the-user-passes-test-decorator-in-class-based-views
    # todo: permissions ekleyelim
    # or user.user_permissions


def succeed_create_check_account(request):
    return render(request, 'checkaccount/succeed_form.html')


def get_customer(request, pk, state=0):
    """

    :param request:
    :param pk:
    :param state: 1 -> comes from creating check account form.
                  0 -> just retrieve one account
    :return:
    """
    try:
        check_account = CheckAccount.objects.get(pk=pk)

    except CheckAccount.DoesNotExist:
        return render(request, 'checkaccount/no_check_account_error.html')

    # related account documents checking
    acc_doc_state = False
    try:
        AccountDocuments.objects.get(pk=pk)
        acc_doc_state = True

    except AccountDocuments.DoesNotExist:
        pass

    except AccountDocuments.MultipleObjectsReturned:
        # todo: logging
        print("Bir hesaba bagli birden çok döküman tespit edildi.")
        acc_doc_state = True

    if request.method == 'GET':
        context = {'checkaccount': check_account, 'state': state, 'acc_doc_state': acc_doc_state,
                   'part_doc_state': True, 'bank_state': True
                   }

        return render(request, context=context, template_name='checkaccount/get_check_account_and_upload.html')


class CitiesAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        pass


@method_decorator(login_required(login_url='/login'), name='dispatch')
@method_decorator(user_passes_test(not_in_checkaccount_group, login_url='/login'), name='dispatch')
class CheckAccountView(DetailView):
    template_name = 'checkaccount/get_check_account_and_upload.html'
    model = CheckAccount

    def get(self, request, *args, **kwargs):
        return super(CheckAccountView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        return super(CheckAccountView, self).get_queryset()


@method_decorator(login_required(login_url='/login'), name='dispatch')
@method_decorator(user_passes_test(not_in_checkaccount_group, login_url='/login'), name='dispatch')
class CheckAccountFormView(View):
    form_class = CheckAccountCreateForm
    initial = {'key': 'value'}
    template_name = 'checkaccount/checkaccount_form.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            return HttpResponseRedirect('/success/')

        return render(request, self.template_name, {'form': form})


@method_decorator(login_required(login_url='/login'), name='dispatch')
@method_decorator(user_passes_test(not_in_checkaccount_group, login_url='/login'), name='dispatch')
class CheckAccountFormCreateView(CreateView):
    template_name = 'checkaccount/checkaccount_form.html'
    model = CheckAccount
    form_class = CheckAccountCreateForm

    def get_success_url(self):
        return f'/checkaccount/get/{self.object.customer_id}'

    def get_form(self, form_class=None):
        form = super(CheckAccountFormCreateView, self).get_form(form_class)
        # form.instance.created_by = self.request.user

        # FOR TESTING
        ca = tests.CheckAccountTest.test_create_one_account()
        ca.created_by = self.request.user

        form = CheckAccountCreateForm(instance=ca)

        return form


@method_decorator(login_required(login_url='/login'), name='dispatch')
@method_decorator(user_passes_test(not_in_checkaccount_group, login_url='/login'), name='dispatch')
class CheckAccountFormDeleteView(DeleteView):
    model = CheckAccount
    template_name = 'checkaccount/delete_checkaccount_succeeded.html'
    success_url = '/'


@method_decorator(login_required(login_url='/login'), name='dispatch')
@method_decorator(user_passes_test(not_in_checkaccount_group, login_url='/login'), name='dispatch')
class CheckAccountFormUpdateView(UpdateView):
    # model = CheckAccountCreateForm
    fields = checkaccount_shown_fields


@method_decorator(login_required(login_url='/login'), name='dispatch')
@method_decorator(user_passes_test(not_in_checkaccount_group, login_url='/login'), name='dispatch')
class CheckAccountSearchView(FilterView):
    pass


class LoginUserView(LoginView):
    template_name = 'login_page.html'


class LogoutUserView(LogoutView):
    template_name = 'logout_page.html'
    next_page = '/'


class ErrorPages:
    @staticmethod
    def not_implemented_yet(request):
        return render(request, 'checkaccount/not_implemented_yet.html')


class GetAccountDocumentsList(DetailView):
    model = AccountDocuments
    template_name = 'checkaccount/uploaded_account_documents.html'
    context_object_name = 'AccountDocuments'

    # pk_url_kwarg = 'customer_id_id'
    # slug_field = 'customer'

    def get(self, request, *args, **kwargs):
        try:
            self.kwargs['pk'] = AccountDocuments.objects.get(customer=CheckAccount.objects.get(**self.kwargs)).pk

        except AccountDocuments.DoesNotExist:
            return redirect('upload_docs', **kwargs)

        return super(GetAccountDocumentsList, self).get(request, *args, **kwargs)
    #
    # def get_queryset(self):
    #     qset = super(GetAccountDocumentsList, self).get_queryset()
    #     customer_id = self.kwargs.get('customer_id')
    #     customer = CheckAccount.objects.get(pk=customer_id)
    #
    #     try:
    #         self.kwargs['pk'] = AccountDocuments.objects.get(customer=customer).pk
    #     except AccountDocuments.DoesNotExist:
    #         pass
    #
    #     return qset.filter(customer=customer)


class UploadAccountDocumentsView(CreateView):
    model = AccountDocuments
    form_class = UploadAccountDocumentForm
    success_url = reverse_lazy('docs')
    template_name = 'checkaccount/upload_account_document.html'

    def post(self, request, *args, **kwargs):
        # f = UploadAccountDocumentForm(request.POST)
        # f.created_by = request.user
        return super(UploadAccountDocumentsView, self).post(request, *args, **kwargs)

    def file_all_check(self):
        checkaccount_id = self.kwargs.get('pk')
        doc_control = self.document_control(checkaccount_id)
        if all(doc_control.values()):
            return True
        else:
            return False

    def get(self, request, *args, **kwargs):
        if self.file_all_check():
            # If all file uploaded?
            return redirect(reverse('docs', kwargs=self.kwargs))
        return super(UploadAccountDocumentsView, self).get(request, *args, **kwargs)

    def get_form(self, form_class=None):
        f = super(UploadAccountDocumentsView, self).get_form(form_class=form_class)

        if self.request.method == 'POST':
            if f.is_valid():
                check_account = CheckAccount.objects.get(**self.kwargs)
                f.instance.customer = check_account
                try:
                    f.instance = AccountDocuments.objects.get(customer_id=check_account)
                except AccountDocuments.DoesNotExist:
                    # never been created
                    pass

        if self.request.method == 'GET':
            f = self.form_state_manipulation(f, self.kwargs['pk'])

        return f

    def form_state_manipulation(self, form, customer_id):
        doc_control = self.document_control(customer_id)
        trpname = AccountDocuments.tax_return_pdf.field.attname
        aslpname = AccountDocuments.authorized_signatures_list_pdf.field.attname
        acpname = AccountDocuments.activity_certificate_pdf.field.attname

        if doc_control[trpname]:
            form.fields.get(trpname).disabled = True

        if doc_control[aslpname]:
            form.fields.get(aslpname).disabled = True

        if doc_control[acpname]:
            form.fields.get(acpname).disabled = True

        return form

    def get_success_url(self):
        # file uploading completed
        # referring document page
        return reverse_lazy('docs', kwargs=self.kwargs)

    def document_control(self, check_account_pk):
        trpname = AccountDocuments.tax_return_pdf.field.attname
        aslpname = AccountDocuments.authorized_signatures_list_pdf.field.attname
        acpname = AccountDocuments.activity_certificate_pdf.field.attname

        result_dict = {acpname: False, aslpname: False, trpname: False}

        try:
            acc = AccountDocuments.objects.get(customer_id=check_account_pk)

            if acc.activity_certificate_pdf.name:
                result_dict[acpname] = True
            if acc.authorized_signatures_list_pdf.name:
                result_dict[aslpname] = True
            if acc.tax_return_pdf.name:
                result_dict[trpname] = True

        except AccountDocuments.DoesNotExist:
            print(f"{check_account_pk} has no Account Documents")

        finally:
            return result_dict

    def get_context_data(self, **kwargs):
        customer_id = self.kwargs.get('pk')
        context = super(UploadAccountDocumentsView, self).get_context_data(**kwargs)

        if customer_id is not None:
            check_account = CheckAccount.objects.get(pk=customer_id)
            context['check_account'] = check_account
        return context

    def form_valid(self, form):
        account = CheckAccount.objects.get(**self.kwargs)
        # form.instance.customer = account
        # form.instance.customer_id = account.pk

        return super(UploadAccountDocumentsView, self).form_valid(form=form)


def delete_succeed_doc(request):
    return render(request, 'checkaccount/success_file_delete.html')


class DeleteAccountDocumentsView(DeleteView):
    model = AccountDocuments
    template_name = 'checkaccount/delete_check_account.html'

    # pk_url_kwarg = 'attachment_id'
    # success_url = 'checkaccount/docs/delete/succeed/'

    def post(self, request, *args, **kwargs):
        return super(DeleteAccountDocumentsView, self).post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        acc = AccountDocuments.objects.get(pk=self.kwargs.get(self.pk_url_kwarg))
        acc.delete_by_type(int(self.kwargs.get('type')))
        acc.save()

        doc_pk = self.kwargs.get('pk')  # this pk belongs to doc
        c_pk = AccountDocuments.objects.get(pk=doc_pk).customer.pk

        kw = {'pk': c_pk}
        return redirect(reverse('docs', kwargs=kw))

    def delete(self, request, *args, **kwargs):
        super(DeleteAccountDocumentsView, self).delete(request, *args, **kwargs)


class CheckAccountInitialProcesses:
    """
    Including warnings and importing some files, pulling some data etc.
    """
    account_warning_template = 'checkaccount/added_dataset_warning_base.html'

    def render_base(self, request, **kwargs):
        return render(request, self.account_warning_template, kwargs)

    def alert_popup(self, request, message_type, *messages):
        context = {'messages': messages, 'message_type': message_type}
        return self.render_base(request, context=context)

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

# DO NOT DELETE TO REMEMBER EASY WAY.
# def upload_test(request):
#     context = {}
#     if request.method == 'POST':
#         uploaded_file = request.FILES['document']
#         fs = FileSystemStorage()
#         name = fs.save(uploaded_file.name, uploaded_file)
#         context['url'] = fs.url(name)
#     return render(request, 'uploadtest.html', context)
