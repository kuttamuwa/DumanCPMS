from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
# Create your views here.
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from django_filters.views import FilterView

from checkaccount import tests, errors
from checkaccount.forms import CheckAccountCreateForm, UploadAccountDocumentForm
from checkaccount.models import CheckAccount, AccountDocuments
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


@method_decorator(login_required(login_url='/login'), name='dispatch')
@method_decorator(user_passes_test(not_in_checkaccount_group, login_url='/login'), name='dispatch')
class CheckAccountView(DetailView):
    template_name = 'checkaccount/get_check_account_and_upload.html'
    model = CheckAccount

    def get(self, request, *args, **kwargs):
        try:
            CheckAccount.objects.get(pk=kwargs.get('pk'))  # exists?
            super(CheckAccountView, self).get(request, *args, **kwargs)

        except CheckAccount.DoesNotExist:
            # messages.warning(request, errors.DoesNotExistsWarning.message, extra_tags='alert')
            return redirect('checkaccount-create')

        return super(CheckAccountView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        return super(CheckAccountView, self).get_queryset()


@method_decorator(login_required(login_url='/login'), name='dispatch')
@method_decorator(user_passes_test(not_in_checkaccount_group, login_url='/login'), name='dispatch')
class CheckAccountFormCreateView(CreateView):
    template_name = 'checkaccount/checkaccount_form.html'
    model = CheckAccount
    form_class = CheckAccountCreateForm

    def get_success_url(self):
        return f'/checkaccount/get/{self.object.pk}'

    def get_form(self, form_class=None):
        form = super(CheckAccountFormCreateView, self).get_form(form_class)

        if self.request.method == 'POST':
            return form

        elif self.request.method == 'GET':
            form.instance.created_by = self.request.user

            # FOR TESTING
            ca = tests.CheckAccountTest.test_create_one_account(self.request.user)
            ca.created_by = self.request.user

            form = CheckAccountCreateForm(instance=ca)

            return form


@method_decorator(login_required(login_url='/login'), name='dispatch')
@method_decorator(user_passes_test(not_in_checkaccount_group, login_url='/login'), name='dispatch')
class CheckAccountFormDeleteView(DeleteView):
    model = CheckAccount
    template_name = 'checkaccount/delete_checkaccount_succeeded.html'
    success_url = '/'

    def get(self, request, *args, **kwargs):
        try:
            CheckAccount.objects.get(pk=kwargs.get('pk'))  # exists?
            return super(CheckAccountFormDeleteView, self).get(request, *args, **kwargs)

        except CheckAccount.DoesNotExist:
            messages.warning(request, messages.WARNING, errors.DoesNotExistsWarning.message)
            return redirect('ch-index')

    def post(self, request, *args, **kwargs):
        try:
            ca = CheckAccount.objects.get(pk=self.kwargs.get('pk'))

            # if customers deleted, also documents must be deleted
            # kw = {'pk': ca.pk, 'type': 4}
            # reverse('delete_docs', kwargs=kw)
            # messages.add_message(request, messages.INFO, 'Related documents were deleted also !')

            super(CheckAccountFormDeleteView, self).post(request, *args, **kwargs)
            return redirect('ch-index')

        except CheckAccount.DoesNotExist:
            messages.add_message(request, messages.WARNING, 'There is no Check account !')
            return redirect('ch-index')


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

    def get(self, request, *args, **kwargs):
        try:
            ca = CheckAccount.objects.get(**self.kwargs)
            acc = AccountDocuments.objects.get(customer=ca)
            all_uploaded = acc.check_all_field_uploaded()  # True -> all is uploaded, False is at least one is not

            if all_uploaded:
                self.kwargs['pk'] = acc.pk  # we redirect with check account pk

            else:  # objects were created before but deleted one of them.
                return redirect('upload_docs', **kwargs)

        except AccountDocuments.DoesNotExist:
            messages.warning(request, errors.DoesNotExistsWarning)
            return redirect('upload_docs', **kwargs)

        except CheckAccount.DoesNotExist:
            return redirect('ch-index')

        return super(GetAccountDocumentsList, self).get(request, *args, **kwargs)


class UploadAccountDocumentsView(CreateView):
    model = AccountDocuments
    form_class = UploadAccountDocumentForm
    success_url = reverse_lazy('docs')
    template_name = 'checkaccount/upload_account_document.html'

    def update(self):
        form = UploadAccountDocumentForm(self.request.FILES)

        pk = self.kwargs.get('pk')
        check_account = CheckAccount.objects.get(pk=pk)
        acc = AccountDocuments.objects.get(customer=check_account)
        form.instance = acc

    def post(self, request, *args, **kwargs):
        try:
            ca = CheckAccount.objects.get(pk=self.kwargs.get('pk'))
            acc = AccountDocuments.objects.get(customer=ca)
            kwargs['pk'] = acc.pk

        except CheckAccount.DoesNotExist:
            # messages.warning(request, errors.DoesNotExistsWarning)
            return redirect('ch-index')

        except AccountDocuments.DoesNotExist:
            return super(UploadAccountDocumentsView, self).post(request, *args, **kwargs)

    def file_all_check(self):
        checkaccount_id = self.kwargs.get('pk')
        doc_control = self.document_control(checkaccount_id)
        if all(doc_control.values()):
            return True
        else:
            return False

    def get(self, request, *args, **kwargs):
        try:
            if self.file_all_check():
                # If all file uploaded?
                return redirect(reverse('docs', kwargs=self.kwargs))

            response = super(UploadAccountDocumentsView, self).get(request, *args, **kwargs)

            return response
        except CheckAccount.DoesNotExist:
            # messages.warning(request, errors.DoesNotExistsWarning)
            return redirect('ch-index')

    def fill_other_fields_auto(self, form):
        acc = AccountDocuments.objects.get(customer=self.kwargs.get('pk'))

        if acc.activity_certificate_pdf.name not in ("", None):
            form.instance.activity_certificate_pdf = acc.activity_certificate_pdf

        if acc.tax_return_pdf.name not in ("", None):
            form.instance.tax_return_pdf = acc.tax_return_pdf

        if acc.authorized_signatures_list_pdf.name not in ("", None):
            form.instance.authorized_signatures_lidf_pdf = acc

        return form

    def fill_form_auto(self, form):
        check_account = CheckAccount.objects.get(pk=self.kwargs.get('pk'))

        form.instance.created_by = self.request.user
        form.instance.created_date = datetime.now()
        form.instance.customer = check_account

        # form all fields
        f_fields = list(form.fields.keys())
        for f in f_fields:
            if getattr(form.instance, f).name is not None:
                f.instance = getattr(form.instance, f)

        # if another field was filled before ?
        try:
            self.fill_other_fields_auto(form)
        except AccountDocuments.DoesNotExist:
            pass

        return form

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
            f = self.fill_form_auto(f)

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
        return super(UploadAccountDocumentsView, self).form_valid(form=form)


def delete_succeed_doc(request):
    return render(request, 'checkaccount/success_file_delete.html')


class DeleteAccountDocumentsView(DeleteView):
    model = AccountDocuments
    template_name = 'checkaccount/delete_check_account.html'

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



