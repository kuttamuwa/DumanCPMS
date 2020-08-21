from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView, LogoutView
from django.core.files.storage import FileSystemStorage
from django.http.response import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
# Create your views here.
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from django.views.generic.list import ListView
from django_filters.views import FilterView
from rest_framework import status
from rest_framework.views import APIView

from checkaccount.forms import CheckAccountCreateForm, UploadAccountDocumentForm
from checkaccount.models import CheckAccount, AccountDocuments, PartnershipDocuments, CustomerBank
from checkaccount.serializers import CheckAccountSerializer


def main_page(request):
    return render(request, 'base.html')


checkaccount_shown_fields = [i.name for i in CheckAccount._meta.get_fields() if i not in CheckAccount.get_auto_fields()]


# Site views
def checkaccount_mainpage(request):
    return render(request, 'checkaccount/checkaccount_main.html')


def not_in_checkaccount_group(user):
    if user.is_authenticated and user.groups.filter(name='CheckAccountAdmin').exists():
        return True
    else:
        return False
    # todo : https://stackoverflow.com/questions/29682704/how-to-use-the-user-passes-test-decorator-in-class-based-views
    # todo: permissions ekleyelim
    # or user.user_permissions


def succeed_create_check_account(request):
    return render(request, 'checkaccount/succeed_form.html')


def get_customer(request, customer_id, state=0):
    """

    :param request:
    :param customer_id:
    :param state: 1 -> comes from creating check account form.
                  0 -> just retrieve one account
    :return:
    """
    try:
        check_account = CheckAccount.objects.get(customer_id=customer_id)

    except CheckAccount.DoesNotExist:
        return render(request, 'checkaccount/no_check_account_error.html')

    # related account documents checking
    acc_doc_state = False
    try:
        AccountDocuments.objects.get(customer_id=customer_id)
        acc_doc_state = True

    except AccountDocuments.DoesNotExist:
        pass

    # related partnership documents checking
    part_doc_state = False
    try:
        PartnershipDocuments.objects.get(customer_id=customer_id)
        part_doc_state = True
    except PartnershipDocuments.DoesNotExist:
        pass

    # related Customer Bank Information
    bank_state = False
    try:
        CustomerBank.objects.get(customer_id=customer_id)
        bank_state = True

    except CustomerBank.DoesNotExist:
        pass

    if request.method == 'GET':
        context = {'checkaccount': check_account, 'state': state, 'acc_doc_state': acc_doc_state,
                   'part_doc_state': part_doc_state, 'bank_state': bank_state}

        return render(request, context=context, template_name='checkaccount/get_check_account_and_upload.html')


# API VIEW
class CheckAccountAPI(APIView):
    # renderer_classes = [TemplateHTMLRenderer]
    # template_name = 'templates/abc.html'

    def get(self, request, format=None):
        snippets = CheckAccount.objects.all()
        serializer = CheckAccountSerializer(snippets, many=True)
        return JsonResponse(dict(serializer.data[0]), status=201)

    def post(self, request, format=None):
        serializer = CheckAccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(serializer.data, status=status.HTTP_201_CREATED)
        return HttpResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# todo: replace with get_customer function !
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

    fields = '__all__'

    def get_success_url(self):
        return f'/checkaccount/get/{self.object.customer_id}/true'

    def form_valid(self, form):
        print("form took")
        return super().form_valid(form)


class CheckAccountFormDeleteView(DeleteView):
    model = CheckAccount
    template_name = 'checkaccount/delete_checkaccount_succeeded.html'
    success_url = '/'

    def get_queryset(self):
        qs = super(CheckAccountFormDeleteView, self).get_queryset()
        # todo : not a good way but it works
        c_id = int(self.request.path.split("/")[3])
        return qs.filter(customer_id=c_id)


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


class GetAccountDocumentsList(ListView):
    model = AccountDocuments
    template_name = 'checkaccount/uploaded_account_documents.html'
    context_object_name = 'AccountDocuments'


class UploadAccountDocumentsView(CreateView):
    model = AccountDocuments
    form_class = UploadAccountDocumentForm
    # success_url = reverse_lazy('docs', kwargs={'customer_id': })
    template_name = 'checkaccount/upload_account_document.html'

    def get_success_url(self):
        return reverse_lazy('docs', kwargs=self.kwargs)

    def get_context_data(self, **kwargs):
        customer_id = self.kwargs.get('customer_id')
        context = super().get_context_data(**kwargs)

        if customer_id is not None:
            check_account = CheckAccount.objects.get(customer_id=customer_id)
            context['check_account'] = check_account

        return context

    def form_valid(self, form):
        form.instance.customer_id = CheckAccount.objects.get(customer_id=self.kwargs.get('customer_id'))
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

# DO NOT DELETE TO REMEMBER EASY WAY.
# def upload_test(request):
#     context = {}
#     if request.method == 'POST':
#         uploaded_file = request.FILES['document']
#         fs = FileSystemStorage()
#         name = fs.save(uploaded_file.name, uploaded_file)
#         context['url'] = fs.url(name)
#     return render(request, 'uploadtest.html', context)
