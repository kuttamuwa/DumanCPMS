from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView, LogoutView
from django.http.response import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
# Create your views here.
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from django.views.generic.list import ListView
from django_filters.views import FilterView
from rest_framework import status
from rest_framework.views import APIView

from checkaccount.forms import CheckAccountCreateForm, TestFileUpload
from checkaccount.models import CheckAccount
from checkaccount.serializers import CheckAccountSerializer
from .filters import CheckAccountFilter


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


def get_customer(request, customer_id):
    check_account = CheckAccount.objects.get(customer_id=customer_id)

    if request.method == 'GET':
        context = {'checkaccount': check_account}

        return render(request, context=context, template_name='checkaccount/get_check_account.html')

    if request.method == 'POST':
        print("posted")


# @login_required(login_url='/login')
# @user_passes_test(not_in_checkaccount_group, login_url='/login')
# def check_account_search(request):
#     check_account_filter = CheckAccountFilter(request.GET, queryset=CheckAccount.objects.all())
#     check_account = CheckAccount.objects.all()
#
#     return render(request, 'checkaccount/account_with_filter.html', {'account_filter': check_account_filter,
#                                                                      'checkaccount': check_account})

# if request.method == 'GET':
#     account_filter = CheckAccountFilter(request.GET)
#     checkaccount = CheckAccount.objects.all()
#
#     context = {'checkaccount': checkaccount,
#                'account_filter': account_filter, }
#     return render(request, context=context, template_name='checkaccount/account_with_filter.html')
#
# elif request.method == 'POST':
#
# context = {'checkaccount': checkaccount,
#            'account_filter': account_filter,
#            }
#
# return render(request, context=context, template_name='checkaccount/account_with_filter.html')


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
class CheckAccountFormCreateView(CreateView):  # , LoginRequiredMixin):
    template_name = 'checkaccount/checkaccount_form.html'
    # form_class = CheckAccountForm
    # success_url = 'checkaccount/succeed_form.html'
    model = CheckAccount

    fields = '__all__'

    def form_valid(self, form):
        print("form took")
        return super().form_valid(form)


class CheckAccountFormDeleteView(DeleteView):
    model = CheckAccount
    # fields = checkaccount_shown_fields


class CheckAccountFormUpdateView(UpdateView):
    # model = CheckAccountCreateForm
    fields = checkaccount_shown_fields


@method_decorator(login_required(login_url='/login'), name='dispatch')
@method_decorator(user_passes_test(not_in_checkaccount_group, login_url='/login'), name='dispatch')
class CheckAccountSearchView(FilterView):
    pass


# Attachment
class AttachmentUploadView(CreateView):
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
